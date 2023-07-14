# install pdflatex tlmgr  
# respect to https://github.com/indrjo/minimal-texlive-installer/tree/main for the installer, it just works 
chmod +x ./install-texlive
./install-texlive --scheme=small
source ~/.bashrc

tlmgr install hyperref
tlmgr install texliveonfly #to install missing packages on the fly

# and python requirements
pip install -r requirements.txt

echo "Done!"