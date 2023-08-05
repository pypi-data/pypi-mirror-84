
echo "Make site tool {tool_file}"
cat > /var/www/{site}/tool/{tool_file} <<EOL
{command}
EOL
chown {owner}:{owner} /var/www/{site}/tool/{tool_file}
chmod 700 /var/www/{site}/tool/{tool_file}