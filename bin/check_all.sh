#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

source bin/setup.sh

./bin/fmt.sh
./bin/lint.sh $1
./bin/type_check.sh
./bin/docker.sh
