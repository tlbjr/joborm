#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

mkdir -p ${ROOT_DIR}/pgvol

if [ "$1" == "clear" ];
then
    echo "Clearing volume"
    docker container rm joborm-postgres
    rm -r ${ROOT_DIR}/pgvol
fi

if [ `which docker | wc -l` == "0" ];
then
    echo "Docker command not found. Waiting to quit."
    ${ROOT_DIR}/bin/showwait.sh 10
else
    if [ `docker container ls --all | grep joborm-postgres | wc -l` != "0" ];
    then
        echo "Starting existing container"
        docker container start -ai joborm-postgres
    else
        echo "Running new container"
        docker run -e POSTGRES_DB=joborm -e POSTGRES_PASSWORD=postgres -v ${ROOT_DIR}/pgvol:/var/lib/postgresql -p 5432:5432 --name joborm-postgres -it postgres:18
    fi
fi

