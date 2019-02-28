#Petit script pour restaurer la config de firefox depuis un zip
#zf190226.0846

rm -rf ~/.mozilla/
unzip firefox_config.zip -d ~/
mv ~/home/zuzu/.mozilla ~/
rmdir ~/home/zuzu/
rmdir ~/home/





