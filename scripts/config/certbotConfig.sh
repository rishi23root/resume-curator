
# sudo add-apt-repository ppa:certbot/certbot > /dev/null
sudo apt install certbot python3-certbot-nginx -y > /dev/null 
sudo certbot --nginx -d $websiteUrl -m $email --agree-tos --non-interactive