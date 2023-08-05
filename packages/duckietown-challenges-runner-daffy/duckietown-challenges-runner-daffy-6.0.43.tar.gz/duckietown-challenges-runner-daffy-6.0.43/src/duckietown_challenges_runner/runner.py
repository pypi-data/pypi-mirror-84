#!/usr/bin/env python3
import argparse
import copy
import getpass
import json
import logging
import mimetypes
import os
import platform
import random
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import traceback
from contextlib import contextmanager
from typing import Callable, Dict, List, Optional, Set, Tuple
from urllib.parse import urlsplit

import termcolor
import timeout_decorator
import yaml
from ansi2html import Ansi2HTMLConverter
from dateutil import parser
from docker.models.containers import Container
from six import BytesIO
from zuper_commons.fs import write_ustring_to_utf8_file
from zuper_commons.text import box
from zuper_commons.types import ZException

from duckietown_challenges import __version__ as version_dc, ChallengesConstants, get_duckietown_server_url
from duckietown_challenges.challenge import ChallengeDescription, EvaluationParameters
from duckietown_challenges.challenge_results import (
    ChallengeResults,
    NoResultsFound,
    read_challenge_results,
)
from duckietown_challenges.cmd_submit_build import get_complete_tag, parse_complete_tag
from duckietown_challenges.constants import (
    CHALLENGE_DESCRIPTION_DIR,
    CHALLENGE_EVALUATION_OUTPUT_DIR,
    CHALLENGE_PREVIOUS_STEPS_DIR,
    CHALLENGE_RESULTS_DIR,
    CHALLENGE_SOLUTION_OUTPUT_DIR,
    CHALLENGE_TMP_SUBDIR,
    DEFAULT_DTSERVER,
    ENV_CHALLENGE_NAME,
    ENV_CHALLENGE_STEP_NAME,
)
from duckietown_challenges.rest_methods import (
    dtserver_job_heartbeat,
    dtserver_report_job,
    dtserver_work_submission,
    get_challenge_description,
    SubmissionID,
)
from duckietown_challenges.utils import friendly_size, indent
from duckietown_docker_utils.docker_run import get_developer_volumes
from . import __version__, __version__ as version_dcr
from .env_checks import (
    check_docker_environment,
    check_executable_exists,
    InvalidEnvironment,
)
from .exceptions import UserError
from .ipfs_utils import ipfs_available
from .logging import elogger
from .runner_cache import copy_to_cache, get_file_from_cache
from .shell_config import DTShellConstants, read_shell_config
from .types import ContainerName


def get_token_from_shell_config():
    k = DTShellConstants.DT1_TOKEN_CONFIG_KEY

    if k in os.environ:
        # msg = 'Using token passed in environment variable %s' % k
        # elogger.debug(msg)
        return os.environ[k]
    else:
        pass

        # msg = 'Could not find the env variable %s; reading shell config.' % k
        # elogger.debug(msg)

    shell_config = read_shell_config()
    if shell_config.token_dt1 is None:
        msg = "Please set a Duckietown Token using the command `dts tok set`."
        raise UserError(msg)
    else:
        return shell_config.token_dt1


def dt_challenges_evaluator():
    try:
        dt_challenges_evaluator_()
    except SystemExit:  # --help
        raise
    except BaseException:
        msg = traceback.format_exc()
        elogger.error(msg)
        sys.exit(2)


# noinspection PyBroadException
def dt_challenges_evaluator_(args: List[str] = None, token: str = None):
    from duckietown_challenges.col_logging import setup_logging

    setup_logging()
    elogger.info(f"dt-challenges-evaluator {__version__}", args=args, sys_argv=sys.argv)

    usage = """

Usage:

"""
    prog = "dt-challenges-evaluator"
    parser = argparse.ArgumentParser(prog=prog, usage=usage)
    parser.add_argument("--version", action="store_true", default=False)
    parser.add_argument("--continuous", action="store_true", default=False)
    parser.add_argument("--no-pull", dest="no_pull", action="store_true", default=False)
    parser.add_argument("--no-upload", dest="no_upload", action="store_true", default=False)
    parser.add_argument("--no-delete", dest="no_delete", action="store_true", default=False)
    parser.add_argument("--no-cache", dest="no_cache", action="store_true", default=False)
    parser.add_argument("--ipfs", dest="ipfs", action="store_true", default=False)
    parser.add_argument("--one", dest="one", action="store_true", default=False)
    parser.add_argument("--keep-registry", dest="do_not_mess_with_repo", action="store_true", default=False)
    parser.add_argument("--machine-id", default=None, help="Machine name")
    parser.add_argument("--name", default=None, help="Evaluator name")
    parser.add_argument("--impersonate", default=None)
    DEFAULT_TMPDIR = "/tmp/duckietown/DT18/evaluator/executions"

    parser.add_argument("--tmpdir", default=DEFAULT_TMPDIR)
    parser.add_argument("--submission", default=None, help="evaluate this particular submission")
    parser.add_argument(
        "--reset", dest="reset", action="store_true", default=False, help="Reset submission",
    )
    parser.add_argument("--features", default="{}")
    parser.add_argument("--debug-volumes", default=None)
    parsed = parser.parse_args(args=args)
    if parsed.submission and parsed.continuous:
        msg = "Cannot specify both --submission and --continuous."
        raise UserError(msg)
    if parsed.version:
        msg = f"Duckietown Challenges Runner {__version__}"
        from duckietown_challenges import __version__ as dcversion

        msg += f"\nDuckietown Challenges {dcversion}"
        print(msg)
        return

    copy_to_machine_cache = not parsed.no_cache
    check_docker_environment()
    try:
        check_executable_exists("docker-compose")
    except InvalidEnvironment:
        msg = "Could not find docker-compose. Please install it."
        msg += "\n\nSee: https://docs.docker.com/compose/install/#install-compose"
        raise InvalidEnvironment(msg)
    tmpdir = parsed.tmpdir

    try:
        more_features = yaml.load(parsed.features, Loader=yaml.SafeLoader)
    except BaseException as e:
        msg = "Could not evaluate your YAML string %r:\n%s" % (parsed.features, e)
        raise Exception(msg)

    if not isinstance(more_features, dict):
        msg = "I expected that the features are a dict; obtained %s: %r" % (
            type(more_features).__name__,
            more_features,
        )
        raise Exception(msg)

    do_pull = not parsed.no_pull
    do_upload = not parsed.no_upload
    delete = not parsed.no_delete
    reset = parsed.reset
    evaluator_name = (parsed.name or "noname") + "-" + "%s" % socket.gethostname() + "-" + "%s" % os.getpid()
    machine_id = parsed.machine_id or socket.gethostname()
    allow_host_network = False

    if token is None:
        token = get_token_from_shell_config()

    if parsed.continuous:

        timeout = 5.0  # seconds
        multiplier = 1.0
        multiplier_grow = 1.5
        max_multiplier = 5
        while True:
            multiplier = min(multiplier, max_multiplier)
            t0 = time.time()
            try:
                go_(
                    None,
                    reset=False,
                    do_upload=do_upload,
                    do_pull=do_pull,
                    more_features=more_features,
                    delete=delete,
                    evaluator_name=evaluator_name,
                    machine_id=machine_id,
                    tmpdir=tmpdir,
                    token=token,
                    debug_volumes=parsed.debug_volumes,
                    impersonate=parsed.impersonate,
                    copy_to_machine_cache=copy_to_machine_cache,
                    allow_host_network=allow_host_network,
                    use_ipfs=parsed.ipfs,
                    do_not_mess_with_repo=parsed.do_not_mess_with_repo,
                )
                multiplier = 1.0
                if parsed.one:
                    msg = "Because --one was passed, I will finish here."
                    elogger.info(msg)
                    break
            except NothingLeft:
                delta = time.time() - t0

                elogger.debug(f"No work for me yet. Server answers in {delta:.1f} seconds.")
                # ndots += 1
                # if ndots == 5:
                #     # sys.stderr.write(' no work for me yet.\n')
                #     ndots = 0
                # time.sleep(timeout * multiplier)
                # elogger.info('No submissions available to evaluate.')
            except ConnectionError as e:
                elogger.error(e)
                multiplier *= multiplier_grow
            except KeyboardInterrupt:
                break
            except BaseException:
                msg = "Uncaught exception"
                elogger.error(msg, e=traceback.format_exc())
                multiplier *= multiplier_grow

            r = random.random() * 2

            try:
                time.sleep(timeout * multiplier + r)
            except KeyboardInterrupt:
                break

    else:
        if parsed.submission:
            submissions = [parsed.submission]
        else:
            submissions = [None]

        for submission_id in submissions:
            try:
                go_(
                    submission_id,
                    reset=reset,
                    do_upload=do_upload,
                    do_pull=do_pull,
                    more_features=more_features,
                    delete=delete,
                    evaluator_name=evaluator_name,
                    machine_id=machine_id,
                    tmpdir=tmpdir,
                    token=token,
                    debug_volumes=parsed.debug_volumes,
                    impersonate=parsed.impersonate,
                    copy_to_machine_cache=copy_to_machine_cache,
                    allow_host_network=allow_host_network,
                    use_ipfs=parsed.ipfs,
                    do_not_mess_with_repo=parsed.do_not_mess_with_repo,
                )
            except NothingLeft as e:
                if submission_id is None:
                    msg = "No submissions available to evaluate."
                else:
                    msg = f"Could not evaluate submission {submission_id}."

                msg += "\n" + str(e)
                elogger.error(msg)


