#!/usr/bin/env bash

# check if gunicorn is installed
if ! [ -x "$(command -v gunicorn)" ]; then
    echo 'Error: gunicorn is not installed.' >&2
    pip install install gunicorn > /dev/null
    echo 'Done! ✅'
fi


gunicornCall(){
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
}
cleanUp(){
    # remove the service file
    sudo rm $serviceFilePath
    # remove the socket file
    # sudo rm $(pwd)/flask-app.sock
}


serviceName="buildyourresume"
serviceFilePath="/etc/systemd/system/$serviceName.service"

cleanUp
# Make a systemd service file if not exists make full service file setup
if [ ! -f $serviceFilePath ]; then
    ./scripts/serverConfig.sh $serviceFilePath
    sudo systemctl daemon-reload
fi

# sudo systemctl start $serviceName
# sudo systemctl enable $serviceName

# Reload systemd 