
echo "Make all normal user can sudo {tool_name}"
echo "ALL ALL = NOPASSWD: /usr/local/bin/{tool_name}" > "/etc/sudoers.d/opsbot-allow-{tool_name}"