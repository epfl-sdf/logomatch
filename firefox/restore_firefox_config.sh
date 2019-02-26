#Petit script pour restaurer la config de firefox depuis un zip
#zf190226.0846

rm -rf ~/.mozilla/
unzip firefox_config.zip -d ~/
mv ~/root/.mozilla ~/
rm -rf ~/root





