#Petit script pour installer K'ancienne version de Firefox 64
#zf190226.0840

firefox --version
sudo apt-get update && apt-get install -yq wget zip firefox
sudo apt -yq remove firefox
sudo rm -rf /opt/firefox/ /etc/firefox/
wget https://netcologne.dl.sourceforge.net/project/ubuntuzilla/mozilla/apt/pool/main/f/firefox-mozilla-build/firefox-mozilla-build_64.0.2-0ubuntu1_amd64.deb
sudo apt install -yq ./firefox-mozilla-build_64.0.2-0ubuntu1_amd64.deb
./restore_firefox_config.sh
firefox --version

