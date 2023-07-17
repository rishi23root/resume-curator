
sudo add-apt-repository ppa:certbot/certbot > dev/null
sudo apt install python-certbot-nginx > dev/null 
sudo certbot --nginx -d $websiteUrl -m $email --agree-tos --non-interactive