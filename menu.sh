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
BRED="\e[41m"
BBLUE="\e[38;5;21m"
# ==========================================
#information
OK = "$ {
  Green
}[OK]$ {
  Font
}"
Error = "$ {
  Red
}[Mistake]$ {
  Font
}"
clear
echo -e "$BLUE╔═══════════════════════════════════════$BLUE╗"
echo -e "$BLUE║           $ORANGE  [ Main Menu ]          $BLUE   ║"
echo -e "$BLUE╠═══════════════════════════════════════$BLUE╣"
echo -e "$BLUE║---------------------------------------║"
echo -e "$BLUE╠➣$NC 1$NC. Add admin ID (only 1)       $BLUE      ║ "
echo -e "$BLUE╠➣$NC 2$NC. add admin username          $BLUE      ║ " 
echo -e "$BLUE╠➣$NC 3$NC. add admin password          $BLUE      ║ " 
echo -e "$BLUE╠➣$NC 4$NC. Setting Bot Token           $BLUE      ║ " 
echo -e "$BLUE╠➣$NC 5$NC. Add Authkey                 $BLUE      ║ " 
echo -e "$BLUE╠➣$NC 6$NC. Start Bot                   $BLUE      ║ " 
echo -e "$BLUE╠➣$NC 7$NC. Stop bot                    $BLUE      ║ " 
echo -e "$BLUE╠➣$NC 8$NC. Check Service               $BLUE      ║ " 
echo -e "$BLUE╠➣$NC 9$NC. Exit                        $BLUE      ║ " 
echo -e "$BLUE║---------------------------------------║"
echo -e "$BLUE╠➣$NC Created By LIZSVR                    $BLUE║"
echo -e "$BLUE╠➣$NC Telegram https://t.me/liz_mine       $BLUE║"
echo -e "$BLUE╚═══════════════════════════════════════╝$NC"  
read -p "Select From Options [ 1 - 6 ] : " menu
echo -e ""
case $menu in
1)
clear
id_admin="$(cat ~/myfile/.env | grep ADMIN_ID | awk '{print $3}' )"
echo -e "======================================"
echo -e ""
echo -e "Admin id now $CYAN$id_admin $NC"
echo -e ""
echo -e "======================================"
read -p "New Admin Id : " id_new
if [ -z $id_new ]; then
echo "Please Input ID"
exit 0
fi
sed -i "s/$id_admin/'$id_new'/g" /root/myfile/.env
clear
echo -e "======================================"
echo -e ""
echo -e "Success Admin new $CYAN$id_new $NC"
echo -e ""
echo -e "======================================"
exit 0
;;
2)
clear
uname_admin="$(cat ~/myfile/.env | grep ADMIN_USERNAME | awk '{print $3}' )"
echo -e "======================================"
echo -e ""
echo -e "Admin username now $CYAN$uname_admin $NC"
echo -e ""
echo -e "======================================"
read -p "New Admin Id : " uname_new
if [ -z $uname_new ]; then
echo "Please Input ID"
exit 0
fi
sed -i "s/$uname_admin/'$uname_new'/g" /root/myfile/.env
clear
echo -e "======================================"
echo -e ""
echo -e "Success Admin username $CYAN$uname_new $NC"
echo -e ""
echo -e "======================================"
exit 0
;;
3)
clear
pas_admin="$(cat ~/myfile/.env | grep ADMIN_PASSWORD | awk '{print $3}' )"
echo -e "======================================"
echo -e ""
echo -e "Admin password now $CYAN$pas_admin $NC"
echo -e ""
echo -e "======================================"
read -p "New Admin password : " pass_new
if [ -z $pass_new ]; then
echo "Please Input password"
exit 0
fi
sed -i "s/$pas_admin/'$pass_new'/g" /root/myfile/.env
clear
echo -e "======================================"
echo -e ""
echo -e "Success Admin password $CYAN$pass_new $NC"
echo -e ""
echo -e "======================================"
exit 0
;;
4)
clear
bot_token="$(cat ~/myfile/.env | grep API_TOKEN | awk '{print $3}' )"
echo -e "======================================"
echo -e ""
echo -e "Bot Token now $CYAN$bot_token $NC"
echo -e ""
echo -e "======================================"
read -p "Bot Token now : " token_new
if [ -z $token_new ]; then
echo "Please Input Bot Token"
exit 0
fi
sed -i "s/$bot_token/'$token_new'/g" /root/myfile/.env
clear
echo -e "======================================"
echo -e ""
echo -e "Success Bot Token $CYAN$token_new $NC"
echo -e ""
echo -e "======================================"
exit 0
;;
5)
clear
auth_token="$(cat ~/myfile/.env | grep AUTH_KEY | awk '{print $3}' )"
echo -e "======================================"
echo -e ""
echo -e "Auth Token now $CYAN$auth_token $NC"
echo -e ""
echo -e "======================================"
read -p "Auth token new : " auth_new
if [ -z $auth_new ]; then
echo "Please Input Auth token"
exit 0
fi
sed -i "s/$auth_token/'$auth_new'/g" /root/myfile/.env
clear
echo -e "======================================"
echo -e ""
echo -e "Success Auth token $CYAN$auth_new $NC"
echo -e ""
echo -e "======================================"
exit 0
;;
6)
clear
echo "Start bot Sercive please wait..."
systemctl daemon-reload
systemctl enable api
systemctl start api
sleep 3
clear
echo "Start bot Sercive Success..."
;;
7)
clear
echo "Stoped bot Sercive please wait..."
systemctl daemon-reload
systemctl stop api
sleep 3
clear
echo "Stoped bot Sercive Success..."
;;
8)
clear
echo -e "$BLUE━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$NC"
echo -e "$BRED           Service Status            $NC"
echo -e "$BLUE━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$NC"
ell=active
sts=$(systemctl status api | grep Active: | awk '{print $2}')
if [ "$sts" == "$ell" ]; then
echo -e " Python3 / Bot            :$GREEN [Running] $NC"
else
echo -e " Python3 / Bot            :$RED [Error] $NC"
fi
echo -e "$BLUE━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$NC"
echo -e "$BRED---------- Scipt By LIZSVR ----------"
echo -e "$BLUE━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$NC"
;;
9)
clear
;;
*)
clear
;;
esac
#