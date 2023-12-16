#!/usr/bin/env bash

serviceName="buildyourresume"
serviceFilePath="/etc/systemd/system/$serviceName.service"
nginxFilePath="/etc/nginx/sites-available/$serviceName"
websiteUrl="api.buildyourresume.online"
port=5000
email="rishabhjainfinal@gmail.com"
virtualEnv='venv'




cleanUpService(){
    # remove the service file
    sudo rm $serviceFilePath
    # remove the socket file
    # sudo rm $(pwd)/flask-app.sock
    sudo systemctl daemon-reload
    sudo systemctl stop $serviceName
    sudo systemctl disable $serviceName
    sudo systemctl daemon-reload
}

cleanUpNginx(){
    # remove the nginx file
    sudo rm $nginxFilePath
    # remove the nginx link
    sudo rm /etc/nginx/sites-enabled/$serviceName
    sudo systemctl daemon-reload
    sudo systemctl stop nginx
    sudo systemctl disable nginx
    sudo systemctl daemon-reload
}

cleanUpCertbot(){
    # if certbot is installed
    if [ -x "$(command -v certbot)" ]; then
        echo "Removing certbot"
        sudo apt-get remove certbot
        echo ""
    fi
}


# just old code 
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
