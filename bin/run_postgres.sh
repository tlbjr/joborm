#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

mkdir -p ${ROOT_DIR}/pgvol

if [ "$1" == "clear" ];
then
	docker container rm joborm-postgres
	rm -r ${ROOT_DIR}/pgvol
fi

docker run -e POSTGRES_DB=joborm -e POSTGRES_PASSWORD=postgres -v ${ROOT_DIR}/pgvol:/var/lib/postgresql -p 5432:5432 --name joborm-postgres -it postgres:18

