#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

export PYTHONPATH=${ROOT_DIR}/src/python/joborm

${ROOT_DIR}/venv/bin/uvicorn --reload web.serve:app
