#!/bin/bash

docker rm -vf $(docker ps -aq)
docker network prune
docker volume rm $(docker volume ls -q)
