#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Missing parameters!"
    echo "Usage: certbotsafe <domain1,domain2>"
    exit
fi
certbot -n --apache --agree-tos --expand -m {admin} --domain "$1"