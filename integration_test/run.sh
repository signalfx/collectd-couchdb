#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

printf "Running Integration Tests against python2.7\n"
docker-compose run --rm test
status=$?

docker-compose down

printf $status

if [ "$status" != "0" ]; then exit $status; fi

printf "\n Running Integration Tests against python2.6\n"
docker-compose run --rm test26
status=$?

docker-compose down

printf $status

exit $status