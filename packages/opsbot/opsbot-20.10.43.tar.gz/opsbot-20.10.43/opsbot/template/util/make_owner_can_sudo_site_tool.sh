
echo "Make owner can sudo site tool: {tool_file}"
echo "{owner} ALL = NOPASSWD: /var/www/{site}/tool/{tool_file}" > /etc/sudoers.d/opsbot-{site_nodot}
ln -s /etc/sudoers.d/opsbot-{site_nodot}  /var/www/{site}/hook/sudoers.d-opsbot-{site}-{tool_file}