#!/usr/bin/env bash

source ./scripts/constant.sh
# make everything executable in the scripts folder
chmod +x ./scripts/*


# get new changes from git
git pull

# Run the setup script
./scripts/setup.sh

# if nginx is not installed install it
if ! [ -x "$(command -v nginx)" ]; then
    echo '🚫 Error: nginx is not installed.' >&2
    echo 'Installing nginx ..' 
    sudo apt-get install nginx -y 2>/dev/tty >/dev/null
    echo 'Done! ✅' 
fi


# Run the server
./scripts/hostFlaskApi.sh

echo http://$websiteUrl

# Run the checks 
echo "Checking if gunicorn is running"
sudo systemctl status $serviceName | grep active

echo "Checking if nginx is running"
sudo systemctl status nginx | grep active


# generate output files 
echo "Generating output templates pdf files"
python3 main.py > /dev/null
echo 'Done! ✅' 