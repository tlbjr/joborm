#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

export PYTHONPATH=${ROOT_DIR}/src/python/joborm

if [ "$1" == "alembic" ];
then
	echo "Waiting for pg"
	sleep 5
	${ROOT_DIR}/bin/run_alembic.sh
fi

${ROOT_DIR}/venv/bin/uvicorn --reload web.serve:app
