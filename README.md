### Command Install Admin

```
rm -f setup.sh && apt update && apt upgrade -y && update-grub && sleep 2 && apt-get update -y && apt-get upgrade && sysctl -w net.ipv6.conf.all.disable_ipv6=1 && sysctl -w net.ipv6.conf.default.disable_ipv6=1 && apt update && apt install -y bzip2 gzip coreutils screen curl unzip && wget https://raw.githubusercontent.com/lizsvr/botpanel/main/setup.sh && chmod +x setup.sh && sed -i -e 's/\r$//' setup.sh && screen -S setup ./setup.sh
```

### Command Install for API SSH server 

```
apt update && apt upgrade -y && curl -O hhttps://raw.githubusercontent.com/lizsvr/botpanel/main/api.sh && bash api.sh
```

### Fitur Bot Panel SSH [ By LIZ ]

• Create SSH and Delete Acc with bot

• Admin setting

• Top up member and delete member

• Use Sqlite3 database

### Note!

• Program ini hanya contoh untuk pembelajaran ya 

• Silahkan Update database dengan Postgres atau yang lain 

• jika ada error silahkan hubungin saya di Telegram 

### Os Supported

• Debian 10 Only

• Ubuntu 18.04 & 20.04 (Recommended)

### Tutorial Install

•Comming soon

------------
**Telegram**
------------
[LIZSVR](https://t.me/liz_mine)