class NothingLeft(ZException):
    pass


def get_features(more_features, use_ipfs: bool):
    import psutil

    features = {}

    machine = platform.machine()
    features["linux"] = sys.platform.startswith("linux")
    features["mac"] = sys.platform.startswith("darwin")
    features["x86_64"] = machine == "x86_64"
    features["armv7l"] = machine == "armv7l"
    meminfo = psutil.virtual_memory()
    # svmem(total=16717422592, available=5376126976, percent=67.8, used=10359984128, free=1831890944,
    # active=7191916544, inactive=2325667840, buffers=525037568, cached=4000509952, shared=626225152)

    features["ram_total_mb"] = int(meminfo.total / (1024 * 1024.0))
    features["ram_available_mb"] = int(meminfo.available / (1024 * 1024.0))
    features["nprocessors"] = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    if cpu_freq is not None:
        # None on Docker
        features["processor_frequency_mhz"] = int(psutil.cpu_freq().max)
    f = psutil.cpu_percent(interval=0.2)
    features["processor_free_percent"] = int(100.0 - f)
    features["p1"] = True

    disk = psutil.disk_usage(os.getcwd())

    features["disk_total_mb"] = disk.total / (1024 * 1024)
    features["disk_available_mb"] = disk.free / (1024 * 1024)
    features["picamera"] = False
    features["nduckiebots"] = False
    features["compute_sims"] = True
    # features['map_3x3'] = False

    if use_ipfs:
        if not ipfs_available():
            msg = "IPFS needed but not found"
            raise UserError(msg)
        else:
            elogger.info("OK - IPFS still working well")
        features["ipfs"] = 1

    features["gpu"] = os.path.exists("/proc/driver/nvidia/version")

    for k, v in more_features.items():
        if k in features:
            msg = f"Using {k!r} = {more_features[k]!r} instead of {features[k]!r}"
            # elogger.info(msg)
        features[k] = v

    # elogger.debug(json.dumps(features, indent=4))

    return features


class DockerComposeFail(ZException):
    pass


def get_FORMAT_datefmt():
    pre = "%(asctime)s|%(name)s|%(filename)s:%(lineno)s|%(funcName)s(): "
    pre = termcolor.colored(pre, attrs=["dark"])
    FORMAT = pre + "%(message)s"
    datefmt = "%H:%M:%S"
    return FORMAT, datefmt


@contextmanager
def setup_logging(wd):
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    if not os.path.exists(wd):
        os.makedirs(wd)
    f_stderr = os.path.join(wd, "stderr.log")
    f_stdout = os.path.join(wd, "stdout.log")

    my_stderr = Tee(os.path.join(wd, "stderr.log"), sys.stderr)
    sys.stderr = my_stderr
    my_stdout = Tee(os.path.join(wd, "stdout.log"), sys.stdout)
    sys.stdout = my_stdout
    ch = logging.StreamHandler(sys.stderr.file)

    ch.setLevel(logging.DEBUG)

    root = logging.getLogger()
    FORMAT, datefmt = get_FORMAT_datefmt()
    formatter = logging.Formatter(FORMAT, datefmt=datefmt)
    ch.setFormatter(formatter)
    root.addHandler(ch)

    try:
        yield
    finally:
        #
        my_stdout.flush()
        my_stderr.flush()

        # for s in [my_stderr, my_stdout]:
        #     try:
        #         fn = os.path.splitext(s.name)[0] + '.html'
        #         with open(fn, 'w') as f:
        #             from ansi2html import Ansi2HTMLConverter
        #             conv = Ansi2HTMLConverter()
        #             v = s.getvalue().strip()
        #             if not v:
        #                 v = '(No output was produced.)'
        #             html = conv.convert(v)
        #             f.write(html)
        #         os.remove(s.name)
        #     except:
        #         pass

        sys.stderr = old_stderr
        sys.stdout = old_stdout
        root.removeHandler(ch)

    def convert(log):
        fn = os.path.splitext(log)[0] + ".html"
        if not os.path.exists(log):
            data = f"There was no output produced. File not found: {log}"
        else:
            data = open(log).read().strip()

            if not data:
                data = "(No output was produced.)"

        # noinspection PyBroadException
        try:
            conv = Ansi2HTMLConverter()
            html = conv.convert(data)
            write_ustring_to_utf8_file(html, fn)

        except:
            pass
        # os.remove(log)

    convert(f_stdout)
    convert(f_stderr)


