#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

export PYTHONPATH=${ROOT_DIR}/src/python/joborm

if [ "$1" == "alembic" ];
then
    echo "Waiting for pg"
    timeout 30 sh -c 'until nc -z $0 $1; do sleep 1; done' localhost 5432
    ${ROOT_DIR}/bin/run_alembic.sh
fi

${ROOT_DIR}/venv/bin/uvicorn --reload web.serve:app
# ~2.5x more throughput per seconds (1,200 => 4,000)
#${ROOT_DIR}/venv/bin/python -m socketify web.serve:app
