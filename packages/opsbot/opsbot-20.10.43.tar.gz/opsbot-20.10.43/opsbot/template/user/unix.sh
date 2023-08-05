echo "Create unix user ..."
encrypted=$(python -c "import crypt; print(crypt.crypt(\"${username}_unix_password\", \"Fx\"))")
useradd --create-home --password $encrypted --shell /bin/bash {username} 
chmod 700 "/home/{username}"