def go_(
    submission_id: Optional[SubmissionID],
    do_pull: bool,
    more_features,
    do_upload: bool,
    delete: bool,
    reset: bool,
    evaluator_name: str,
    machine_id: str,
    tmpdir: str,
    copy_to_machine_cache: bool,
    token: str = None,
    impersonate: Optional[int] = None,
    debug_volumes: Optional[str] = None,
    allow_host_network: bool = False,
    use_ipfs: bool = False,
    do_not_mess_with_repo: bool = False,
):
    if use_ipfs:
        allow_host_network = True
    features = get_features(more_features, use_ipfs=use_ipfs)
    # if features['processor_free_percent'] < 10:
    #     elogger.info(f"Waiting because free CPU is {features['processor_free_percent']}%.")
    #     return

    if token is None:
        token = get_token_from_shell_config()

    url = get_duckietown_server_url()

    if do_not_mess_with_repo:
        elogger.info(f"Do not mess with repo")
        server_host = None
    else:
        elogger.info(url=url)
        url_parsed = urlsplit(url)
        netloc: str = url_parsed.netloc
        if ":" in netloc:
            server_host, _, _ = netloc.rpartition(":")
        else:
            server_host = netloc
        if not server_host:
            raise ZException(url=url, server_host=server_host)

    elogger.info(f"Using server_host", server_host=server_host, url=url)

    evaluator_version = f"d-c:{version_dc};d-c-r:{version_dcr}"
    process_id = evaluator_name

    timeout_server = 60
    res = dtserver_work_submission(
        token,
        submission_id,
        machine_id,
        process_id,
        evaluator_version,
        features=features,
        reset=reset,
        timeout=timeout_server,
        impersonate=impersonate,
    )

    if "job_id" not in res:
        elogger.info("No jobs available", url=url)
        msg = "Could not find jobs."
        raise NothingLeft(msg, res=res)
    job_id = res["job_id"]
    elogger.info(res=res)

    if False:
        cd = get_challenge_description(token, res["challenge_name"], impersonate=impersonate)
    else:
        cd = None

    def heartbeat():
        res = None
        try:
            res = dtserver_job_heartbeat(
                token,
                job_id=job_id,
                machine_id=machine_id,
                process_id=process_id,
                evaluator_version=evaluator_version,
                impersonate=impersonate,
            )

            abort = res["abort"]
            why = res["why"]
        except:
            elogger.warning(traceback.format_exc(), res=res)
        else:
            if abort:
                msg = f"The server told us to abort the job because: {why}"
                raise KeyboardInterrupt(msg)

    cr, uploaded = get_cr(
        res,
        tmpdir,
        do_upload,
        evaluator_name,
        job_id,
        delete,
        debug_volumes,
        do_pull,
        copy_to_machine_cache=copy_to_machine_cache,
        allow_host_network=allow_host_network,
        use_ipfs=use_ipfs,
        server_host=server_host,
        cd=cd,
        heartbeat=heartbeat,
    )

    msg = "Reporting status %s for job %s submission %s.\n\n%s\n\n%s\n\n%s" % (
        cr.get_status(),
        job_id,
        submission_id,
        indent(cr.msg, " msg |"),
        indent(json.dumps(cr.get_stats(), indent=4), "stats |"),
        cr.ipfs_hashes,
    )
    if cr.get_status() != ChallengesConstants.STATUS_JOB_SUCCESS:
        elogger.error(msg)
    else:
        elogger.info(msg)

    stats = cr.get_stats()
    # REST call to the duckietown chalenges server
    ntries = 5
    interval = 10
    while ntries >= 0:
        try:
            dtserver_report_job(
                token,
                job_id=job_id,
                stats=stats,
                result=cr.get_status(),
                ipfs_hashes=cr.ipfs_hashes,
                machine_id=machine_id,
                process_id=process_id,
                evaluator_version=evaluator_version,
                uploaded=uploaded,
                impersonate=impersonate,
                timeout=timeout_server,
            )
            break
        except BaseException:
            msg = "Could not report."
            elogger.warning(msg, e=traceback.format_exc())
            elogger.info(f"Retrying {ntries} more times after {interval} seconds")
            ntries -= 1
            time.sleep(interval)


def get_cr(
    res: dict,
    tmpdir: str,
    do_upload: bool,
    evaluator_name: str,
    job_id: int,
    delete: bool,
    debug_volumes,
    do_pull: bool,
    copy_to_machine_cache: bool,
    allow_host_network: bool,
    use_ipfs: bool,
    server_host: str,
    cd: Optional[ChallengeDescription],
    heartbeat: Optional[Callable] = None,
) -> Tuple[ChallengeResults, List]:
    # noinspection PyBroadException
    try:

        challenge_name = res["challenge_name"]
        challenge_step_name = res["step_name"]
        submission_id = res["submission_id"]
        timeout_sec = res["timeout"]
        if timeout_sec is None or timeout_sec == 0:
            msg = f"Invalid timeout {timeout_sec}"
            raise ValueError(msg)

    except BaseException:
        msg = "Uncaught exception."
        elogger.error(msg, e=traceback.format_exc())
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        return ChallengeResults(status, msg, scores={}), []

    uploaded = []
    wd = None
    # noinspection PyBroadException
    try:

        steps2artefacts = res["steps2artefacts"]

        locations = res["parameters"]["locations"]
        location = locations[0]
        organization = location["organization"]
        repository = location["repository"]
        tag = location["tag"]
        digest = location["digest"]  # FIXME: previously disabled, now we should re-enable
        registry = location["registry"]

        if registry == "dockerhub":
            registry = "docker.io"

            # solution_container = f"{organization}/{repository}:{tag}"
        solution_container = f"{registry}/{organization}/{repository}:{tag}@{digest}"
        # else:
        #     solution_container = f"{registry}/{organization}/{repository}:{tag}"
        elogger.info(f"solution_container = {solution_container}")

        wd0 = os.path.join(
            tmpdir,
            challenge_name,
            f"submission{submission_id}",
            f"{challenge_step_name}-{evaluator_name}-job{job_id}",
        )
        wd = wd0 + "-a-wd"
        fd = wd0 + "-a-fifos"

        if not os.path.exists(wd):
            os.makedirs(wd)
        if not os.path.exists(fd):
            os.makedirs(fd)
        own_logs_dir = os.path.join(wd, "logs", "challenges-runner")

        aws_config = res["aws_config"]
        if aws_config and do_upload:
            try_s3(aws_config)

        require_scores = set()

        if cd is not None:
            if len(cd.steps) == 1:
                require_scores = set(_.name for _ in cd.scoring.scores)

        try:

            with setup_logging(own_logs_dir):
                elogger.debug("running get_cr()", delete=delete, copy_to_machine_cache=copy_to_machine_cache)
                challenge_parameters_ = EvaluationParameters.from_yaml(res["challenge_parameters"])

                rnd = random.randint(1, 1000000)

                project = f"{evaluator_name}-job{job_id}-{rnd}"
                if not do_upload:
                    aws_config = None

                cr = run_single(
                    wd=wd,
                    fd=fd,
                    aws_config=aws_config,
                    steps2artefacts=steps2artefacts,
                    challenge_parameters=challenge_parameters_,
                    solution_container=solution_container,
                    challenge_name=challenge_name,
                    challenge_step_name=challenge_step_name,
                    project=project,
                    do_pull=do_pull,
                    debug_volumes=debug_volumes,
                    timeout_sec=timeout_sec,
                    allow_host_network=allow_host_network,
                    use_ipfs=use_ipfs,
                    server_host=server_host,
                    require_scores=require_scores,
                    heartbeat=heartbeat,
                )
        finally:
            if do_upload:
                uploaded = upload_files(wd, aws_config, copy_to_machine_cache=copy_to_machine_cache)

        try:
            cmd = ["down"]
            run_docker(wd, project, cmd)
        except DockerComposeFail:
            elogger.warning("While taking down after success:\n\n" + traceback.format_exc())

    except KeyboardInterrupt:
        msg = f"KeyboardInterrupt:\n{traceback.format_exc()}"

        cmd = ["down"]
        if wd is not None:
            try:
                run_docker(wd, project, cmd)
            except DockerComposeFail:
                elogger.warning("While taking down after failure:\n\n" + traceback.format_exc())

        elogger.error(msg)
        status = ChallengesConstants.STATUS_JOB_ABORTED
        cr = ChallengeResults(status, msg, scores={})

    except IPFSException:
        msg = f"Could not access IPFS data:\n{traceback.format_exc()}"
        elogger.error(msg)
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        cr = ChallengeResults(status, msg, scores={})

    except BaseException:
        msg = f"Uncaught exception:\n{traceback.format_exc()}"
        elogger.error(msg)
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        cr = ChallengeResults(status, msg, scores={})
    finally:
        if wd:
            if delete:
                msg = f"I am deleting temporary dir {wd}"
                elogger.info(msg, contents=list_all_files(wd))
                if os.path.exists(wd):
                    shutil.rmtree(wd)
            else:
                msg = f"I will not delete temporary dir {wd}"
                elogger.info(msg)
        else:
            elogger.info("Temp dir wd not set")

    return cr, uploaded


