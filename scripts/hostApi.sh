#!/usr/bin/env bash

# check if gunicorn is installed
if ! [ -x "$(command -v gunicorn)" ]; then
    echo 'Error: gunicorn is not installed.' >&2
    sudo apt-get install gunicorn > /dev/null
    echo 'Done! ✅'
fi

# take port number from command line argument make sure it is not empty default to 5000
port=${1:-5000}
# get no of cores
cores=$(nproc --all)
# calculate no of workers
workers=$(( $cores * 2 + 1 ))
# print port and workers
echo "port: $port"
echo "workers: $workers"

# run gunicorn with 4 workers
gunicorn wsgi:app --log-file - --bind 0.0.0.0:$port --workers=$workers --timeout 120 --reload