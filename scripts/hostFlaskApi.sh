#!/usr/bin/env bash
source scripts/constant.sh

# give ufw access to 
sudo ufw --force enable

# check if gunicorn is installed
if ! [ -x "$(command -v env/bin/gunicorn)" ]; then
    source $(pwd)/env/bin/activate
    echo 'Error: gunicorn is not installed.' >&2
    sudo env/bin/pip install gunicorn 
    echo 'Done! ✅'
    deactivate
    echo ""
fi

# # Make a systemd service file if not exists make full service file setup
cleanUpService
if [ ! -f $serviceFilePath ]; then
    ./scripts/config/serviceConfig.sh 
    sudo systemctl daemon-reload
    sudo systemctl start $serviceName
    sudo systemctl enable $serviceName
fi

# setup nginx
cleanUpNginx
if [ ! -f $nginxFilePath ]; then
    ./scripts/config/nginxConfig.sh
    sudo ln -s $nginxFilePath /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    sudo ufw delete allow 5000
    sudo ufw allow 'Nginx Full'
    echo "Done ✅"
    echo ""
fi


chmod +x ./scripts/config/certbotConfig.sh

# install cert bot and get ssl certificate
# if ssl certificate is not present
if [ ! -f /etc/letsencrypt/live/$websiteUrl/fullchain.pem ]; then
    ./scripts/config/certbotConfig.sh
fi