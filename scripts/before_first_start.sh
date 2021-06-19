#!/bin/bash
cd .. 
sudo apt update
sudo apt upgrade
sudo apt install git
sudo apt install mc
sudo apt install python3
sudo apt install python3-venv
sudo apt install python3-pip
sudo apt install supervisor
sudo apt install nginx
sudo apt install -y ufw
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow 443/tcp
sudo ufw --force enable
sudo ufw status
python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt