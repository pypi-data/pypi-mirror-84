echo "install LAMP (Linux - Apache - Mysql - PHP) ..."
debconf-set-selections <<< "mysql-server mysql-server/root_password password $root_mysql_password"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $root_mysql_password"
apt install -y lamp-server^

echo "enable mod rewrite ..."
a2enmod rewrite

echo ""

cat > /etc/apache2/conf-enabled/gitprotect.conf <<EOL
<DirectoryMatch "/\.git"> 
Require all denied
</DirectoryMatch>
EOL



echo "start apache2 and mysql if stopped ..."
service apache2 start
service mysql start

echo "Fix Mysql on ubuntu 18.04 . Change authentication type of root."
mysql --execute="ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$root_mysql_password';FLUSH PRIVILEGES;"

echo "install apache without promt ..."
debconf-set-selections <<< "phpmyadmin phpmyadmin/dbconfig-install boolean true"
debconf-set-selections <<< "phpmyadmin phpmyadmin/app-password-confirm password $root_mysql_password"
debconf-set-selections <<< "phpmyadmin phpmyadmin/mysql/admin-pass password $root_mysql_password"
debconf-set-selections <<< "phpmyadmin phpmyadmin/mysql/app-pass password $phpmyadmin_mysql_password"
debconf-set-selections <<< "phpmyadmin phpmyadmin/reconfigure-webserver multiselect apache2"
apt install -y phpmyadmin


echo "Install Apache proxy"
a2enmod proxy
a2enmod proxy_http
