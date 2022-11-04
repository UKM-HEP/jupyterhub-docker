#!/bin/bash

docker rm -vf $(docker ps -aq)
docker network prune
docker volume rm $(docker volume ls -q)
docker rmi $(docker images | grep "^<none>" | awk "{print $3}" | tr -s ' ' | cut -d ' ' -f 3)
