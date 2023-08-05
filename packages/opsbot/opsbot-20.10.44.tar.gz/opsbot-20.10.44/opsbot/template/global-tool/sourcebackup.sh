#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Missing parameters!"
    echo "Usage: sourcebackup <site>"
    exit
fi

site="$1"
LOGFILE="/var/www/$site/log/source-backup.log"

function backup {
    remoteurl=$(git config --get remote.origin.url)
    if [[ $remoteurl == http* ]]; then
        echo "Current remote.origin.url not support yet"
        echo $remoteurl
        echo "Please change into ssh url use command : "
        echo "git remote set-url origin ..."
        exit
    fi
    echo ""
    echo ""
    date 

    echo "Run ssh-agent"
    eval "$(ssh-agent -s)"
    echo "Add ssh key"
    ssh-add ~/.ssh/id_rsa


    echo "Commit ..."
    cd /var/www/$site/html
    #git branch backup
    git config user.name "Opsbot"
    git config user.email "opsbot@magik.vn"
    git add . 
    git commit -am "Opsbot auto backup html" 
    echo "Push ..."
    git push 

    echo "Reset Site Owner Permission"
    sudo /var/www/$site/tool/resetowner.sh
    
    echo "Done at $(date)"

}
backup 2>&1 | tee -a ${LOGFILE}
