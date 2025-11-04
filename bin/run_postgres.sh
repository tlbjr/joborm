#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

mkdir -p ${ROOT_DIR}/pgvol

docker run -e POSTGRES_PASSWORD=postgres -v ${ROOT_DIR}/pgvol:/var/lib/postgresql -p 5432:5432 -it postgres:18
