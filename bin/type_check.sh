#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=${SCRIPT_DIR}/..

source ${ROOT_DIR}/bin/setup.sh

pushd ${ROOT_DIR}/src/python/joborm > /dev/null
mypy --explicit-package-bases .
popd > /dev/null
