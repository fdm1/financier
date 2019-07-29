build_test:
	docker build -t financier_test -f Dockerfile.test .

test: build_test
	docker run --rm financier_test

pylint: build_test
	docker run --rm financier_test ./ci/pylint.sh

lint: pylint

interactive: build_test
	docker run --rm -it -v $(pwd):/financier financier_test bash

build:
	docker build -t financier .

start: build
	docker run --rm -p 5000:5000 financier

