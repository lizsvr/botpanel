apt update && apt upgrade -y
apt install python3-pip python3
pip3 install flask
tee -a /etc/systemd/system/api.service<<END
[Unit]
Description=My Project
After=network.target

[Service]
WorkingDirectory=/etc/botpanel/
ExecStart=/usr/bin/python3 /etc/botpanel/sqldb.py
Restart=always

[Install]
WantedBy=multi-user.target
END

systemctl start api
systemctl enable api
echo "[+] API Installation Completed."