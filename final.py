#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot, datetime
from sqlalchemy import create_engine, insert
from dotenv import load_dotenv
from telebot import types
import requests, re, base64, json, os, subprocess, socket
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import datetime as DT

API_TOKEN = '5599756373:AAFaM673KFraL4yDyDiy102WD_1aVvOk7k4'

bot = telebot.TeleBot(API_TOKEN)
load_dotenv() # get .env variable
today = DT.date.today()

# all status
status_register = "register"
status_login = "login"
status_logout = "logout"

# load data base
basedir = 'database/'
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
ADMIN_ID = os.getenv("ADMIN_ID")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
AUTH_KEY = os.getenv("AUTH_KEY")
SERVER = os.getenv("SERVER").split(";")
server = []
for z in SERVER:
	s = z.split(",")
	server.append({"name":s[0],"host":s[1],"harga":s[2]})
 # ============================================================================
def rupiah_format(uang):
    y = str(uang)
    if len(y) <= 3:
        return "Rp" + y
    else:
        p = y[-3:]
        q = y[:-3]
        return rupiah_format(q) + '.' + p
        print('Rp' + rupiah_format(q) + '.' + p)

# ============================================================================

# Function that creates a message the contains a list of all the server
def list_server(ans):
    text = ""
    for i in ans:
        id = i[0]
        reg = i[1]
        isp = i[2]
        domain = i[3]
        harga = i[4]
        harga_akhir = rupiah_format(harga)
        # text += "<b>"+ str(id) +"</b> | " + "<b>"+ str(product) +"</b> | " + "<b>"+ str(quantity)+"</b> | " + "<b>"+ str(creation_date)+"</b>\n"
        # text += "<b>"+ str(id) +".</b> | " +"<b>"+ str(reg) +"</b> | " + "<b>"+ str(isp) +"</b> | " + "<b>Rp."+ str(harga)+"</b>\n"
        text += f"`{id}.| {reg} | {isp} | {harga_akhir}`\n" 
    message = "`LIZ🇮🇩 SSH PREMIUM 📖\n\n💰Price List:`\n"+text
    return message

# ============================================================================        
        
# Function that creates a message the contains a list of all the server
def member_list(ans):
    text = ""
    for i in ans:
        id = i[0]
        username = i[1]
        password = i[2]
        saldo = i[3]
        status = i[4]
        saldo_out = rupiah_format(saldo)
        # [ ID | Username | Saldo ]
        # text += "<b>"+ str(id) +"</b> | " + "<b>"+ str(product) +"</b> | " + "<b>"+ str(quantity)+"</b> | " + "<b>"+ str(creation_date)+"</b>\n"
        # text += "<b>"+ str(id) +".</b> | " +"<b>"+ str(reg) +"</b> | " + "<b>"+ str(isp) +"</b> | " + "<b>Rp."+ str(harga)+"</b>\n"
        text += f"ID: `{id}` | `{username}` | `{saldo_out}` \n" 
    message = "`LIZ🇮🇩 SSH PREMIUM 📖\n\n📑Member List:`\n\n"+text
    return message

# ============================================================================
def server_out(ip_s, domain, username, password, create, exp_acc):
    server_o = f"""
Thank You For Using Our Services                                            
====== SSH & OVPN Account ======
IP/Host       : `{ip_s}`
Domain        : `{domain}`
Username      : `{username}`
Password      : `{password}`
======== Running On Port =======
Dropbear      : 109, 143
SSL/TLS       : 443, 445, 777
SSH WS SSL    : 443
SSH WS No SSL : 8880
Ovpn Ws       : 2086
Port TCP      : 1194
Port UDP      : 2200
Port SSL      : 990
========== Ovpn Config ==========                                            
OVPN TCP   : `http://{domain}:89/tcp.ovpn`
OVPN UDP   : `http://{domain}:89/udp.ovpn`                           
OVPN SSL   : `http://{domain}:89/ssl.ovpn `                            
BadVpn     : `7100-7200-7300`
Created    : {create}
Expired    : {exp_acc}
================================
Silahkan pilih /start untuk ke menu
================================"""
    return server_o

# ============================================================================

