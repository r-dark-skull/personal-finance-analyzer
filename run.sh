#! /bin/bash

docker-compose stop
docker-compose rm -f
docker-compose build
docker image prune -f
docker-compose up -d
