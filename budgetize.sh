#!/bin/sh
cd "$(dirname "$0")"

windows_mnt_pattern='s/\mnt//'  # deal with windows docker volume mounting
lib_dir="$(pwd | sed $windows_mnt_pattern)"
config_dir="$(cd $(dirname $1); pwd | sed $windows_mnt_pattern)"
config_file="$(basename "$1")"

docker run -it --rm \
  -v $lib_dir:/financier \
  -v $config_dir:/config \
  -w /financier fdm1/base_python_dev:python3 \
  python3 cmd.py -c /config/$config_file "${@:2}"
