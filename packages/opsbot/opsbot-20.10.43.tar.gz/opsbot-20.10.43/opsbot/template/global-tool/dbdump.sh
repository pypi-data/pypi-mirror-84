#!/bin/bash
if [ "$#" -ne 5 ]; then
    echo "Missing parameters!"
    echo "usage : dbdump <import|export> <site> <db_username> <mysql_password> <mongodb_password>"
    exit
fi

action="$1"
site="$2"
db_username="$3"
mysql_password="$4"
mongodb_password="$5"
line_per_file=100

db_path="/var/www/$site/db"
lst_path="$db_path/dblist.opsbot"

SQL_CONNECT_STR="-u$db_username -p$mysql_password"
MONGODB_CONNECT_STR="-u $db_username -p $mongodb_password --authenticationDatabase=admin"

if [ ! -f $lst_path ]; then
    echo "db config not exists"
    exit;
fi

while IFS= read -r line || [ -n "$line" ];  do
    if [ "$line" = "" ]; then
        continue
    fi
    stringarray=($line)
    dbms=${stringarray[0]}
    database=${stringarray[1]}

    echo "Begin dump $action $dbms database [$line]"
    if [ "$dbms" = "mysql" ]; then
        if [ "$action" = "export" ]; then
            mysqldump $SQL_CONNECT_STR --skip-dump-date --single-transaction --extended-insert=FALSE  $database > "$db_path/$database.sql"
        fi
        if [ "$action" = "import" ]; then
            mysqladmin $SQL_CONNECT_STR create $database
            mysql $SQL_CONNECT_STR $database <  "$db_path/$database.sql"
        fi
    fi

    if [ "$dbms" = "mongodb" ]; then
        dir="$db_path/$database"
        if [ "$action" = "export" ]; then
            cols=$(mongo $database $MONGODB_CONNECT_STR --quiet --eval "db.getCollectionNames()" | grep \" | tr -d '\[\]\"[:space:]' | tr ',' ' ')
            for col in $cols; do
                echo "$database.$col"
                mongoexport $MONGODB_CONNECT_STR -d $database -c $col -o $dir/$col.json
            done
        fi
        if [ "$action" = "import" ]; then
            ls -1 $dir/*.json | sed "s,$dir/,,g" | sed 's/.json$//' | while read col; do 
                tmpDir=$(mktemp -d)
                echo "Split $col.json to $tmpDir"
                split -l $line_per_file $dir/$col.json $tmpDir/

                ls -1 $tmpDir/* | while read file; do
                    echo "Import $file to $col"
                    mongoimport $MONGODB_CONNECT_STR -d $database -c $col --file $file --mode upsert
                done
                rm -r $tmpDir
            done
        fi
    fi
done < "$lst_path"
