#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

source bin/setup.sh

pushd src/python/joborm > /dev/null
mypy --explicit-package-bases *.py
popd > /dev/null