class IPFSException(Exception):
    pass


def run_single(
    *,
    wd: str,
    fd: str,
    aws_config,
    steps2artefacts,
    challenge_parameters: EvaluationParameters,
    solution_container: str,
    challenge_name: str,
    challenge_step_name: str,
    project: str,
    do_pull: bool,
    server_host: Optional[str],
    debug_volumes: Optional[str] = None,
    timeout_sec: float,
    require_scores: Set[str],
    allow_host_network: bool = False,
    use_ipfs: bool = False,
    heartbeat: Optional[Callable] = None,
):
    """

    :param wd:
    :param fd: Directory for fifos
    :param aws_config:
    :param steps2artefacts:
    :param challenge_parameters:
    :param solution_container:
    :param challenge_name:
    :param challenge_step_name:
    :param project:
    :param do_pull:
    :param server_host:
    :param debug_volumes:
    :param timeout_sec:
    :param require_scores: Set of scores required for this step to be valid
    :param allow_host_network:
    :param use_ipfs:
    :param heartbeat:

    :return:
    """
    prepare_dir(wd, aws_config, steps2artefacts, use_ipfs=use_ipfs)

    tomonitor: List[ContainerName] = []
    for service_name, service_def in challenge_parameters.services.items():
        if service_def.image == ChallengesConstants.SUBMISSION_CONTAINER_TAG:
            continue
        else:
            if "evaluator" in service_name:
                tomonitor.append(ContainerName(service_name))
    if not tomonitor:
        elogger.error(f"Cannot find any container to monitor among {list(challenge_parameters.services)}")

    elogger.info(f"The containers to monitor: {tomonitor}")
    add_extra_environment = {}
    add_extra_environment[ENV_CHALLENGE_NAME] = challenge_name
    add_extra_environment[ENV_CHALLENGE_STEP_NAME] = challenge_step_name
    # add_extra_environment["submission_id"] = submission_id
    add_extra_environment[ChallengesConstants.SUBMISSION_CONTAINER_TAG] = solution_container
    #
    # fd = os.path.join(wd, "fifos")
    # if os.path.exists(fd):
    #     shutil.rmtree(fd)
    # os.makedirs(fd)

    config = get_config(
        wd=wd,
        fd=fd,
        server_host=server_host,
        challenge_parameters_=challenge_parameters,
        solution_container=solution_container,
        debug_volumes=debug_volumes,
        allow_host_network=allow_host_network,
        add_extra_environment=add_extra_environment,
        use_ipfs=use_ipfs,
    )
    config_yaml = yaml.safe_dump(config, encoding="utf-8", indent=4, allow_unicode=True)
    if isinstance(config_yaml, bytes):
        config_yaml = config_yaml.decode("utf-8")
    # elogger.debug('YAML:\n' + config_yaml)

    dcfn_original = os.path.join(wd, "docker-compose.original.yaml")
    dcfn = os.path.join(wd, "docker-compose.yaml")

    # elogger.info('Compose file: \n%s ' % compose)
    write_ustring_to_utf8_file(config_yaml, dcfn_original)
    write_ustring_to_utf8_file(config_yaml, dcfn)

    # validate the configuration

    try:
        config_validated = run_docker(wd, project, ["config"], get_output=True).decode("utf-8")
        write_ustring_to_utf8_file(config_validated, dcfn)
        elogger.info(config_orig=config_yaml, config_validated=config_validated)
        valid_config = True
        valid_config_error = None
    except DockerComposeFail:
        valid_config_error = "Could not validate Docker Compose configuration:\n%s" % traceback.format_exc()
        elogger.error(valid_config_error)
        valid_config = False

    if valid_config:
        services_names = list(challenge_parameters.services)
        # print('services: %s' % services_names)
        cr = run_one(
            wd,
            project,
            do_pull,
            services=services_names,
            monitor=tomonitor[0],
            timeout_sec=timeout_sec,
            heartbeat=heartbeat,
        )

        write_logs(wd, project, services=config["services"])
    else:
        status = ChallengesConstants.STATUS_JOB_ERROR

        cr = ChallengeResults(status, valid_config_error, scores={})

    if cr.status == ChallengesConstants.STATUS_JOB_SUCCESS:
        found_scores = set(cr.scores)
        missing_scores = require_scores - found_scores
        if missing_scores:
            msg = f"Missing scores: requires {require_scores} found {found_scores}"
            elogger.error(msg)
            cr.status = ChallengesConstants.STATUS_JOB_ERROR
            cr.msg = msg

    return cr


def get_id_for_service(wd, project, service_name) -> str:
    cmd = ["ps", "-q", service_name]

    try:
        o = run_docker(wd, project, cmd, get_output=True)
        container_id = o.decode("utf-8").strip()  # \n at the end
    except DockerComposeFail:
        raise
    return container_id


class EvaluatorTimeout(Exception):
    pass


