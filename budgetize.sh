#!/bin/sh
cd "$(dirname "$0")"


config_dir="$(dirname "$1")"
config_file="$(basename "$1")"

docker run -it --rm \
  -v $(pwd):/financier \
  -v $config_dir:/config \
  -w /financier fdm1/base_python_dev:python3 \
  python3 cmd.py -c /config/$config_file "${@:2}"
