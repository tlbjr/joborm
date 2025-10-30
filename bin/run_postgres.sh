#!/usr/bin/env bash
docker run -e POSTGRES_PASSWORD=postgres -p 5432:5432 -it postgres:18