# all keyoard markup
callback_login = types.InlineKeyboardButton(text="Login", callback_data="login")
callback_logout = types.InlineKeyboardButton(text="Logout", callback_data="logout")
callback_back = types.InlineKeyboardButton(text="Back Menu", callback_data="back")
callback_register = types.InlineKeyboardButton(text="Register", callback_data="register")
callback_menu = types.InlineKeyboardButton(text="Menu", callback_data="menu")
callback_settings = types.InlineKeyboardButton(text="Settings", callback_data="settings")
callback_add_acc = types.InlineKeyboardButton(text="Create SSH", callback_data="add_acc")
callback_list_acc = types.InlineKeyboardButton(text="List ACC", callback_data="list_acc")
callback_dell_acc = types.InlineKeyboardButton(text="Dell ACC", callback_data="dell_acc")
# admin keyboard
callback_admin_login = types.InlineKeyboardButton(text="Password", callback_data="adm_login")
callback_admin_logout = types.InlineKeyboardButton(text="Logout", callback_data="adm_logout")
callback_admin_back = types.InlineKeyboardButton(text="Menu", callback_data="adm_back")
callback_admin_topup_acc = types.InlineKeyboardButton(text="Topup member", callback_data="topup_member")
callback_admin_server_add = types.InlineKeyboardButton(text="Add server", callback_data="add_server")
callback_admin_server_edit = types.InlineKeyboardButton(text="Edit server", callback_data="edit_server")
callback_admin_server_delete = types.InlineKeyboardButton(text="Delete server", callback_data="delete_server")
callback_admin_list_member = types.InlineKeyboardButton(text="List Member", callback_data="list_member")
# setting row keyboard
keyboard_m = types.InlineKeyboardMarkup(row_width=2)
keyboard_l = types.InlineKeyboardMarkup(row_width=2)
keyboard_r = types.InlineKeyboardMarkup(row_width=2)
keyboard_back = types.InlineKeyboardMarkup(row_width=2)
keyboard_list_menu = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin_back = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin_login = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin_add_svr = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin_edit_svr = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin_delete_svr = types.InlineKeyboardMarkup(row_width=2)
# add keyboard
keyboard_l.add(callback_login)
keyboard_r.add(callback_register)
keyboard_m.add(callback_menu, callback_settings, callback_logout)
keyboard_back.add(callback_back)
keyboard_list_menu.add(callback_add_acc, callback_dell_acc, callback_list_acc, callback_back)
keyboard_admin.add(callback_admin_topup_acc, callback_admin_server_add, callback_admin_server_edit, callback_admin_server_delete, callback_admin_logout)
keyboard_admin_login.add(callback_admin_login)
keyboard_admin_add_svr.add(callback_admin_server_add)
keyboard_admin_edit_svr.add(callback_admin_server_edit)
keyboard_admin_delete_svr.add(callback_admin_back, callback_admin_server_delete)
keyboard_admin_back.add(callback_admin_back)




# Get starterd
@bot.message_handler(commands=['start'])
def any_msg(message):
    # print(message)
    teleid = str(message.from_user.id)
    exist_id = [z[0] for z in db.execute("SELECT idtele FROM userz").fetchall()]
    print("Teleid /start:",teleid)
    if teleid in exist_id:
        sts_r = db.execute("SELECT status FROM userz WHERE idtele = ?",(teleid)).fetchone()[0]
        username_m = db.execute("SELECT username FROM userz WHERE idtele = ?",(teleid)).fetchone()[0]
        print(sts_r)
        if sts_r == status_register:
            bot.send_message(message.chat.id, "Silahkan Login Terlebih Dahulu", reply_markup=keyboard_l)
            print("user sudah di register")
        elif teleid in exist_id and sts_r == status_logout:
            print("user belum login")
            bot.send_message(message.chat.id, "Silahkan Login ulang Terlebih Dahulu", reply_markup=keyboard_l)
        elif teleid in exist_id and sts_r == status_login:
            print("user sudah login")
            saldo_awal = db.execute("SELECT saldo FROM userz WHERE username = ?",(username_m)).fetchone()[0]
            reg_date = db.execute("SELECT dateRegister FROM userz WHERE username = ?",(username_m)).fetchone()[0]
            saldo_akhir = rupiah_format(saldo_awal)
            print(saldo_akhir)
            text = f"""Selamat datang di Liz SSH premium!!\nHallo {username_m}😃\nSaldo: {saldo_akhir}\nRestered: 30/01/2023\nemail : -none\nAccount SSH : 0"""
            bot.send_message(message.chat.id, text=text ,parse_mode='html', reply_markup=keyboard_m)
    else:
        print("user belum registrasi")
        bot.send_message(message.chat.id, "Silahkan Register Terlebih Dahulu", reply_markup=keyboard_r)
        
