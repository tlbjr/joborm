#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

source bin/setup.sh

export PYTHONPATH=$ROOT_DIR/src/python/joborm:$PATH

tmux new-session \; split-window -h \; split-window -h ${ROOT_DIR}/bin/run_api.sh alembic \; split-window -v ${ROOT_DIR}/bin/run_postgres.sh \; attach
