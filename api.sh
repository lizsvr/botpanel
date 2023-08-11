echo -n "[+] Input Your Auth_Key: "
read AUTH
apt update && apt upgrade -y
apt install wget -y
apt install python3-pip python3
pip3 install flask
tee -a /etc/systemd/system/api.service<<END
[Unit]
Description=My Project
After=network.target

[Service]
WorkingDirectory=/usr/bin
ExecStart=/usr/bin/python3 /usr/bin/api.py 0.0.0.0 $AUTH
Restart=always

[Install]
WantedBy=multi-user.target
END

cd /usr/bin
wget https://raw.githubusercontent.com/lizsvr/botpanel/main/api.py
clear
systemctl start api
systemctl enable api
echo "[+] API Installation Completed."