def write_logs_worker(service_name, container_id):
    # elogger.info('writing logs for %s ' % container_id)

    client = check_docker_environment()

    container = client.containers.get(container_id)
    for x in container.logs(stream=True, stdout=True, stderr=True, timestamps=True):
        x = x.decode("utf-8")
        i = x.index(" ")
        timestamp = x[:i]
        message = x[i + 1 :].rstrip()  # \n
        ts = parser.parse(timestamp)
        s = f"{ts.strftime('%H:%M:%S')} {service_name} {message}"
        sys.stdout.write(s + "\n")
        sys.stdout.flush()
        if container.status != "running":
            break

    exit_code = exit_code_for_container(container_id)

    elogger.info(f"container {service_name} terminated with {exit_code}")


def exit_code_for_container(container_id):
    cmd = ["docker", "inspect", container_id, "--format={{.State.ExitCode}}"]
    out = subprocess.check_output(cmd)
    return int(out.strip())


class Workers(object):
    workers = []


def stream_logs(service_name, container_id):
    from multiprocessing import Process

    p = Process(target=write_logs_worker, args=(service_name, container_id))
    p.start()
    Workers.workers.append(p)


def teminate_workers():
    for p in list(Workers.workers):
        # elogger.debug('terminating %s' % p)
        Workers.workers.remove(p)
        p.terminate()
    # elogger.debug('terminated all workers.')


# noinspection PyBroadException
def run_one(
    wd: str,
    project: str,
    do_pull: bool,
    monitor: ContainerName,
    services,
    timeout_sec: float,
    heartbeat: Optional[Callable] = None,
):
    client = check_docker_environment()

    # noinspection PyBroadException
    try:
        if do_pull:
            elogger.info("pulling containers...")
            cmd = ["pull"]  # '--ignore-pull-failures'
            run_docker(wd, project, cmd)

        try:
            _pruned = client.networks.prune(filters=dict(until="1h"))
            # elogger.debug('pruned: %s' % pruned)
        except BaseException:  # XXX not critical
            pass

        # elogger.info('Creating containers')
        # cmd = ['create', '--force-recreate']
        # run_docker(wd, project, cmd)
        cmd = [
            "down",
            "-v",
            # '--remove-orphans',
            # '--abort-on-container-exit'
        ]
        run_docker(wd, project, cmd)
        elogger.info("Running containers %s" % services)
        cmd = [
            "up",
            "-d",
            "--renew-anon-volumes",
            # '--remove-orphans',
            # '--abort-on-container-exit'
        ]
        elogger.info("now running", wd=wd, cwd=os.getcwd(), wd_files=list_all_files(wd))
        run_docker(wd, project, cmd)

        service2id = {}
        for service_name in services:
            service2id[service_name] = get_id_for_service(wd, project, service_name)
            stream_logs(service_name, service2id[service_name])
        t0 = time.time()

        client = check_docker_environment()

        for service_name, container_id in service2id.items():
            container: Container = client.containers.get(container_id)
            container.reload()
            #
            # cpu.cfs_quota_us: the total available run-time within a period (in microseconds)
            # cpu.cfs_period_us: the length of a period (in microseconds)
            # cpu.stat: exports throttling statistics [explained further below]

            if "solution" in service_name:
                if False:
                    # every second
                    cpu_period = 1000 * 1000
                    # get 100% cpu
                    cpu_quota = 1000 * 1000

                    container.update(cpu_period=cpu_period, cpu_quota=cpu_quota)
                    elogger.info(
                        "Applying CPU quota",
                        service_name=service_name,
                        cpu_period=cpu_period,
                        cpu_quota=cpu_quota,
                    )

            # noinspection PyUnresolvedReferences
            ports = container.ports
            # {'10123/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '32769'}]}
            elogger.info(f"container ports: {ports}")
            for port_proto, forwards in ports.items():
                for forward in forwards:
                    if "HostPort" in forward:
                        HostPort = forward["HostPort"]

                        msg = f"   Visualization will be available shortly at http://127.0.0.1:{HostPort}   "
                        # msg = termcolor.colored(msg, color="blue")
                        msg = "\n" * 10 + box(msg) + "\n" * 2
                        elogger.info(msg)

        exited = []
        while True:
            if heartbeat:
                heartbeat()
            running = []
            for service_name, container_id in service2id.items():
                if service_name in exited:
                    continue
                container = client.containers.get(container_id)
                # msg = 'service %s: %s' % (service_name, container.status)
                # elogger.debug(msg)
                if container.status != "running":
                    exited.append(service_name)
                    exit_code = exit_code_for_container(container_id)
                    if exit_code:
                        msg = f'The container "{service_name}" exited with code {exit_code}.\n'
                        if exit_code == 137:
                            msg += (
                                "\n\nError code 137 likely means an out-of-memory error. You likely did not "
                                "give "
                                "Docker enough RAM."
                            )

                        msg += "\n\nLook at the logs for the container to know more about the error."
                        elogger.error(msg)
                        try:
                            cr = read_challenge_results(wd)
                        except NoResultsFound:
                            msg2 = f"No results found! Something very wrong. \n{traceback.format_exc()}"
                            elogger.error(msg2)
                            msg += "\n\n" + msg2
                            status = ChallengesConstants.STATUS_JOB_ERROR
                            cr = ChallengeResults(status, msg, scores={})
                        return cr
                else:
                    running.append(service_name)

            delta = time.time() - t0
            msg = (
                f"Running for {int(delta)} s (timeout: {int(timeout_sec)} s). Services running: {running}  "
                f"exited:  {exited}"
            )
            elogger.debug(msg)

            if monitor in exited:
                elogger.info(f"The container {monitor!r} has exited; bye bye.")
                break

            if delta > timeout_sec:
                msg = "Waited %d seconds for container to finish. Giving up. " % delta
                elogger.error(msg)
                status = ChallengesConstants.STATUS_JOB_ERROR
                cr = ChallengeResults(status, msg, scores={})
                return cr

            time.sleep(5)

        try:
            cr = read_challenge_results(wd)
        except NoResultsFound as e:
            msg = f"""\
The result file is not found in working dir {wd}:

{e}

This usually means that the evaluator did not finish and some times that there was an import error.
Check the evaluator log to see what happened."""
            l = "\n".join("-" + f for f in list_all_files(wd))
            msg += f"\n\nList of all files:\n\n {l}"
            elogger.error(msg)
            status = ChallengesConstants.STATUS_JOB_ERROR
            cr = ChallengeResults(status, msg, scores={})

    except DockerComposeFail as e:
        msg = f"Error while running Docker Compose:\n\n{e}"
        elogger.error(msg)
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        cr = ChallengeResults(status, msg, scores={})

    except KeyboardInterrupt:
        msg = f"KeyboardInterrupt:\n{traceback.format_exc()}"
        elogger.error(msg)
        status = ChallengesConstants.STATUS_JOB_ABORTED
        cr = ChallengeResults(status, msg, scores={})

    except BaseException:
        msg = f"Uncaught exception while running Docker Compose:\n{traceback.format_exc()}"
        elogger.error(msg)
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        cr = ChallengeResults(status, msg, scores={})
    finally:
        teminate_workers()

    return cr


