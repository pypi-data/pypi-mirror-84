ARG AIDO_REGISTRY
FROM  ${AIDO_REGISTRY}/ubuntu:20.04
#FROM ${AIDO_REGISTRY}/duckietown/aido-base-python3:daffy-amd64

ARG PIP_INDEX_URL
ENV PIP_INDEX_URL=${PIP_INDEX_URL}


RUN apt-get update \
    && apt-get install -y \
    curl \
    git \
    docker.io \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN curl -f -L https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m) \
    -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose


RUN usermod -G docker -a root

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONIOENCODING=utf8

WORKDIR /project


ARG REFRESHED_REQS=5

RUN pip3 install -U "pip>=20.2"
COPY requirements.* ./
RUN cat requirements.* > .requirements.txt
RUN  pip3 install --use-feature=2020-resolver -r .requirements.txt


COPY  . .

RUN pip3 install --no-deps .
RUN pip3 list
RUN pipdeptree
RUN dt-challenges-evaluator --version

CMD ["dt-challenges-evaluator"]
