#!/usr/bin/env bash

source ./scripts/constant.sh

# sudo add-apt-repository ppa:certbot/certbot > /dev/null
sudo apt install certbot python3-certbot-nginx -y 
echo "Adding cert for $websiteUrl " 
echo "sudo certbot --nginx -d $websiteUrl -m $email --agree-tos -n"
sudo certbot --nginx -d $websiteUrl -m $email --agree-tos -n