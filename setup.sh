apt update
# apt upgrade -y

# # install all the packages
# sudo apt install texlive-latex-base -y 
# sudo apt-get install texlive-fonts-recommended  -y 
# sudo apt-get install texlive-latex-extra -y 

# which pdflatex
# pdflatex --version

# cd /tmp
# wget https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz 
# zcat < install-tl-unx.tar.gz | tar xf -
# cd install-tl-2023*
# perl ./install-tl --no-interaction
# export PATH=/usr/local/texlive/2020/bin/x86_64-linux:$PATH

# sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr path add
# sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr update --self
# sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr update --all
# sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr install collection-fontsrecommended &
# sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr install collection-fontsextra &
# sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr install collection-latexrecommended &
# sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr install collection-latexextra &
# sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr install collection-xetex &

# wait

# tlmgr init-usertree

# respect to https://github.com/indrjo/minimal-texlive-installer/tree/main for the installer, it just works 
./install-texlive --scheme=medium
# to auto install requirements 
# tlmgr install texliveonfly
tlmgr install hyperref