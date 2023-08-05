echo "Create mongodb user"
#TODO: support grant permission multi db for user.
username="{username}"
password="${username}_mongodb_password"
db="{prefix}"
mongo admin --eval "db.createUser({{user: \"$username\", pwd: \"$password\", roles:[{{role:\"dbOwner\", db:\"$db\"}}]}});"