source ./scripts/constant.sh

echo "Installing certbot and getting ssl certificate"
    

# if certbot is not installed
if ! [ -x "$(command -v certbot)" ]; then
    echo "Installing certbot"
    sudo apt install certbot python3-certbot-nginx -y 
fi

echo "Adding cert for $websiteUrl " 
    echo "sudo certbot --nginx -d $websiteUrl -m $email --agree-tos -n"
sudo certbot --nginx -d $websiteUrl -m $email --agree-tos -n
echo "Done ✅"