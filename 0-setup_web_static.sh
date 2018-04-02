#!/usr/bin/env bash
# install nginx if not already installed
sudo apt-get -y update
sudo apt-get -y install nginx

# Make directories
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# create temporary index
TEMP=$'<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>'
sudo echo "$TEMP" | sudo tee /data/web_static/releases/test/index.html

# create soft link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# change ownership
sudo chown -R ubuntu:ubuntu /data

# add location to sites-available
sudo sed -i '37 i \\tlocation /hbnb_static {' /etc/nginx/sites-available/default
sudo sed -i '38 i \\t\talias /data/web_static/current;' /etc/nginx/sites-available/default
sudo sed -i '39 i \\t}' /etc/nginx/sites-available/default

# then restart
sudo service nginx restart