def list_all_files(wd: str) -> List[str]:
    return [os.path.join(dp, f) for dp, dn, fn in os.walk(wd) for f in fn]


def prepare_dir(wd, aws_config, steps2artefacts, use_ipfs: bool):
    if not os.path.exists(wd):
        os.makedirs(wd)
    # output for the sub
    challenge_solution_output_dir = os.path.join(wd, CHALLENGE_SOLUTION_OUTPUT_DIR)
    # the yaml with the scores
    challenge_results_dir = os.path.join(wd, CHALLENGE_RESULTS_DIR)
    # the results of the "preparation" step
    challenge_description_dir = os.path.join(wd, CHALLENGE_DESCRIPTION_DIR)
    challenge_evaluation_output_dir = os.path.join(wd, CHALLENGE_EVALUATION_OUTPUT_DIR)
    previous_steps_dir = os.path.join(wd, CHALLENGE_PREVIOUS_STEPS_DIR)

    for d in [
        challenge_solution_output_dir,
        challenge_results_dir,
        challenge_description_dir,
        challenge_evaluation_output_dir,
        previous_steps_dir,
    ]:
        if not os.path.exists(d):
            os.makedirs(d)

    download_artefacts(aws_config, steps2artefacts, previous_steps_dir, use_ipfs=use_ipfs)


def get_config(
    wd: str,
    fd: str,
    challenge_parameters_,
    solution_container: str,
    add_extra_environment: Dict[str, str],
    server_host: Optional[str],
    debug_volumes: Optional[str] = None,
    allow_host_network: bool = False,
    use_ipfs: bool = False,
):
    """
        server_host: reachable from other ips
    """
    UID = os.getuid()
    GID = os.getgid()
    USERNAME = getpass.getuser()
    dir_home_guest = f"/fake-home/{USERNAME}"
    dir_fake_home_host = os.path.join("/tmp", "fake-%s-home" % USERNAME)
    if not os.path.exists(dir_fake_home_host):
        os.makedirs(dir_fake_home_host)
    extra_environment = dict(username=USERNAME, uid=UID, USER=USERNAME, HOME=dir_home_guest)

    # Adding the submission container
    for service_def in challenge_parameters_.services.values():
        service_def.build = None

        if service_def.image == ChallengesConstants.SUBMISSION_CONTAINER_TAG:
            service_def.image = solution_container

    config = challenge_parameters_.as_dict()

    # do_trick = False
    for service in config["services"].values():
        image = service["image"]
        br = parse_complete_tag(image)
        # br.tag = None
        service["image"] = get_complete_tag(br)
        #
        # if do_trick:
        #     if image_digest:
        #         # If we have the image then we don't bother with pulling the tag
        #         try:
        #             c = client.images.get(image_digest)
        #         except NotFound:
        #             msg = 'Could not find the image for %s by digest %s; will need to pull.' % (
        #                 service['image'], image_digest)
        #             elogger.info(msg)
        #         else:
        #             msg = 'I already have the exact image for %s' % service['image']
        #             elogger.info(msg)
        #             #
        #             #
        #             if True:
        #
        #                 n = len('91bac885982d')
        #                 partial_id = image_digest.replace('sha256:', '')[:n]
        #                 service['image'] = partial_id
        #             else:
        #                 image = service['image']
        #                 # remove tag
        #                 if ':' in image:
        #                     image = image.split(':')[0]
        #                 service['image'] = image + '@' + image_digest

        service.pop("build", None)

        # This is not needed, because the tag is sufficient as it is generated anew.
        # We should perhaps check that we have the right image tag
        #
        # if image_digest is not None:
        #     service['image'] += '@' + image_digest

    # else:
    #     msg = 'Cannot find the tag %s' % SUBMISSION_CONTAINER_TAG
    #     elogger.warning(msg)
    #     # raise Exception(msg)

    def naturalize(image: str) -> str:
        if "localhost" in image:
            image2 = image.replace("localhost", server_host)
            elogger.info(f"replacing {image} -> {image2}")
            # raise Exception(image)
            return image2
        return image

    if server_host is not None:
        for service in config["services"].values():
            service["image"] = naturalize(service["image"])

    # adding extra environment variables:

    for service in config["services"].values():
        service["environment"].update(add_extra_environment)
        service["environment"].update(extra_environment)
        service["user"] = f"{UID}:{GID}"

    # add volumes
    # wd = os.path.join(os.getcwd(), wd)
    # fd = os.path.join(os.getcwd(), fd)
    # "/Volumes/work/DT/dt-env/dt-env-developer/src/aido-analyze/src/aido_analyze": {
    #             "bind": "/usr/local/lib/python3.8/dist-packages/aido_analyze",
    #             "mode": "ro"
    #         }
    volumes0 = {}
    volumes0[wd] = {"bind": "/challenges", "mode": "rw"}
    volumes0[fd] = {"bind": "/fifos", "mode": "rw"}
    volumes0[dir_fake_home_host] = {"bind": dir_home_guest, "mode": "rw"}

    if use_ipfs:
        if os.path.exists("/ipfs"):
            volumes0["ipfs"] = {"bind": "/ipfs", "mode": "ro"}
        else:
            msg = "/ipfs mount point not found"
            raise IPFSException(msg)

    if debug_volumes:
        volumes0.update(get_developer_volumes())
        # data = yaml.load(open(debug_volumes).read(), Loader=yaml.SafeLoader)
        # volumes.extend(data["volumes"])

    for service in config["services"].values():
        assert "volumes" not in service
        volumes = [f'{k}:{v["bind"]}:{v["mode"]}' for k, v in volumes0.items()]
        service["volumes"] = copy.deepcopy(volumes)

    # elogger.info('Now:\n%s' % safe_yaml_dump(config))

    NETWORK_NAME = "evaluation"
    networks_evaluator = dict(evaluation=dict(aliases=[NETWORK_NAME]))
    for service in config["services"].values():

        if allow_host_network:
            service["network_mode"] = "host"
        else:
            service["networks"] = copy.deepcopy(networks_evaluator)
    config["networks"] = dict(evaluation=None)
    config["volumes"] = dict(fifos=None)
    return config


