#!/bin/bash

#deploy wordpress and generate some generic content for believability in social engineering engagements
apt-get install apache2 apache2-utils 
systemctl enable apache2
systemctl start apache2

cat << 'EOF' > /etc/apache2/apache2.conf
DefaultRuntimeDir ${APACHE_RUN_DIR}
PidFile ${APACHE_PID_FILE}
Timeout 300
KeepAlive On
MaxKeepAliveRequests 100
KeepAliveTimeout 5
User ${APACHE_RUN_USER}
Group ${APACHE_RUN_GROUP}
HostnameLookups Off
ErrorLog ${APACHE_LOG_DIR}/error.log
LogLevel warn
IncludeOptional mods-enabled/*.load
IncludeOptional mods-enabled/*.conf
Include ports.conf
<Directory />
	Options FollowSymLinks
	AllowOverride None
	Require all denied
</Directory>
<Directory /usr/share>
	AllowOverride None
	Require all granted
</Directory>
<Directory /var/www/>
	Options Indexes FollowSymLinks
	AllowOverride None
	Require all granted
</Directory>
<Directory /var/www/html/>
    AllowOverride All
</Directory>
AccessFileName .htaccess
<FilesMatch "^\.ht">
	Require all denied
</FilesMatch>
LogFormat "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" vhost_combined
LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" combined
LogFormat "%h %l %u %t \"%r\" %>s %O" common
LogFormat "%{Referer}i -> %U" referer
LogFormat "%{User-agent}i" agent
IncludeOptional conf-enabled/*.conf
IncludeOptional sites-enabled/*.conf
EOF

mysql_root_password=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 15 | head -n 1)
echo "Mysql root is $mysql_root"

wordpress_password=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 15 | head -n 1)
echo "Wordpress password is $wordpress_password"

apt-get install mysql-client mysql-server

#need to do this noninteractively
mysql_secure_installation 

mysql -u root -pProtiviti2017 -e "CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
mysql -u root -pProtiviti2017 -e "GRANT ALL ON wordpress.* TO 'wordpressuser'@'localhost' IDENTIFIED BY 'Protiviti2017!';"
mysql -u root -pProtiviti2017 -e "FLUSH PRIVILEGES;"


apt-get install php php-curl php-gd php-mbstring php-mcrypt php-xml php-xmlrpc php-mysql



wget -c http://wordpress.org/latest.tar.gz
tar -xzvf latest.tar.gz

cp wordpress/wp-config-sample.php wordpress/wp-config.php

cp -a wordpress/* /var/www/html

chown -R david:www-data /var/www/html
find /var/www/html -type d -exec chmod g+s {} \;
chmod g+w /var/www/html/wp-content
chmod -R g+w /var/www/html/wp-content/themes
chmod -R g+w /var/www/html/wp-content/plugins

curl -s https://api.wordpress.org/secret-key/1.1/salt/
