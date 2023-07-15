# install pdflatex tlmgr  
# respect to https://github.com/indrjo/minimal-texlive-installer/tree/main for the installer, it just works 
chmod +x ./scripts/install-texlive
./scripts/install-texlive --scheme=small

texlivePath=$HOME/texlive/2023/bin/x86_64-linux
# make this path executable for every user
chmod -R 755 $texlivePath
# if user on zsh make this path available to zsh
[ -f $HOME/.zshrc ] && echo "Path Also added to your zshrc 😎" && echo "export PATH=$texlivePath:$PATH" >> $HOME/.zshrc 

# to install missing packages on the fly
$texlivePath/tlmgr install texliveonfly 

and python requirements
pip install -r requirements.txt

echo "Done!"