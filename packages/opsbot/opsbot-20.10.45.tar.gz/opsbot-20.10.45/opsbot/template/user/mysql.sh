echo "Create mysql user ..."
sql="
    CREATE USER '{username}'@'%' IDENTIFIED WITH mysql_native_password BY  '${username}_mysql_password';
    GRANT ALL PRIVILEGES ON \`{prefix}%\`.* TO '{username}'@'%' WITH GRANT OPTION;
    flush privileges;
"
mysql -uroot -p"$root_mysql_password" --execute="$sql"