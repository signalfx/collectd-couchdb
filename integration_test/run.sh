#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

printf "Running Integration Tests"
docker-compose run test
status=$?

docker-compose down

printf $status
exit $status