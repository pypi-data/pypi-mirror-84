echo "Install package python for scrapy"
apt install python python-pip python-mysqldb

echo "Install scrapy & libs"
pip install scrapy requests bs4 geopy phonenumbers
