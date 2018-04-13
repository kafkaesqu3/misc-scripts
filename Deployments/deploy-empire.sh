#!/bin/bash

apt-get update
apt-get -y install git build-essential python python2.7 python2.7-dev python-pip libssl-dev
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
apt-get install software-properties-common -y
add-apt-repository ppa:certbot/certbot -y
apt-get update
apt-get install python-certbot-apache -y

echo -e "\033[32m [*] Requesting certificate"
certbot certonly -d $domain --standalone --register-unsafely-without-email --agree-tos

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

cat << EOF > /root/dev.rc
set Host https://$domain:443
set CertPath /etc/letsencrypt/live/$domain/
set Port 443
set ServerVersion Apache/2.4.9 (Unix)
set DefaultProfile /search/admin.html|Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko
EOF

cat << EOF > /root/prod.rc
set Host https://$domain:443
set CertPath /etc/letsencrypt/live/$domain/
set Port 443
set ServerVersion Apache/2.4.9 (Unix)
set DefaultProfile /search/admin.html|Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko|Accept:text/html,application/xhtml+xml,application/xml
set DefaultDelay 25
set DefaultJitter 0.3
set WorkingHours 08:00-17:00 
EOF

echo -e "\033[32m [*] Resource file: /root/improved_empire_$domain.rc"
echo "wget --spider --force-html -r -l2 $url 2>&1 \
  | grep '^--' | awk '{ print $3 }' \
  | grep -v '\.\(css\|js\|png\|gif\|jpg\)$'
"

echo "Dont forget to change the html base!"
echo "Good luck"
echo "Dont forget to change the html!"

