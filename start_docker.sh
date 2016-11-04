#!/bin/sh
cd "$(dirname "$0")"

if [[ "$(docker ps -qa -f name=financier 2> /dev/null)" == "" ]]; then
    echo 'starting financier container'
    docker run -it --name financier -v $(pwd):/financier -p 5000:5000 -w /financier fdm1/base_python_dev:python3
  else
    echo 'starting/attaching to financier container'
    docker start financier
    docker attach financier
  fi

