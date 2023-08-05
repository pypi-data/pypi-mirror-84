
echo "Make a daily cron"
cat <(crontab -l) <(echo "{minute} {hour} * * * {command}") | crontab -