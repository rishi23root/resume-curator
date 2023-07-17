#!/usr/bin/env bash

source ./scripts/constant.sh

# sudo chmod 777 $(pwd)/$sockFileName


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
        include proxy_params;
        proxy_pass http://unix:$(pwd)/$sockFileName;
    }
}
END
echo "--------------------------------------------------------------------------"
echo ""
echo "nginx avilable site file setup complete! ✅" $nginxFilePath



# sudo chmod 777 $(pwd)/$sockFileName