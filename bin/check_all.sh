#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

source ${ROOT_DIR}/bin/setup.sh

${ROOT_DIR}/bin/fmt.sh
${ROOT_DIR}/bin/lint.sh $1
${ROOT_DIR}/bin/type_check.sh
${ROOT_DIR}/bin/docker.sh
