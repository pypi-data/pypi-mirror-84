
build:
	dts build_utils aido-container-build


push: build
	dts build_utils aido-container-push



#AIDO_REGISTRY ?= docker.io
#PIP_INDEX_URL ?= https://pypi.org/simple
#PIP_TRUSTED_HOST ?=
#
#
#build_options = \
#	--build-arg PIP_INDEX_URL=$(PIP_INDEX_URL) \
#	--build-arg AIDO_REGISTRY=$(AIDO_REGISTRY) \
#	$(shell dt-labels)
#
#branch=$(shell git rev-parse --abbrev-ref HEAD)
#branch=daffy
#name=$(AIDO_REGISTRY)/duckietown/dt-challenges-evaluator:$(branch)
#name_rpi=$(AIDO_REGISTRY)/duckietown/rpi-dt-challenges-evaluator:$(branch)
#
#all:
#
#bump-upload:
#	$(MAKE) bump
#	$(MAKE) upload
#
bump: # v2
	bumpversion patch
	git push --tags
	git push

upload: # v3
	dts build_utils check-not-dirty
	dts build_utils check-tagged
	dt-check-need-upload --package duckietown-challenges-runner-daffy make upload-do
#
upload-do:
	rm -f dist/*
	rm -rf src/*.egg-info
	python3 setup.py sdist
	twine upload --skip-existing --verbose dist/*
#
#
#
#update-reqs:
#	pur --index-url $(PIP_INDEX_URL) -r requirements.txt -f -m '*' -o requirements.resolved
#	dt-update-reqs requirements.resolved
#
#build: update-reqs
#	docker build --pull -t $(name)  $(build_options) .
#
#build-no-cache: update-reqs
#	docker build --pull -t $(name)  $(build_options) --no-cache .
#
#push: build
#	dts build_utils push $(name)
#
#
#
#build-arm:
#	docker build --pull -t $(name_rpi) -f Dockerfile.arm  $(build_opts) .
#
#build-arm-no-cache:
#	docker build --pull -t $(name_rpi) -f Dockerfile.arm  $(build_opts) --no-cache  .
#
#push-arm:
#	dts build_utils push $(name_rpi)
#
#
#
#tests-clean:
#	rm -rf out-comptests
#
#tests:
#	comptests --nonose duckietown_challenges_runner_tests
#
#shell18:
#	docker run  -it --rm --workdir /project -v $(PWD):/project  python:3 /bin/bash
#
#black:
#	black -l 110 src setup.py