# ============================================================================

# Get login admin
@bot.message_handler(commands=['admin'])
def any_msg(message):
    teleid = str(message.from_user.id)
    try:
        db.execute("SELECT password FROM admin WHERE idtele = ?",(teleid)).fetchone()[0]
        sts_l = db.execute("SELECT status FROM admin WHERE idtele = ?",(teleid)).fetchone()[0]
    except:
        db.execute("INSERT INTO admin (idtele,username,password,status) VALUES (?,?,?,?);",(teleid,ADMIN_USERNAME,ADMIN_PASSWORD,status_register))
        sts_l = db.execute("SELECT status FROM admin WHERE idtele = ?",(teleid)).fetchone()[0]
    
    if teleid == ADMIN_ID and sts_l == status_login:
        sent = bot.send_message(message.chat.id, text=f"""Selamat Datang {ADMIN_USERNAME} 🥰\n""", reply_markup=keyboard_admin)
    elif teleid == ADMIN_ID:
        sent = bot.send_message(message.chat.id, text=f"""Selamat Datang {ADMIN_USERNAME} 🥰\nSilahkan login terlebih dahulu""", reply_markup=keyboard_admin_login)
    elif teleid in ADMIN_ID and sts_l == status_logout:
        print("user belum login")
        bot.send_message(message.chat.id, "Silahkan Login ulang Terlebih Dahulu", reply_markup=keyboard_admin_login)
    else:
        print("Maf anda bukan admin..")
        bot.send_message(message.chat.id, "Maaf anda bukan admin..")
        
