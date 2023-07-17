#!/usr/bin/env bash

source ./scripts/constant.sh

# use proxy insted of unix socket


echo "Setting up nginx file config"
echo ""
# creating the file 
echo "Adding into nginx avilable sites... $nginxFilePath"
sudo touch $nginxFilePath
echo "--------------------------------------------------------------------------"
# sudo cat $serviceFilePath << END
sudo tee $nginxFilePath << END
server {
    listen 80;
    server_name $websiteUrl;
    
    location / {
        proxy_pass http://localhost:$port;
        include /etc/nginx/proxy_params;
        proxy_redirect off;
    }
}
END
echo "--------------------------------------------------------------------------"
echo ""
echo "nginx avilable site file setup complete! ✅" $nginxFilePath