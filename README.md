### Command Install

```
rm -f setup.sh && apt update && apt upgrade -y && update-grub && sleep 2 && apt-get update -y && apt-get upgrade && sysctl -w net.ipv6.conf.all.disable_ipv6=1 && sysctl -w net.ipv6.conf.default.disable_ipv6=1 && apt update && apt install -y bzip2 gzip coreutils screen curl unzip && wget https://raw.githubusercontent.com/lizsvr/botpanel/install.sh && chmod +x setup.sh && sed -i -e 's/\r$//' install.sh && screen -S install ./install.sh
```

### Fitur Bot Panel SSH [ By LIZ ]

• SSH & OpenVPN

• SSH Websocket TLS & No TLS ( CloudFlare & CloudFront )

• OHP SSH & OHP Dropbear & OHP OpenVPN

• Backup Data ALL Service

• Restore Data ALL Service

### Os Supported

• Debian 10 Only

• Ubuntu 18.04 & 20.04 (Recommended)

------------
**Telegram**
------------
[LIZSVR](https://t.me/liz_mine)
