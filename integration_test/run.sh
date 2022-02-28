#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

printf "Running Integration Tests against python2.7\n"
docker-compose run --rm test
status=$?

docker-compose down

printf $status

exit $status