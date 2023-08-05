#!/bin/bash
chown -R {owner}:www-data /var/www/{site}/html
chown -R {owner}:{owner} /var/www/{site}/db