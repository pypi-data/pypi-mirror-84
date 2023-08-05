echo "Make virtual host config ..."
cat > /etc/apache2/sites-available/{site}.conf <<EOL
<VirtualHost *:80>
    ServerName {site}
    ServerAlias {domains}
    ErrorLog  /var/www/{site}/log/error-{site}.log
    CustomLog /var/www/{site}/log/access-{site}.log combined

    ProxyRequests Off
    ProxyPreserveHost On
    ProxyVia Full
    <Proxy *>
       Require all granted
    </Proxy>
    <Location / >
       ProxyPass http://127.0.0.1:{port}/
       ProxyPassReverse http://127.0.0.1:{port}/
    </Location>
</VirtualHost>
EOL

ln -s /etc/apache2/sites-available/{site}.conf /var/www/{site}/hook/sites-available-{site}.conf 

echo "Enable virtual host ..."
a2ensite {site}