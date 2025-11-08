#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

source ${ROOT_DIR}/bin/setup.sh

pushd ${ROOT_DIR}/src/python/joborm > /dev/null

if [ "$1" != "" ];
then

	alembic "$@"
else
	alembic upgrade head
fi


