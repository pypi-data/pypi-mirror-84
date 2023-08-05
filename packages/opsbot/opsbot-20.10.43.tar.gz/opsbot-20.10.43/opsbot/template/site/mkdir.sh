echo "Make directories for website ..."
mkdir /var/www/{site}
mkdir /var/www/{site}/html
mkdir /var/www/{site}/db
mkdir /var/www/{site}/hook
mkdir /var/www/{site}/tool
mkdir /var/www/{site}/log

echo "Config log rotate"
touch /var/www/{site}/log/access-{site}.log
touch /var/www/{site}/log/error-{site}.log

cat > /etc/logrotate.d/vhost-{site}.lr <<EOL
/var/www/{site}/log/*.log {{
        monthly
        missingok
        rotate 12
        maxsize 500M
        notifempty
        create 644 root adm
        sharedscripts
        postrotate
                if /etc/init.d/apache2 status > /dev/null ; then 
                    /etc/init.d/apache2 reload > /dev/null; 
                fi;
        endscript
        prerotate
                if [ -d /etc/logrotate.d/httpd-prerotate ]; then 
                        run-parts /etc/logrotate.d/httpd-prerotate; 
                fi;
        endscript
}}
EOL

echo "Hook noted"
ln -s /etc/logrotate.d/vhost-{site}.lr /var/www/{site}/hook/logrotate.d-vhost-{site}.lr

echo "Setup permissions for website directories"
chown {owner}:{owner} /var/www/{site}
chown {owner}:www-data /var/www/{site}/html
chown {owner}:{owner} /var/www/{site}/db
chmod g+s /var/www/{site}/html /var/www/{site}/db
chmod o-rwx /var/www/{site}/html  /var/www/{site}/db