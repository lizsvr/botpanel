#!/bin/bash
# ==========================================
# Color
RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
LIGHT='\033[0;37m'
# ==========================================
#information
OK="${GREEN}[OK]${NC}"
Error="${RED}[Mistake]${NC}"
#!/bin/bash
if [ "${EUID}" -ne 0 ]; then
		echo "You need to run this script as root"
		exit 1
fi
if [ "$(systemd-detect-virt)" == "openvz" ]; then
		echo "OpenVZ is not supported"
		exit 1
fi

# Link Hosting Kalian 
lizsvr="raw.githubusercontent.com/lizsvr/botpanel/"
clear
# install all tools
apt update && apt upgrade -y 
apt install python3 -y
apt install python3-pip -y
pip3 install flask
pip3 install pyTelegramBotAPI
pip3 install SQLAlchemy
pip3 install requests
cd /root/
rm .setup.sh
if [ -f "/etc/botpanel/.env" ]; then
echo "Script Already Installed"
exit 0
fi
mkdir /var/lib/lizsvr
mkdir /etc/botpanel
mkdir /etc/botpanel/database
sleep 1
cd /usr/bin/
wget -O menu "https://${lizsvr}/menu.sh"
chmod +x menu
sleep 1
cd /etc/botpanel
wget https://${lizsvr}/sqldb.py
wget https://${lizsvr}/.env

tee -a /etc/systemd/system/api.service<<END
[Unit]
Description=My Project
After=network.target

[Service]
WorkingDirectory=/etc/botpanel
ExecStart=/usr/bin/python3 /etc/botpanel/sqldb.py
Restart=always

[Install]
WantedBy=multi-user.target
END
clear
systemctl daemon-reload
systemctl start api
systemctl enable api
echo "[+] API Installation Completed."
sleep 3
clear
rm -f /root/install.sh
echo "Installation Bot Completed "
sleep 3