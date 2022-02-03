#!/usr/bin/env bash
# Create /data/ folder if it doesn't already exist
# Create /data/web_static/ folder if it doesn't already exist
# Create /data/web_static/releases/ folder if it doesn't already exist
# Create /data/web_static/shared/ folder if it doesn't already exist
# Create /data/web_static/releases/test folder if it doesn't already exist
# Create fake HTML file in /data/web_static/releases/test/index.html
# Create a symbolic link `current` of /data/web_static/releases/test in /data/web_static/
# Change owner of /data/ parent directory to ubuntu. Change group to ubuntu as well
# Configure Nginx to serve content in symlink `current` when request directory is /hbnb_static/

if ! which nginx > /dev/null; then
	apt update;  apt install nginx -y
fi

mkdir -p /data/web_static/shared
mkdir -p /data/web_static/releases /data/web_static/releases/test

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | tee /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test /data/web_static/current;

chown -Rh ubuntu:ubuntu /data

if ! grep -q "/hbnb_static" /etc/nginx/sites-available/default; then
	sed -i "s/\tlocation \/ {/\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t\ttry_files \$uri \$uri\/index.html \$uri\/ =404;\n\t}\n\n\tlocation \/ {/" /etc/nginx/sites-available/default
fi

service nginx restart
