echo "Make virtual host config ..."
cat > /etc/apache2/sites-available/{site}.conf <<EOL
<VirtualHost *:80>
    ServerName {site}
    ServerAlias {domains}
    DocumentRoot /var/www/{site}/html/{public_directory}
    <Directory /var/www/{site}/html/{public_directory}>
        AllowOverride All
    </Directory>
    ErrorLog  /var/www/{site}/log/error-{site}.log
    CustomLog /var/www/{site}/log/access-{site}.log combined
</VirtualHost>
EOL

ln -s /etc/apache2/sites-available/{site}.conf /var/www/{site}/hook/sites-available-{site}.conf 

echo "Enable virtual host ..."
a2ensite {site}