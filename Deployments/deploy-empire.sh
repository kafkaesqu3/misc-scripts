#!/bin/bash

apt-get update
apt-get -y install git build-essential python2.7 python2.7-dev python-pip libssl1.1 libssl-dev
git clone https://github.com/EmpireProject/Empire
STAGING_KEY = python -c "import string; from Crypto.Random import random; punctuation = '!#%&()*+,-./:;<=>?@[]^_{|}~'; print ''.join(random.sample(string.ascii_letters + string.digits + punctuation, 32))"
echo export $STAGING_KEY >> ~/.bashrc
source ~/.bashrc
cd Empire/setup
./install.sh

wget https://github.com/PowerShell/PowerShell/releases/download/v6.0.0-rc.2/powershell_6.0.0-rc.2-1.ubuntu.16.04_amd64.deb

if [ "$@" -ne 2 ]; then
	echo -e "\033[32m [*] Usage: ./get-cert.sh [domain]"
fi
domain=$1
echo -e "\033[32m [*] Installing Letsencrypt certbot"
apt-get install software-properties-common
add-apt-repository ppa:certbot/certbot
apt-get update
apt-get install python-certbot-apache

echo -e "\033[32m [*] Building config at /etc/letsencrypt/cli.ini"
cat << EOF > /etc/letsencrypt/cli.ini
text = True
agree-tos = True
email = admin@$domain
webroot-path = /var/www/html
EOF
echo -e "\033[32m [*] Requesting certificate"
certbot --apache -d $domain --config /etc/letsencrypt/cli.ini

echo -e "\033[32m [*] Stopping apache server"
service apache2 stop

cd /etc/letsencrypt/live/$domain
cat cert.pem privkey.pem > empire.pem
cp privkey.pem empire-priv.key
cp fullchain.pem empire-chain.pem

if [ -s /etc/letsencrypt/live/$domain/empire.pem]; then
	echo -e "\033[32m [*] SUCCESS: Your cert is at /etc/letsencrypt/live/$domain/empire.pem"
else
	echo -e "\033[31m [*] FAILURE no certificate detected" 
fi

echo -e "\033[32m [*] Generating resource file"

cat << EOF > /root/improved_empire_$domain.rc
listeners
uselistener http
set Host https://$domain:443
set CertPath /etc/letsencrypt/live/$domain/
set Port 443
set ServerVersion nginx
set DefaultProfile /search?q=news&go=Search&qs=bs&form=QBRE,/search?q=weather&go=Search&qs=bs&form=QBRE,/search?q=movie%20tickets&go=Search&qs=bs&form=QBRE,/search?q=unit%20conversion&go=Search&qs=bs&form=QBRE,/search?q=bitcoin%eprices&go=Search&qs=bs&form=QBRE,/search?q=current%20weather&go=Search&qs=bs&form=QBRE|Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko|Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8|Cookie:DUP=Q=GjU3nAvlFmEWar0NsbcP3ga&T=273053546&A=2&ID

EOF

echo -e "\033[32m [*] Resource file: /root/improved_empire_$domain.rc"