def write_logs(wd, project, services):
    client = check_docker_environment()

    logdir = os.path.join(wd, "logs")
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    for service in services:
        try:
            container_id = get_id_for_service(wd, project, service)

            # cmd = ['ps', '-q', service]
            # try:
            #     o = run_docker(wd, project, cmd, get_output=True)
            #     container_id = o.strip()  # \n at the end
            # except DockerComposeFail:
            #     continue

            if not container_id:
                logs = 'Service "%s" was not started.' % service
                elogger.warning(logs)
            else:
                # elogger.info('Found container ID = %r' % container_id)

                for fname, options in [
                    ("combined", dict(stderr=True, stdout=True)),
                    ("stderr", dict(stderr=True, stdout=False)),
                    ("stdout", dict(stdout=True, stderr=False)),
                ]:

                    logs = logs_for_container(client, container_id, **options)

                    from ansi2html import Ansi2HTMLConverter

                    conv = Ansi2HTMLConverter()
                    html = conv.convert(logs)

                    logdir_service = os.path.join(logdir, service)
                    if not os.path.exists(logdir_service):
                        os.makedirs(logdir_service)
                    fn = os.path.join(logdir_service, "%s.log" % fname)
                    write_ustring_to_utf8_file(logs, fn)

                    fn = os.path.join(logdir_service, "%s.html" % fname)
                    write_ustring_to_utf8_file(html, fn)
        except:
            elogger.error(traceback.format_exc())


class Tee:
    def __init__(self, name, f):
        self.file = open(name, "w")
        self.name = name
        self.original = f

    def close(self):
        if hasattr(self, "file"):
            if self.file is not None:
                self.file.close()
                self.file = None

    def __del__(self):
        self.close()

    def write(self, data: str):
        # if isinstance(data, str):
        #     data = data.encode('utf-8')
        self.file.write(data)
        self.file.flush()
        # data_s = data.decode('utf-8')
        self.original.write(data)
        self.original.flush()

    def flush(self):
        self.file.flush()
        self.original.flush()

    def fileno(self):
        return self.file.fileno()

    def getvalue(self):
        with open(self.name) as f:
            return f.read()


