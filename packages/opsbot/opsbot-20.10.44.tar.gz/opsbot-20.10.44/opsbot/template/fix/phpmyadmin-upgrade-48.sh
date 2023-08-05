echo "Fix phpmyadmin on php72. Upgrade phpmyadmin to version 4.8"
mv /usr/share/phpmyadmin /usr/share/phpmyadmin_old
echo "Downloading new version ..."
wget  https://files.phpmyadmin.net/phpMyAdmin/4.8.2/phpMyAdmin-4.8.2-english.tar.gz
echo "Dxtracting ... "
tar -xvzf phpMyAdmin-4.8.2-english.tar.gz > /dev/null
mv phpMyAdmin-4.8.2-english /usr/share/phpmyadmin
rm phpMyAdmin-4.8.2-english.tar.gz
cp /etc/phpmyadmin/config.inc.php  /usr/share/phpmyadmin
mkdir /usr/share/phpmyadmin/tmp
chown www-data:www-data /usr/share/phpmyadmin/tmp
echo "Removing old version ..."
rm -rf /usr/share/phpmyadmin_old > /dev/null
