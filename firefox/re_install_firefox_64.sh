#Petit script pour installer K'ancienne version de Firefox 64
#zf190226.1745

#si une fois il n'est plus possible d'installer firefox sur la machine, c'est qu'il y a DEUX firefox installés partiellement en MEME temps !
#on peut les détecter avec: 'sudo apt list --installed |grep firefox' et les désintaller un après l'autre avec: 'sudo apt remove appname'


firefox --version
sudo apt-get update && sudo apt-get install -yq wget zip firefox
sudo apt -yq remove firefox
sudo rm -rf /opt/firefox/ /etc/firefox/
rm firefox-mozilla*.deb
wget https://netcologne.dl.sourceforge.net/project/ubuntuzilla/mozilla/apt/pool/main/f/firefox-mozilla-build/firefox-mozilla-build_64.0.2-0ubuntu1_amd64.deb
sudo apt install -yq ./firefox-mozilla-build_64.0.2-0ubuntu1_amd64.deb
./restore_firefox_config.sh
firefox --version

