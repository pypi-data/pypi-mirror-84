echo "Gen a ssh key"
mkdir ~/.ssh
yes n | ssh-keygen -t rsa -b 4096 -C "VM" -N "" -f ~/.ssh/id_rsa

echo "Run ssh-agent"
eval "$(ssh-agent -s)"

echo "Add ssh key"
ssh-add ~/.ssh/id_rsa
