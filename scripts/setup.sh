# install pdflatex tlmgr  
# respect to https://github.com/indrjo/minimal-texlive-installer/tree/main for the installer, it just works 
# check if pdflatx, tlmgr and texliveonfly is installed
# if not install it
if command -v pdflatex >/dev/null && command -v tlmgr >/dev/null && command -v texliveonfly >/dev/null; then
    echo "All required packages are installed. ✅"
else
    chmod +x ./scripts/install-texlive
    ./scripts/install-texlive --scheme=small

    texlivePath=$HOME/texlive/2023/bin/x86_64-linux
    # make this path executable for every user
    chmod -R 755 $texlivePath
    # if user on zsh make this path available to zsh
    [ -f $HOME/.zshrc ] && echo "Path Also added to your zshrc 😎" && echo "export PATH=$texlivePath:$PATH" >> $HOME/.zshrc 

    # to install missing packages on the fly
    echo "Installing texliveonfly..."
    $texlivePath/tlmgr install texliveonfly > /dev/null
    echo "Done! ✅"
fi

# install pip if not installed
if ! [ -x "$(command -v pip)" ]; then
    echo 'Error: pip is not installed.' 
    echo 'Installing pip ..' 
    sudo apt-get install python-pip > /dev/null
    echo 'Done! ✅' 
fi

update_pip() {
    echo "Updating pip..."
    sudo pip install --upgrade pip > /dev/null
    echo "Done! ✅\n"
}

update_pip


# check if requirements.txt exists and install requirements
if [ -f "requirements.txt" ]; then
    echo "requirements.txt found. 😎 installing requirements..."
    sudo pip install -r requirements.txt > /dev/null
    echo "Done! ✅"
else
    echo "requirements.txt not found. 🚫"
    exit 1
fi



# make all files in scripts executable
echo "Making all files in scripts executable..."
chmod +x ./scripts/*.sh
echo "Done! ✅"

echo "Setup Done! 🎉"