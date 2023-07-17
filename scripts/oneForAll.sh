source ./scripts/constant.sh
# make everything executable in the scripts folder
chmod +x ./scripts/*


# Run the setup script
# ./scripts/setup.sh

# if nginx is not installed install it
if ! [ -x "$(command -v nginx)" ]; then
    echo 'Error: nginx is not installed.' >&2
    echo 'Installing nginx ..' 
    sudo apt-get install nginx -y > /dev/null
    echo 'Done! ✅' 
fi


# get new changes from git
git pull

# Run the server
./scripts/hostFlaskApi.sh

echo $websiteUrl