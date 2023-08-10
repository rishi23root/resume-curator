#!/usr/bin/env bash

# install pdflatex tlmgr  
# respect to https://github.com/indrjo/minimal-texlive-installer/tree/main for the installer, it just works 
# check if pdflatx, tlmgr and texliveonfly is installed
# if not install it
# check if texlive path is added to path
# if not add it
if [ -d "$HOME/texlive/2023/bin/x86_64-linux" ]; then
    source $HOME/.bashrc 
else
    echo "texlive is not installed. 🚫"
fi

sudo chmod +x ./builder/*

if command -v pdflatex 2>/dev/tty >/dev/null && command -v tlmgr 2>/dev/tty >/dev/null && command -v texliveonfly 2>/dev/tty >/dev/null; then
    echo "All required packages are installed. ✅"
else
    echo "Installing texlive and texliveonfly..."
    chmod +x ./scripts/install-texlive
    ./scripts/install-texlive --scheme=small

    texlivePath=$HOME/texlive/2023/bin/x86_64-linux
    # make this path executable for every user
    chmod -R 755 $texlivePath
    # if user on zsh make this path available to zsh
    [ -f $HOME/.zshrc ] && echo "Path Also added to your zshrc 😎" && echo "export PATH=$texlivePath:$PATH" >> $HOME/.zshrc 

    # to install missing packages on the fly
    echo "Installing texliveonfly..."
    $texlivePath/tlmgr install texliveonfly 2>/dev/tty >/dev/null
    echo "Done! ✅"
    
    echo Installed here: $texlivePath
fi




# install pip if not installed
if ! [ -x "$(command -v pip)" ]; then
    echo '🚫 Error: pip is not installed.' 
    echo 'Installing pip ..' 
    sudo apt-get install python3-pip -y 2>/dev/tty >/dev/null
    echo 'Done! ✅' 
fi

update_pip() {
    echo "Updating pip..."
    sudo pip install --upgrade pip 2>/dev/tty >/dev/null
    echo "Done! ✅\n"
}

update_pip

# set up python virtual environment
echo "Setting up python virtual environment..."
echo ""
# check if venv exists
if [ -d "env" ]; then
    echo "venv exists. 😎"
    source ./env/bin/activate
else
    echo "venv does not exist. 🚫"
    echo "Creating env..."
    sudo apt install python3.10-venv -y 2>/dev/tty >/dev/null
    sudo python3 -m venv env 2>/dev/tty >/dev/null
    source ./env/bin/activate
    echo "Done! ✅"
fi

# check if requirements.txt exists and install requirements
if [ -f "requirements.txt" ]; then
    echo "requirements.txt found. 😎 installing requirements..."
    sudo ./env/bin/pip install -r requirements.txt 2>/dev/tty >/dev/null
    echo "Done! ✅"
else
    echo "requirements.txt not found. 🚫"
    exit 1
fi

echo "Python virtual environment setup complete! ✅"
deactivate
echo ""


# make all files in scripts executable
echo "Making all files in scripts executable..."
chmod +x ./scripts/*.sh
echo "Done! ✅"

echo "Setup Done! 🎉"
echo "" 