#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

source ${ROOT_DIR}/bin/setup.sh

export PYTHONPATH=${ROOT_DIR}/src/python/joborm

python src/python/joborm/tests/tests.py
pytest ${ROOT_DIR}/src/python/joborm/tests/tests.py
