# install all the packages
sudo apt install texlive-latex-base -y
sudo apt-get install texlive-fonts-recommended  -y
sudo apt-get install texlive-fonts-extra -y
sudo apt-get install texlive-latex-extra -y
sudo apt-get install texlive-xetex -y

cd /tmp
wget https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz 
zcat < install-tl-unx.tar.gz | tar xf -
cd install-tl-*
perl ./install-tl --no-interaction
export PATH=/usr/local/texlive/2020/bin/x86_64-linux:$PATH

sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr path add
sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr update --self
sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr update --all
sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr install collection-fontsrecommended
sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr install collection-fontsextra
sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr install collection-latexrecommended
sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr install collection-latexextra
sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr install collection-xetex

tlmgr init-usertree
tlmgr install hyperref

