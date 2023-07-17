#!/usr/bin/env bash
source ./scripts/constant.sh


cleanUpNginx
cleanUpService
cleanUpCertbot


echo "Checking if gunicorn is running"
sudo systemctl status $serviceName | grep active

echo "Checking if nginx is running"
sudo systemctl status nginx | grep active