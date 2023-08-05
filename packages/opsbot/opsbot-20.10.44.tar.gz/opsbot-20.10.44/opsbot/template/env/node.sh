echo "Install stable nodejs"
apt install -y nodejs
apt install -y npm
npm install -g npm@latest

echo "Install Nodejs Process Manager"
npm install -g pm2