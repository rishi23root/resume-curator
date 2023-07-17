#!/usr/bin/env bash
source ./scripts/constant.sh


# get no of cores for gunicorn workers
cores=$(nproc --all)
# calculate no of workers
workers=$(( $cores * 2 + 1 ))
# echo "workers: $workers"

# write to the file
echo "Setting up systemd service file config"
echo ""
# creating the file 
echo "Creating systemd service file... $serviceFilePath"
sudo touch $serviceFilePath
echo "--------------------------------------------------------------------------"
# sudo cat $serviceFilePath << END
sudo tee $serviceFilePath << END
[Unit]
Description=Gunicorn instance to serve buildyourresume 
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/env/bin"
ExecStart=$(pwd)/env/bin/gunicorn --workers $workers --bind unix:$sockFileName -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
END
echo "--------------------------------------------------------------------------"
echo ""
echo "systemd service file setup complete! ✅" $serviceFilePath

