#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

PYTHON=python3
if [ "`which python3`" == "" ];
then
    PYTHON=python
fi

# TODO Move to pyproject.toml, uv bootstrap, and uv sync
if [ ! -e ${ROOT_DIR}/venv ];
then
    echo "Creating virtual environment"
    $PYTHON -m venv venv
    echo "Installing requirements"
    ${ROOT_DIR}/venv/bin/pip install -r src/python/joborm/requirements.txt
fi

source ${ROOT_DIR}/venv/bin/activate

