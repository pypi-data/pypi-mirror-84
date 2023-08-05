if [ -z "$1" ]; then
    echo "Usage: passwordgenerated.sh <password_variable>"
    exit
fi
touch configgenerated
source configgenerated
passwordvar=$1
passwordvarVal=${!passwordvar}
if [ -z $passwordvarVal ]; then
    echo "Password $passwordvar generated and store in configgenerated"
    passwordvarVal=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c24)
    echo "$passwordvar=\"$passwordvarVal\""  >> configgenerated
fi