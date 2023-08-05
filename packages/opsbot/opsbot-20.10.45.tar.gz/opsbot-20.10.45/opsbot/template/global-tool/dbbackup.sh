#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Missing parameters!"
    echo "Usage: dbbackup <site>"
    exit
fi

site="$1"
LOGFILE="/var/www/$site/log/db-backup.log"

function backup()
{
    echo ""
    echo ""
    date 

    echo "Run ssh-agent"
    eval "$(ssh-agent -s)"
    echo "Add ssh key"
    ssh-add ~/.ssh/id_rsa

    echo "Run dbexport database"
    /var/www/$site/tool/dbexport.sh

    echo "Commit ..."
    cd /var/www/$site/db
    #git branch backup
    git config user.name "Opsbot"
    git config user.email "opsbot@magik.vn"
    git commit -am "Opsbot auto backup database"
    echo "Push to git..."
    git push

    echo "Reset Site Owner Permission"
    sudo /var/www/$site/tool/resetowner.sh

    echo "Done at $(date)"
}
backup 2>&1 | tee -a ${LOGFILE}