# ============================================================================    

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        teleid = str(call.message.chat.id)
        if call.data == "login":
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format Login 'L-username-passwd'""")
            def login_p(message):
                try:
                    user_i = message.text.split("-")
                    req_ = user_i[0]
                    username = user_i[1] # The second (1) element is the id
                    password = user_i[2]
                    user_log= message.chat.first_name
                    exist = [z[0] for z in db.execute("SELECT username FROM userz").fetchall()]
                    sts_r = db.execute("SELECT status FROM userz WHERE idtele = ?",(teleid)).fetchone()[0]
                    sts_u = db.execute("SELECT username FROM userz WHERE idtele = ?",(teleid)).fetchone()[0]
                    # print(message)
                    if req_ == "L":
                        if username not in exist:
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Username {username} salah/tidak terdaftar""")
                            bot.delete_message(message.chat.id, message.id)
                            print("Username Salah/Tidak terdaftar Silakan masukan ulang..")
                            bot.register_next_step_handler(sent, login_p)
                        else:
                            pw = db.execute("SELECT password FROM userz WHERE username = ?",(username)).fetchone()[0]
                            if password != pw and username == sts_u:
                                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Login as {username} fwrong password..Silahkan masukan ulang""")
                                bot.delete_message(message.chat.id, message.id)
                                print(f"""Login as {username} Failed wrong password..!!""")
                                bot.register_next_step_handler(sent, login_p)
                            elif username != sts_u:
                                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Tidak mendukung Multi login Telegram dengan 1 username""")
                                bot.delete_message(message.chat.id, message.id)
                                print(f"""Login as {username} Failed Terdeteksi multi login..!!""")
                            else:
                                saldo_akun = db.execute("SELECT saldo FROM userz WHERE username = ?",(username)).fetchone()[0]
                                reg_date = db.execute("SELECT dateRegister FROM userz WHERE username = ?",(username)).fetchone()[0]
                                saldo_akhir = rupiah_format(saldo_akun)
                                text = f"""Selamat datang di Liz SSH premium!!\nHallo {username}😃\nSaldo : {saldo_akhir}\nRestered: {reg_date}\nemail : -none\nAccount SSH : 0"""
                                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text ,parse_mode='html', reply_markup=keyboard_m)
                                bot.delete_message(message.chat.id, message.id)
                                db.execute("UPDATE userz SET status = ? WHERE idtele = ?", (status_login,teleid))
                                print(f"""Login as {username} successfuly..!!""")
                    else:
                        print("Gunakan 'L'-username-paswd untuk login")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Gunakan 'L'-username-paswd untuk login""")
                        bot.delete_message(message.chat.id, message.id)
                        bot.register_next_step_handler(sent, login_p)
                except:
                    print("Format Login salah!!")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format Login salah!!""")
                    bot.delete_message(message.chat.id, message.id)
            bot.register_next_step_handler(sent, login_p)
            
        if call.data == "register":
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format Register 'R-username-passwd'""")
            today = DT.date.today()
            def register_p(message):
                try:
                    user_i = message.text.split("-")
                    req_ = user_i[0]  # The second (0) element is the telegramID
                    username = user_i[1] # The second (1) element is the username
                    password = user_i[2]  # The second (2) element is the pawssword
                    user_log= message.chat.first_name
                    exist_u = [z[0] for z in db.execute("SELECT username FROM userz").fetchall()]
                    
                    if req_ == "R":
                        if not username:
                            print("Invalid Username")
                        elif not password:
                            print("Invalid password")
                        elif username in exist_u:
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Username already existed..""")
                            bot.delete_message(message.chat.id, message.id)
                            print("username Already Exist")
                        else:
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Registrasi {username} Success!! Silahkan login""", reply_markup=keyboard_l)
                            bot.delete_message(message.chat.id, message.id)
                            db.execute("INSERT INTO userz (idtele,username,password,status,dateRegister) VALUES (?,?,?,?,?);", (teleid, username,password,status_register,today))
                            print(f"""Register as: {user_log}""")
                    else:
                        print("Gunakan 'R'-username-paswd untuk register")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Gunakan 'R'-username-paswd untuk register""")
                        bot.delete_message(message.chat.id, message.id)
                except:
                    print("Format Register salah!!")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format Register salah Silahkan ulangi /start""")
                    bot.delete_message(message.chat.id, message.id)
                return
            bot.register_next_step_handler(sent, register_p)
        if call.data == "logout": 
            # teleid = str(call.message.chat.id)
            username_m = db.execute("SELECT username FROM userz WHERE idtele = ?",(teleid)).fetchone()[0]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Logout as {username_m} Successfuly..!!""")
            db.execute("UPDATE userz SET status = ? WHERE idtele = ?", (status_logout,teleid))
            print(f"""Logout successfuly..!!""")
            print("logout teleid :", teleid)
        
        if call.data == "menu":
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Silahkan pilih menu di bawa \n""", reply_markup=keyboard_list_menu)
            
        if call.data == "settings":
            print("ini settings")
            
        if call.data == "add_acc":
            print("ini add acc")
            server_z = db.execute("SELECT * FROM serverz").fetchall()
            list_s = list_server(server_z)
            count_server = len(server_z)
            sent_l = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""{list_s}\nPilih dari [ 1 - {count_server} ]""", parse_mode='markdown')
            def input_ssh(message):
                # print(message)
                user_in = message.text
                exist_id = [z[0] for z in db.execute("SELECT id FROM serverz").fetchall()]
                try: 
                    if int(user_in) not in exist_id:
                        print("angka tidak ada i dalam list")
                    else:
                        print(f"Angka ada di dalan list {user_in}")
                        sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Silahkan masukan \nUsername + password\n Contoh: \n`lizadm,123`""", parse_mode='markdown', reply_markup=keyboard_back)
                        bot.delete_message(message.chat.id, message.id)
                        def create_ssh(message):
                            try:
                                print(user_in)
                                user_i = message.text.split(",")
                                username = user_i[0]  # The second (0) element is the telegramID
                                password = user_i[1] # The second (1) element is the username
                                id_ = db.execute("SELECT id FROM serverz WHERE id = ?",(user_in)).fetchone()[0]
                                domain = db.execute("SELECT domain FROM serverz WHERE id = ?",(user_in)).fetchone()[0]
                                harga = db.execute("SELECT harga FROM serverz WHERE id = ?",(user_in)).fetchone()[0]
                                saldo_akun = db.execute("SELECT saldo FROM userz WHERE idtele = ?",(teleid)).fetchone()[0]
                                ip_server = socket.gethostbyname(domain)
                                len_msg = len(user_i)
                                # x = requests.get("http://"+serverv[0]+f":6969/adduser/exp?user={user}&password={pw}&exp={exp}")
                                if int(saldo_akun) < int(harga):
                                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Saldo anda tidak cukup Silahkan topup""", parse_mode='markdown', reply_markup=keyboard_back)
                                    bot.delete_message(message.chat.id, message.id)
                                elif str(len_msg) >= "3":
                                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format input lebih""", parse_mode='markdown', reply_markup=keyboard_back)
                                    bot.delete_message(message.chat.id, message.id)
                                else:
                                    url = "http://"+domain+f":6969/adduser/exp?user={username}&password={password}&exp=30"
                                    headers = ({'AUTH_KEY':AUTH_KEY })
                                    try :
                                        today = DT.date.today()
                                        exp = "28"
                                        exp = datetime.datetime.today() + datetime.timedelta(days=int(exp))
                                        exp = exp.strftime("%Y-%m-%d")
                                        requests.get(url, headers=headers)
                                        output_req = server_out(ip_server,domain,username,password,today,exp)
                                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=output_req, parse_mode='markdown')
                                        bot.delete_message(message.chat.id, message.id)
                                        db.execute("UPDATE userz SET saldo = ? WHERE idtele = ?", (str(int(saldo_akun) - int(harga)), teleid))
                                    except:
                                        print("else")
                                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Error server tidak terhubung dengan API bots", parse_mode='markdown')
                                        bot.delete_message(message.chat.id, message.id)
                            except:
                                bot.send_message(message.chat.id, text="Pilih menu /start terlebih dahulu..", parse_mode='html')      
                        bot.register_next_step_handler(sent, create_ssh)

                except:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Silahkan masukan \nUsername + password\n Contoh: \n`lizadm,123`""", parse_mode='markdown', reply_markup=keyboard_back)
                    bot.delete_message(message.chat.id, message.id)
                    
            bot.register_next_step_handler(sent_l, input_ssh)
 
        if call.data == "list_acc":
            print("ini list acc")
            
        if call.data == "dell_acc":
            print("ini dell acc")
            
        if call.data == "back":
            print("ini back")
            username = db.execute("SELECT username FROM userz WHERE idtele = ?",(teleid)).fetchone()[0]
            saldo_akun = db.execute("SELECT saldo FROM userz WHERE username = ?",(username)).fetchone()[0]
            reg_date = db.execute("SELECT dateRegister FROM userz WHERE username = ?",(username)).fetchone()[0]
            saldo_akhir = rupiah_format(saldo_akun)
            text = f"""Selamat datang di Liz SSH premium!!\nHallo {username}😃\nSaldo : {saldo_akhir}\nRestered: {reg_date}\nemail : -none\nAccount SSH : 0"""
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text ,parse_mode='html', reply_markup=keyboard_m)
            
        if call.data == "adm_login":
            try:
                sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Silahkan masukan password {ADMIN_USERNAME}""")
                def reply_adm_login(message):
                    if message.text == ADMIN_PASSWORD:
                        print("success login admin")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Selamat Datang {ADMIN_USERNAME} 🥰\n""", reply_markup=keyboard_admin)
                        bot.delete_message(message.chat.id, message.id)
                        db.execute("UPDATE admin SET status = ? WHERE idtele = ?", (status_login,teleid))
                    else:
                        print("password admin salah")
                        text1 = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Password salah silahkan masukan ulang..""", reply_markup=keyboard_admin_login)
                        bot.delete_message(message.chat.id, message.id)
                        
                bot.register_next_step_handler(sent, reply_adm_login)
            except:
                print("something error..!!")
        
        if call.data == "adm_logout": 
            username_adm = db.execute("SELECT username FROM admin WHERE idtele = ?",(teleid)).fetchone()[0]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Logout admin as {username_adm} Successfuly..!!""")
            db.execute("UPDATE admin SET status = ? WHERE idtele = ?", (status_logout,teleid))
            print(f"""Logout successfuly..!!""")
        
        if call.data == "adm_back":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Selamat Datang {ADMIN_USERNAME} 🥰\n""", reply_markup=keyboard_admin)
    
        if call.data == "add_server":
            server_z = db.execute("SELECT * FROM serverz").fetchall()
            list_s = list_server(server_z)
            count_server = len(server_z)
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=list_s+"\n📓 Masukan server dengan format \n`Region,ISP,Domain,harga` \nContoh:\n`SG,DO,sg-do.lizserver.me,10000`", parse_mode='MARKDOWN', reply_markup=keyboard_admin_back)
            
            def add_server(message):
                try:
                    user_i = message.text.split(",")
                    region = user_i[0]  # The second (0) element is the telegramID
                    isp = user_i[1] # The second (1) element is the username
                    domain = user_i[2]  # The second (2) element is the pawssword
                    harga = user_i[3]  # The second (2) element is the pawssword
                    len_user = len(user_i)
                    exist_u = [z[0] for z in db.execute("SELECT region FROM serverz").fetchall()]
                    print(len_user)
                    if len_user == 4:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Add domain: `{domain}` Success!!""", parse_mode="MARKDOWN", reply_markup=keyboard_admin_back)
                        bot.delete_message(message.chat.id, message.id)
                        db.execute("INSERT INTO serverz (id,region,isp,domain,harga) VALUES (NULL,?,?,?,?);", (region, isp, domain, harga))
                        print(f"""Register as: {domain}""")
                    else:
                        print("Format salah silahkan periksa ulang..")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""`Format salah silahkan periksa add ulang..`""", parse_mode="MARKDOWN", reply_markup=keyboard_admin_add_svr)
                        bot.delete_message(message.chat.id, message.id)
                except:
                    print("Format salah silahkan periksa ulang..")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""`Format salah silahkan periksa ulang..`""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin_add_svr)
                    bot.delete_message(message.chat.id, message.id)
                    
            bot.register_next_step_handler(sent, add_server)
            
        if call.data == "edit_server":
            print("ini edit server")
            server_z = db.execute("SELECT * FROM serverz").fetchall()
            list_s = list_server(server_z)
            count_server = len(server_z)
            exist_id = [z[0] for z in db.execute("SELECT id FROM serverz").fetchall()]
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=list_s+"\nEdit server dengan format \n`no,Region,ISP,Domain,harga` \nContoh:\n`1,SG,DO,sg-do.lizserver.me,10000`", parse_mode='MARKDOWN', reply_markup=keyboard_admin_back)
            def edit_server(message):
                try:
                    user_i = message.text.split(",")
                    id = user_i[0]  # The second (0) element is the telegramID
                    region = user_i[1]  # The second (0) element is the telegramID
                    isp = user_i[2] # The second (1) element is the username
                    domain = user_i[3]  # The second (2) element is the pawssword
                    harga = user_i[4]  # The second (3) element is the pawssword
                    msg_count = len(user_i)
                    # print(type(msg_count))
                    if msg_count == 5:
                        print("input lengkap..")                        
                        db.execute("UPDATE serverz SET region = ?, isp = ?, domain = ?, harga = ? WHERE id = ?;", (region,isp,domain,harga,id))
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""`Server Id: {id}\nRegion: {region}\nISP: {isp}\nDomain: {domain}\nHarga: {harga}\nBerhasil di edit.. `""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin_back)
                        bot.delete_message(message.chat.id, message.id)
                    else:
                        print("input lebih..")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Format salah pilih ulang server! \nContoh:\n`1,SG,DO,sg-do.lizserver.me,10000`""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin_edit_svr)
                        bot.delete_message(message.chat.id, message.id)
                except:
                    print("Format salah/kurang..")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Format salah pilih ulang server! \nContoh:\n`1,SG,DO,sg-do.lizserver.me,10000`""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin_edit_svr)
                    bot.delete_message(message.chat.id, message.id)
                    
            bot.register_next_step_handler(sent, edit_server)
            
        if call.data == "topup_member":
            print("ini topup")
            userz_list = db.execute("SELECT * FROM userz").fetchall()
            member_l = member_list(userz_list)
            count_server = len(userz_list)
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=member_l+"\n📓 Masukan username + saldo yang ini akan topup \nContoh:\n`lizsvr,100000`", parse_mode='MARKDOWN', reply_markup=keyboard_admin_back)
            def add_saldo(message):
                try:
                    user_i = message.text.split(",")
                    username = user_i[0]  # The second (0) element is the telegramID
                    saldo = user_i[1] # The second (1) element is the username
                    saldo_awal = db.execute("SELECT saldo FROM userz WHERE username = ?",(username)).fetchone()[0]
                    saldo_akhir = (int(saldo_awal) + int(saldo))
                    db.execute("UPDATE userz SET saldo = ? WHERE username = ?", (saldo_akhir,username))
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""`Topup Saldo {username} Rp.{saldo_akhir} berhasil..`""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin)
                    bot.delete_message(message.chat.id, message.id)
                    print("saldo berhasil di update")
                except:
                    print("Username tidak terdaftar")
            bot.register_next_step_handler(sent, add_saldo)
            
        if call.data == "delete_server":
            print("ini Delete Server")
            server_z = db.execute("SELECT * FROM serverz").fetchall()
            list_s = list_server(server_z)
            count_server = len(server_z)
            exist_id = [z[0] for z in db.execute("SELECT id FROM serverz").fetchall()]
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=list_s+"\nPilih no server yang akan di hapus", parse_mode='MARKDOWN')
            def delete_server(message):
                user_i = message.text
                exist_id = [z[0] for z in db.execute("SELECT id FROM serverz").fetchall()]
                count_server = len(exist_id)
                try:
                    if int(user_i) in exist_id:
                        id_ = db.execute("SELECT id FROM serverz WHERE id = ?",(count_server)).fetchone()[0]
                        region = db.execute("SELECT region FROM serverz WHERE id = ?",(count_server)).fetchone()[0]
                        isp = db.execute("SELECT isp FROM serverz WHERE id = ?",(count_server)).fetchone()[0]
                        domain = db.execute("SELECT domain FROM serverz WHERE id = ?",(count_server)).fetchone()[0]
                        harga = db.execute("SELECT harga FROM serverz WHERE id = ?",(count_server)).fetchone()[0]
                        db.execute("UPDATE serverz SET region = ?, isp = ?, domain = ?, harga = ? WHERE id = ?;", (region,isp,domain,harga,user_i))
                        db.execute("DELETE FROM serverz WHERE id = ?", (count_server) )
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Server Sudah di hapus..!!""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin_back)
                        bot.delete_message(message.chat.id, message.id)
                    else:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Nomor yang anda pilih tidak ada di daftar pilih ulang server..""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin_delete_svr)
                        bot.delete_message(message.chat.id, message.id)
                except:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Masukan hanya ada di pilihan daftar silahkan pilih ulang server..""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin_delete_svr)
                    bot.delete_message(message.chat.id, message.id)
                    
            bot.register_next_step_handler(sent, delete_server)


# def create_ssh(id_s, teleid, usename, passwd, exp):

# p1 = subprocess.call('/home/lizsvr/myweb/subprocess/tes.sh')

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:
        server_z = db.execute("SELECT * FROM serverz").fetchall()
        list_s = list_server(server_z)
        bot.send_message(message.chat.id, text="Pilih menu /start terlebih dahulu..", parse_mode='html')
    except:
        print("Something Wrong")
        

##### MAIN
if __name__ == '__main__':
    try:
        print("Initializing Database...")
        # Connect to local database
        db = create_engine(database, pool_pre_ping=True)
        db.execute("CREATE TABLE IF NOT EXISTS userz (idtele varchar, username varchar, password varchar, saldo varchar DEFAULT 0, status varchar, dateRegister varchar DEFAULT 0)")
        db.execute("CREATE TABLE IF NOT EXISTS transaksi (username varchar, tanggal varchar, akun varchar, harga varchar, status varchar)")
        db.execute("CREATE TABLE IF NOT EXISTS serverz (id INTEGER PRIMARY KEY, region varchar, isp varchar, domain varchar, harga varchar, totalakun varchar DEFAULT 0)")
        db.execute("CREATE TABLE IF NOT EXISTS admin (idtele varchar, username varchar, password varchar, status varchar)")
        # db.execute("INSERT INTO serverz (id,region,isp,domain,harga) VALUES (NULL,'SG','DO','sg-do.lizserver.me','10,000');")
        # db.execute("INSERT INTO serverz (id,region,isp,domain,harga) VALUES (NULL,'US','AZURE','azure.lizserver.me','18,000');")
        # db.execute("INSERT INTO serverz (id,region,isp,domain,harga) VALUES (NULL,'ID','Rajasa','rajasa.lizserver.me','18,000');")
        print("Connected to the database")
        print("Bot Started")
        bot.infinity_polling()
        
    except Exception as error:
        print('Cause: {}'.format(error))