def run_docker(cwd: str, project: str, cmd0: List[str], get_output: bool = False) -> bytes:
    """ raises DockerComposeFail """
    cmd0 = ["docker-compose", "-p", project] + cmd0
    # elogger.info('Running:\n\t%s' % " ".join(cmd0) + '\n\n in %s' % cwd)
    elogger.debug(cwd=cwd, command=" ".join(cmd0))

    d = tempfile.mkdtemp()

    fn1 = os.path.join(d, "docker-stdout.txt")
    fn2 = os.path.join(d, "docker-stderr.txt")
    # elogger.debug('Saving stdout to %s' % fn1)

    tee_stdout = Tee(fn1, sys.stdout)
    tee_stderr = Tee(fn2, sys.stderr)

    try:
        if get_output:
            return subprocess.check_output(cmd0, cwd=cwd, stderr=sys.stderr)
        else:
            # noinspection PyTypeChecker
            # subprocess.check_call(cmd0, cwd=cwd, stdout=tee_stdout, stderr=tee_stderr)
            subprocess.check_call(cmd0, cwd=cwd, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:
        msg = "Could not run command"
        raise DockerComposeFail(
            msg, cmd=cmd0, stdout=tee_stdout.getvalue(), sderr=tee_stderr.getvalue(), e=str(e)
        ) from e
    finally:
        try:
            os.unlink(fn1)
            os.unlink(fn2)
        except:
            pass
        pass


def upload_files(
    wd: str, aws_config, ignore_patterns=(".DS_Store",), copy_to_machine_cache: bool = True,
):
    """
        wd: directory to search for
    """
    toupload = get_files_to_upload(wd, ignore_patterns=ignore_patterns)
    elogger.info(f"{len(toupload)} files to upload.")
    if not aws_config:
        msg = "Not uploading artifacts because AWS config not passed."
        elogger.info(msg)
        uploaded = only_copy_to_cache(toupload)
    else:
        uploaded = upload(aws_config, toupload, copy_to_machine_cache=copy_to_machine_cache)

    return uploaded


@timeout_decorator.timeout(60)
def try_to_get_hash(client, qm):
    res = client.file_ls(qm)

    elogger.info(f"{qm} -> {res}")


class CouldNotDownloadAll(Exception):
    pass


def download_artefacts(aws_config, steps2artefacts, wd, use_ipfs: bool):
    if use_ipfs:
        import ipfsapi

        client = ipfsapi.connect("127.0.0.1", 5001)
        elogger.info("connecting to IPFS peers")
        peers = [
            "/dns4/ipfs.duckietown.org/tcp/4001/ipfs/QmPyoL4ZwaTYtGsvFG8A5fG85tQH5sCHWtexkNVjqa52iK",
            "/ip4/129.132.0.37/tcp/4001/ipfs/QmW5P8PZhGYGoyGzAGZNKNTKrvbg8m7Wv4QF4o2ghYmuf9",
        ]
        peers = []
        for peer in peers:
            elogger.info(f"connecting to {peer}")
            res = client.swarm_connect(peer)
            elogger.debug(str(res))

    else:
        client = None
    for step_name, artefacts in steps2artefacts.items():
        step_dir = os.path.join(wd, step_name)
        os.makedirs(step_dir)
        write_ustring_to_utf8_file("touch", os.path.join(step_dir, "touch"))

        for rpath, data in artefacts.items():
            # elogger.debug(data)
            fn = os.path.join(step_dir, rpath)
            dn = os.path.dirname(fn)
            if not os.path.exists(dn):
                os.makedirs(dn)

            sha256hex = data["sha256hex"]
            size = data["size"]
            storage = data["storage"]

            if data["mime_type"] == "ipfs":
                if not use_ipfs:
                    msg = "Need IPFS for this submission"
                    continue
                else:

                    elogger.info(f"getting {sha256hex} ")

                    try:
                        try_to_get_hash(client, sha256hex)
                    except:
                        msg = f"Could not get IPFS hash {sha256hex}"
                        elogger.error(msg)
                        raise IPFSException(msg)
                    # res = client.file_ls(sha256hex)

                    # elogger.info(f'{sha256hex} -> {res}')
                    #
                    # client.get(sha256hex)
                    # os.rename(sha256hex, fn)

                    fn2 = f"/ipfs/{sha256hex}"
                    #
                    # if not os.path.exists(fn2):
                    #     msg = f'Cannot stat the file {fn2}'
                    #     raise Exception(msg)
                    # else:
                    #     elogger.info(f'list ipfs files: {os.listdir(fn2)}')
                    #
                    # elogger.info(f'list fn files: {os.listdir(fn)}')

                    if os.path.exists(fn):
                        os.unlink(fn)
                    elogger.info(f"Linking {fn} to {fn2}")
                    os.symlink(fn2, fn)

                    assert os.path.lexists(fn2)
                    assert os.path.exists(fn2)

                    continue

            try:
                get_file_from_cache(fn, sha256hex)
                elogger.info("cache   %7s   %s" % (friendly_size(size), rpath))
            except KeyError:

                # no local
                if "s3" in storage:
                    if not aws_config:
                        msg = "I cannot download from S3 because credentials not given."
                        raise CouldNotDownloadAll(msg)
                    else:
                        s3ob = storage["s3"]
                        bucket_name = s3ob["bucket_name"]
                        object_key = s3ob["object_key"]

                        elogger.info("AWS     %7s   %s" % (friendly_size(size), rpath))
                        get_object(aws_config, bucket_name, object_key, fn)
                        copy_to_cache(fn, sha256hex)

                    size_now = os.stat(fn).st_size
                    if size_now != size:
                        msg = "Corrupt cache or download for %s at %s." % (data, fn)
                        raise ValueError(msg)
                else:
                    msg = "Not in cache and no way to download"
                    raise CouldNotDownloadAll(msg)


def try_s3(aws_config):
    bucket_name = aws_config["bucket_name"]
    aws_access_key_id = aws_config["aws_access_key_id"]
    aws_secret_access_key = aws_config["aws_secret_access_key"]
    aws_root_path = aws_config["path"]
    import boto3

    s3 = boto3.resource(
        "s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
    )

    s = b"initial data"
    data = BytesIO(s)
    elogger.debug("trying bucket connection")
    s3_object = s3.Object(bucket_name, os.path.join(aws_root_path, "initial.txt"))
    s3_object.upload_fileobj(data)
    elogger.debug("uploaded")


def get_object(aws_config, bucket_name, object_key, fn):
    aws_access_key_id = aws_config["aws_access_key_id"]
    aws_secret_access_key = aws_config["aws_secret_access_key"]
    import boto3

    s3 = boto3.resource(
        "s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
    )
    aws_object = s3.Object(bucket_name, object_key)
    aws_object.download_file(fn)


def get_files_to_upload(path, ignore_patterns=()):
    def to_ignore(rpath_: str):

        if "fifos" in rpath_:
            elogger.debug(f"ignoring fifo path: {rpath_}")
            return True
        if rpath_.startswith(CHALLENGE_TMP_SUBDIR):
            elogger.debug(f"ignoring tmp path: {rpath_}")
            return True
        # if rpath_.startswith('tmp'):
        #     elogger.debug(f'ignore tmp path: {rpath_}')
        #     return True

        if CHALLENGE_PREVIOUS_STEPS_DIR in rpath_:
            elogger.debug(f" ignoring previous: {rpath_}")

            return True

        for p in ignore_patterns:
            if os.path.basename(rpath_) == p:
                elogger.debug(f" ignoring pattern {p}: {rpath_}")
                return True
        # elogger.debug(f"including {rpath_}")
        return False

    toupload = {}
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            rpath = os.path.join(os.path.relpath(dirpath, path), f)

            if rpath.startswith("./"):
                rpath = rpath[2:]

            if to_ignore(rpath):
                elogger.debug("ignoring %s" % rpath)
                continue
            else:
                elogger.debug("  adding %s" % rpath)

            toupload[rpath] = os.path.join(dirpath, f)

    return toupload


def logs_for_container(client, container_id, stdout, stderr) -> str:
    container = client.containers.get(container_id)
    logs = container.logs(stdout=stdout, stderr=stderr, timestamps=True)
    return logs.decode("utf-8")


def only_copy_to_cache(toupload):
    uploaded = []
    for rpath, realfile in toupload.items():
        sha256hex = compute_sha256hex(realfile)
        copy_to_cache(realfile, sha256hex)
        size = os.stat(realfile).st_size
        mime_type = guess_mime_type(realfile)
        storage = {}
        uploaded.append(
            dict(size=size, mime_type=mime_type, rpath=rpath, sha256hex=sha256hex, storage=storage,)
        )
    return uploaded


def guess_mime_type(filename):
    mime_type, _encoding = mimetypes.guess_type(filename)

    if mime_type is None:
        if filename.endswith(".yaml"):
            mime_type = "text/yaml"
        else:
            mime_type = "binary/octet-stream"
    return mime_type


def upload(aws_config, toupload, copy_to_machine_cache=True):
    import boto3
    from botocore.exceptions import ClientError

    bucket_name = aws_config["bucket_name"]
    aws_access_key_id = aws_config["aws_access_key_id"]
    aws_secret_access_key = aws_config["aws_secret_access_key"]
    # aws_root_path = aws_config['path']
    aws_path_by_value = aws_config["path_by_value"]

    s3 = boto3.resource(
        "s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
    )

    uploaded = []
    for rpath, realfile in toupload.items():

        sha256hex = compute_sha256hex(realfile)
        if copy_to_machine_cache:
            copy_to_cache(realfile, sha256hex)

        # path_by_value
        object_key = os.path.join(aws_path_by_value, "sha256", sha256hex)

        # object_key = os.path.join(aws_root_path, rpath)

        size = os.stat(realfile).st_size
        mime_type = guess_mime_type(realfile)

        aws_object = s3.Object(bucket_name, object_key)
        try:
            aws_object.load()
            # elogger.info('Object %s already exists' % rpath)
            status = "known"
            elogger.info("%15s %8s  %s" % (status, friendly_size(size), rpath))

        except ClientError as e:
            not_found = e.response["Error"]["Code"] == "404"
            if not_found:
                status = "uploading"
                elogger.info("%15s %8s  %s" % (status, friendly_size(size), rpath))
                aws_object.upload_file(realfile, ExtraArgs={"ContentType": mime_type})

            else:
                raise
        url = "http://%s.s3.amazonaws.com/%s" % (bucket_name, object_key)
        storage = dict(s3=dict(object_key=object_key, bucket_name=bucket_name, url=url))
        uploaded.append(
            dict(size=size, mime_type=mime_type, rpath=rpath, sha256hex=sha256hex, storage=storage,)
        )

    return uploaded


def object_exists(s3, bucket, key):
    from botocore.exceptions import ClientError

    try:
        h = s3.head_object(Bucket=bucket, Key=key)
        # print h
    except ClientError as e:
        return int(e.response["Error"]["Code"]) != 404
    return True


def compute_sha256hex(filename) -> str:
    cmd = ["shasum", "-a", "256", filename]
    res: bytes = subprocess.check_output(cmd)
    res2 = res.decode("utf-8")
    tokens = res2.split()
    h = tokens[0]
    assert len(h) == len("08c1fe03d3a6ef7dbfaccc04613ca561b11b5fd7e9d66b643436eb611dfba348")
    return h


def create_index_files(wd, job_id):
    for root, dirnames, filenames in os.walk(wd, followlinks=True):
        print(root, dirnames, filenames)
        index = os.path.join(root, "index.html")
        if not os.path.exists(index):
            d = create_index(root, dirnames, filenames, job_id)
            write_ustring_to_utf8_file(d, index)


def create_index(root, dirnames, filenames, job_id):
    s = "<html><head></head><body>\n"

    url = DEFAULT_DTSERVER + "/humans/jobs/%s" % job_id
    s += '<p>These are the output for <a href="%s">Job %s</a>' % (url, job_id)
    s += "<table>"

    for d in dirnames:
        s += '\n<tr><td></td><td><a href="%s">%s/</td></tr>' % (d, d)

    for f in filenames:
        size = os.stat(os.path.join(root, f)).st_size
        s += '\n<tr><td>%.3f MB</td><td><a href="%s">%s</td></tr>' % (size / (1024 * 1024.0), f, f,)

    s += "\n</table>"
    s += "\n</body></head>"
    return s
