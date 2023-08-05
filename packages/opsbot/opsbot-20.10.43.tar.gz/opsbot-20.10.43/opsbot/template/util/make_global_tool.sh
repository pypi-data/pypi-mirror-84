
echo "Make global tool {tool_name}"
cat > "/usr/local/bin/{tool_name}" <<EOL
{command}
EOL
chmod 755 /usr/local/bin/{tool_name}