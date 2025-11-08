#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

source ${ROOT_DIR}/bin/setup.sh

${ROOT_DIR}/bin/fmt.sh

if [ "$1" == "fix" ];
then
	${ROOT_DIR}/bin/lint.sh --fix
fi

${ROOT_DIR}/bin/type_check.sh

if [ "$1" != "nodocker" ];
then
	${ROOT_DIR}/bin/docker.sh
fi

