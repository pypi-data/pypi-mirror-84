#!/bin/bash
if [ ! -f ~/.ssh/id_rsa ]; then echo "ssh-key not found"; exit; fi

echo "I. ADD SSH KEY"
eval "\$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

echo "II. PULL SOURCE CODE ... "
{comment_line_1}git clone --depth 1 {source_git} /var/www/{site}/html

{comment_line_2}echo "III. PULL DATABASE ..."
{comment_line_2}git clone --depth 1 {database_git} /var/www/{site}/db
{comment_line_2}echo "IV. IMPORT DATABASE ..."
{comment_line_2}/var/www/{site}/tool/dbimport.sh


source /var/www/{site}/tool/configgenerated
if [ -f /var/www/{site}/html/autodeploy.opsbot ]; then 
    echo "V. RUN AUTODEPLOY FROM SITE REPO"
    cd /var/www/{site}/html
    source /var/www/{site}/html/autodeploy.opsbot    
fi

echo "VI. RESET OWNER TO NORMAL USER"
sudo /var/www/{site}/tool/resetowner.sh
