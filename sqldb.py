import os, telebot, datetime, socket, requests
from sqlalchemy import *
from telebot import types
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import datetime as DT

# load data base
basedir = 'database/'
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")

# bot token
# API_TOKEN = '5868093119:AAHmp1MG5NRXXtJOSNRZeoZQTE1i-IgNftk'
load_dotenv() # get .env variable

# ADMIN_ID = "5957002828"
# ADMIN_USERNAME = "lizid"
# ADMIN_PASSWORD = "adminliz"
# AUTH_KEY = "lizid"

ADMIN_ID = os.getenv("ADMIN_ID")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
AUTH_KEY = os.getenv("AUTH_KEY")
API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

# all status
status_register = "register"
status_login = "login"
status_logout = "logout"
status_active = "active"
status_expired = "expired"

# today
today = DT.date.today()

# all keyoard markup
callback_login = types.InlineKeyboardButton(text="Login", callback_data="login")
callback_logout = types.InlineKeyboardButton(text="Logout", callback_data="logout")
callback_back = types.InlineKeyboardButton(text="Back Menu", callback_data="back")
callback_register = types.InlineKeyboardButton(text="Register", callback_data="register")
callback_menu = types.InlineKeyboardButton(text="Menu", callback_data="menu")
callback_settings = types.InlineKeyboardButton(text="Change password", callback_data="cpass")
callback_add_acc = types.InlineKeyboardButton(text="List Server", callback_data="add_acc")
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
keyboard_add_acc = types.InlineKeyboardMarkup(row_width=2)
keyboard_dell_acc = types.InlineKeyboardMarkup(row_width=2)
keyboard_settings = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin_back = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin_login = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin_add_svr = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin_edit_svr = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin_delete_svr = types.InlineKeyboardMarkup(row_width=2)
keyboard_admin_topup_acc = types.InlineKeyboardMarkup(row_width=2)
# add keyboard
keyboard_l.add(callback_login)
keyboard_r.add(callback_register)
keyboard_m.add(callback_menu, callback_settings, callback_logout)
keyboard_back.add(callback_back)
keyboard_add_acc.add(callback_add_acc)
keyboard_dell_acc.add(callback_dell_acc)
keyboard_settings.add(callback_settings)
keyboard_list_menu.add(callback_add_acc, callback_dell_acc, callback_list_acc, callback_back)
keyboard_admin.add(callback_admin_topup_acc, callback_admin_server_add, callback_admin_server_edit, callback_admin_server_delete, callback_admin_logout)
keyboard_admin_login.add(callback_admin_login)
keyboard_admin_add_svr.add(callback_admin_server_add)
keyboard_admin_edit_svr.add(callback_admin_server_edit)
keyboard_admin_delete_svr.add(callback_admin_server_delete)
keyboard_admin_back.add(callback_admin_back)
keyboard_admin_topup_acc.add(callback_admin_topup_acc)
# ====================================================
def dbc(x1,x2):
    with db.engine.begin() as conn:
        x1 = conn.execute(text(x2))
    return(x1)
# ====================================================
def rupiah_format(uang):
    y = str(uang)
    if len(y) <= 3:
        return "Rp" + y
    else:
        p = y[-3:]
        q = y[:-3]
        return rupiah_format(q) + '.' + p
        print('Rp' + rupiah_format(q) + '.' + p)
# ====================================================
def list_server(ans):
    text = ""
    for i in ans:
        id = i[0]
        reg = i[1]
        isp = i[2]
        domain = i[3]
        harga = i[4]
        harga_akhir = rupiah_format(harga)
        text += f"`> {id} | {reg} | {isp} | {harga_akhir}`\n" 
    message = "LIZ🇮🇩 SSH PREMIUM 📖\n\n💰Price List:\n"+text
    return message
# ====================================================
def member_list(ans):
    text = ""
    for i in ans:
        id = i[0]
        username = i[1]
        password = i[2]
        saldo = i[3]
        status = i[4]
        saldo_out = rupiah_format(saldo)
        text += f"ID: `{id}` | `{username}` | `{saldo_out}` \n" 
    message = "`LIZ🇮🇩 SSH PREMIUM 📖\n\n📑Member List:`\n\n"+text
    return message
# ====================================================

def member_ssh(ans):
    text = ""
    for i in ans:
        username = i[1]
        created = i[2]
        expired = i[3]
        status = i[4]
        text += f" ➣ `{username}` | {expired} | {status} \n" 
    message = "LIZ🇮🇩 SSH PREMIUM \n\n📑SSH List:\n"+text
    return message
# ====================================================

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

# ====================================================

@bot.message_handler(commands=['start'])
def any_msg(message):
    teleid = str(message.from_user.id)
    exist_id = [z[0] for z in dbc("db","SELECT idtele FROM userz").fetchall()]
    exist_user = [z[0] for z in dbc("db","SELECT username FROM userz").fetchall()]
    print("Teleid /start:",teleid)
    if teleid in exist_id:
        print("ada")
        sts_r = dbc("db",f"""SELECT status FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
        username_m = dbc("db",f"""SELECT username FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
        if sts_r == status_register:
            bot.send_message(message.chat.id, "Silahkan Login Terlebih Dahulu", reply_markup=keyboard_l)
            print("user sudah di register")
        elif teleid in exist_id and sts_r == status_logout:
            print("user belum login")
            bot.send_message(message.chat.id, "Silahkan Login ulang Terlebih Dahulu", reply_markup=keyboard_l)
        elif teleid in exist_id and sts_r == status_login:
            print("user sudah login")
            saldo_awal = dbc("db",f"""SELECT saldo FROM userz WHERE username = '{username_m}'""").fetchone()[0]
            reg_date = dbc("db",f"""SELECT dateRegister FROM userz WHERE username = '{username_m}'""").fetchone()[0]
            saldo_akhir = rupiah_format(saldo_awal)
            print(saldo_akhir)
            text = f"""Selamat datang di Liz SSH premium!!\nHallo {username_m}!!\nSaldo : {saldo_akhir}\nRestered: {reg_date}\nID anda : `{teleid}`"""
            bot.send_message(message.chat.id, text=text ,parse_mode='markdown', reply_markup=keyboard_m)
    else:
        print("user belum registrasi")
        bot.send_message(message.chat.id, "Silahkan Register Terlebih Dahulu", reply_markup=keyboard_r)


@bot.message_handler(commands=['admin'])
def any_msg(message):
    teleid = str(message.from_user.id)
    sts_l = dbc("db",f"""SELECT status FROM admin WHERE idtele = {teleid}""").fetchone()[0]
    if teleid == ADMIN_ID and sts_l == status_login:
        sent = bot.send_message(message.chat.id, text=f"""Selamat Datang {ADMIN_USERNAME} 🥰\n""", reply_markup=keyboard_admin)
    elif teleid == ADMIN_ID:
        sent = bot.send_message(message.chat.id, text=f"""Selamat Datang {ADMIN_USERNAME} 🥰\nSilahkan login terlebih dahulu""", reply_markup=keyboard_admin_login)
    elif teleid in ADMIN_ID and sts_l == status_logout:
        bot.send_message(message.chat.id, "Silahkan Login ulang Terlebih Dahulu", reply_markup=keyboard_admin_login)
    else:
        bot.send_message(message.chat.id, "Maaf anda bukan admin..")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:
        server_z = dbc("db","SELECT * FROM serverz").fetchall()
        list_s = list_server(server_z)
        bot.send_message(message.chat.id, text="Pilih menu /start terlebih dahulu..", parse_mode='html')
        bot.delete_message(message.chat.id, message.id)
    except:
        bot.send_message(message.chat.id, text="Pilih menu /start terlebih dahulu..", parse_mode='html')
        bot.delete_message(message.chat.id, message.id)
        print("Something Wrong")
        


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        teleid = str(call.message.chat.id)
        if call.data == "register":
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format Register 'username-passwd' Di ingat ya karena akan otomatis terhapus""")
            def register_p(message):
                try:
                    user_i = message.text.split("-")
                    username = user_i[0]
                    password = user_i[1]
                    user_log = message.chat.first_name
                    len_user = len(user_i)
                    print(user_i)
                    if len_user == 2:
                        print("format benar")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Registrasi {username} Success!! Silahkan login""", reply_markup=keyboard_l)
                        bot.delete_message(message.chat.id, message.id)
                        dbc("db",f"""INSERT INTO userz (idtele, username, password, status, dateRegister) VALUES ({teleid}, '{username}', '{password}', '{status_register}', '{today}')""")
                    else:
                        print("Format Register salah!!")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format Register salah Silahkan ulangi /start""")
                        bot.delete_message(message.chat.id, message.id)
                except:
                    print("Format Register salah!!")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format Register salah Silahkan ulangi /start""")
                    bot.delete_message(message.chat.id, message.id)

            bot.register_next_step_handler(sent, register_p)

        if call.data == "login":
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format Login 'L-username-passwd'""")
            def login_p(message):
                try:
                    user_i = message.text.split("-")
                    username = user_i[0]
                    password = user_i[1]
                    user_log= message.chat.first_name
                    exist = [z[0] for z in dbc("db","SELECT username FROM userz").fetchall()]
                    sts_u = dbc("db",f"""SELECT username FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
                    sts_r = dbc("db",f"""SELECT status FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
                    len_user = len(user_i)
                    print(sts_u, sts_r, exist, len_user)
                    if username in exist and len_user == 2:
                        pw = dbc("db",f"""SELECT password FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
                        print(pw)
                        if username == sts_u and password == pw:
                            saldo_akun = dbc("db",f"""SELECT saldo FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
                            reg_date = dbc("db",f"""SELECT dateRegister FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
                            saldo_akhir = rupiah_format(saldo_akun)
                            text = f"""Selamat datang di Liz SSH premium!!\nHallo {username}!!\nSaldo : {saldo_akhir}\nRestered: {reg_date}\nID anda : `{teleid}`"""
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text ,parse_mode='markdown', reply_markup=keyboard_m)
                            bot.delete_message(message.chat.id, message.id)
                            dbc("db",f"""UPDATE userz SET status = '{status_login}' WHERE idtele = '{teleid}'""")
                            print(f"""Login as {username} successfuly..!!""")
                        else:
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Password Salah silahkan coba lagi!!""", reply_markup=keyboard_l)
                            bot.delete_message(message.chat.id, message.id)
                            print("password Salah")
                    else:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Username Salah silahkan coba lagi!!""", reply_markup=keyboard_l)
                        bot.delete_message(message.chat.id, message.id)
                        print("username Salah")
                except:
                    print("Format Login salah!!")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format Login salah silahkan Login ulang""", reply_markup=keyboard_l)
                    bot.delete_message(message.chat.id, message.id)

            bot.register_next_step_handler(sent, login_p)

        if call.data == "logout":
            username_m = dbc("db",f"""SELECT username FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Logout as {username_m} Successfuly..!!""")
            dbc("db",f"""UPDATE userz SET status = '{status_logout}' WHERE idtele = '{teleid}'""")
            print(f"""Logout successfuly..!!""")

        if call.data == "adm_logout": 
            username_adm = dbc("db",f"""SELECT username FROM admin WHERE idtele = '{teleid}'""").fetchone()[0]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Logout admin as {username_adm} Successfuly..!!""")
            dbc("db",f"""UPDATE admin SET status = '{status_logout}' WHERE idtele = '{teleid}'""")
            print(f"""Logout successfuly..!!""")

        if call.data == "adm_login":
            try:
                sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Silahkan masukan password {ADMIN_USERNAME}""")
                def reply_adm_login(message):
                    if message.text == ADMIN_PASSWORD:
                        print("success login admin")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Selamat Datang {ADMIN_USERNAME} 🥰\n""", reply_markup=keyboard_admin)
                        bot.delete_message(message.chat.id, message.id)
                        dbc("db",f"""UPDATE admin SET status = '{status_login}' WHERE idtele = '{teleid}'""")
                    else:
                        print("password admin salah")
                        text1 = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Password salah silahkan masukan ulang..""", reply_markup=keyboard_admin_login)
                        bot.delete_message(message.chat.id, message.id)
                        
                bot.register_next_step_handler(sent, reply_adm_login)
            except:
                print("something error..!!")

        if call.data == "adm_back":
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Selamat Datang {ADMIN_USERNAME} 🥰\n""", reply_markup=keyboard_admin)
            def reply_adm_back(message):
                print(message)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Silahkan Pilih menu""")
            bot.register_next_step_handler(sent, reply_adm_back)

        if call.data == "add_server":
            server_z = dbc("db",f"""SELECT * FROM serverz""").fetchall()
            list_s = list_server(server_z)
            count_server = len(server_z)
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=list_s+"\n📓 Masukan server dengan format \n`id,Region,ISP,Domain,harga` \nContoh:\n`sg1,SG,DO,sg-do.lizserver.me,10000`", parse_mode='MARKDOWN')
            def add_server(message):
                try:
                    user_i = message.text.split(",")
                    idserver = user_i[0]
                    region = user_i[1]  
                    isp = user_i[2] 
                    domain = user_i[3]  
                    harga = user_i[4]
                    len_user = len(user_i)
                    exist_id = [z[0] for z in dbc("db",f"""SELECT id FROM serverz""").fetchall()]
                    print(len_user)
                    if idserver not in exist_id and len_user == 5:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Add domain: `{domain}` Success!!""", parse_mode="MARKDOWN")
                        bot.delete_message(message.chat.id, message.id)
                        dbc("db",f"""INSERT INTO serverz (id,region,isp,domain,harga) VALUES ('{idserver}','{region}','{isp}','{domain}','{harga}')""")
                        dbc("db",f"""CREATE TABLE IF NOT EXISTS '{idserver}' (idtele varchar, username varchar, register varchar, expired varchar, status varchar)""")
                        print(f"""Register as: {domain}""")
                    else:
                        print("Format salah/id sudah terdaftar silahkan periksa ulang..")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""ID server sudah terdaftar/format lebih silahkan periksa add ulang.. /start untuk ke menu utama""", parse_mode="MARKDOWN", reply_markup=keyboard_admin_add_svr)
                        bot.delete_message(message.chat.id, message.id)
                except:
                    print("Format salah silahkan periksa ulang..")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""`Format salah silahkan periksa ulang..`""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin_add_svr)
                    bot.delete_message(message.chat.id, message.id)
                    
            bot.register_next_step_handler(sent, add_server)

        if call.data == "edit_server":
            print("ini edit server")
            server_z = dbc("db",f"""SELECT * FROM serverz""").fetchall()
            list_s = list_server(server_z)
            count_server = len(server_z)
            exist_id = [z[0] for z in dbc("db",f"""SELECT id FROM serverz""").fetchall()]
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=list_s+"\nEdit server dengan format \n`id,Region,ISP,Domain,harga` \nContoh:\n`sg1,SG,DO,sg-do.lizserver.me,10000`", parse_mode='MARKDOWN')
            def edit_server(message):
                try:
                    user_i = message.text.split(",")
                    idinput = user_i[0]  
                    region = user_i[1] 
                    isp = user_i[2]
                    domain = user_i[3] 
                    harga = user_i[4]
                    msg_count = len(user_i)
                    saldo_akhir = rupiah_format(harga)
                    # print(type(msg_count))
                    if idinput in exist_id and msg_count == 5:
                        print("input lengkap..")                        
                        dbc("db",f"""UPDATE serverz SET region = '{region}', isp = '{isp}', domain = '{domain}', harga = '{harga}' WHERE id = '{idinput}'""")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Server Id: {idinput}\nRegion: {region}\nISP: {isp}\nDomain: `{domain}`\nHarga: {saldo_akhir}\nBerhasil di edit.. """, parse_mode='MARKDOWN')
                        bot.delete_message(message.chat.id, message.id)
                    else:
                        print("input lebih..")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format lebih Silahkan ulangi.. /admin untuk menu utama""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin_edit_svr)
                        bot.delete_message(message.chat.id, message.id)
                except:
                    print("Format salah/kurang..")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format Salah/Kurang Silahkan ulangi.. /admin untuk menu utama""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin_edit_svr)
                    bot.delete_message(message.chat.id, message.id)
                    
            bot.register_next_step_handler(sent, edit_server)

        if call.data == "delete_server":
            print("ini Delete Server")
            server_z = dbc("db",f"""SELECT * FROM serverz""").fetchall()
            list_s = list_server(server_z)
            count_server = len(server_z)
            exist_id = [z[0] for z in dbc("db",f"""SELECT id FROM serverz""").fetchall()]
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=list_s+"\nPilih server id yang akan di hapus.. /admin untuk menu utama.", parse_mode='MARKDOWN', reply_markup=keyboard_admin_back)
            def delete_server(message):
                user_i = message.text
                exist_id = [z[0] for z in dbc("db",f"""SELECT id FROM serverz""").fetchall()]
                count_server = len(exist_id)
                try:
                    if user_i in exist_id:
                        dbc("db",f"""DELETE FROM serverz WHERE id = '{user_i}'""")
                        dbc("db",f"""DROP TABLE '{user_i}'""")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Server Sudah di hapus..!!""", parse_mode='MARKDOWN')
                        bot.delete_message(message.chat.id, message.id)
                    else:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""ID yang anda pilih tidak ada di daftar pilih ulang server..""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin_delete_svr)
                        bot.delete_message(message.chat.id, message.id)
                except:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Masukan hanya ada di pilihan daftar silahkan pilih ulang server..""", parse_mode='MARKDOWN' , reply_markup=keyboard_admin_delete_svr)
                    bot.delete_message(message.chat.id, message.id)
                    
            bot.register_next_step_handler(sent, delete_server)

        if call.data == "topup_member":
            print("ini topup")
            userz_list = dbc("db",f"""SELECT * FROM userz""").fetchall()
            exist = [z[1] for z in dbc("db","SELECT * FROM userz").fetchall()]
            member_l = member_list(userz_list)
            count_server = len(userz_list)
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=member_l+"\n📓 Masukan username + saldo yang ini akan topup \nContoh:\n`lizsvr,100000`", parse_mode='MARKDOWN')
            def add_saldo(message):
                try:
                    user_i = message.text.split(",")
                    username = user_i[0]
                    saldo = user_i[1]
                    print(exist)
                    if username in exist and int(saldo):
                        saldo_awal = dbc("db",f"""SELECT saldo FROM userz WHERE username = '{username}'""").fetchone()[0]
                        saldo_ = (int(saldo_awal) + int(saldo))
                        saldo_akhir = rupiah_format(saldo_)
                        saldo_input = rupiah_format(saldo)
                        dbc("db",f"""UPDATE userz SET saldo = '{saldo_}' WHERE username = '{username}'""")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Topup Saldo {username} {saldo_input} berhasil.. Total saldo {saldo_akhir}""", parse_mode='MARKDOWN')
                        bot.delete_message(message.chat.id, message.id)
                        print("saldo berhasil di update")
                    else:
                        print("bukan angka")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Username/input saldo salah Silahkan Ulangi /admin untuk menu utama..""", parse_mode='MARKDOWN', reply_markup=keyboard_admin_topup_acc)
                        bot.delete_message(message.chat.id, message.id)
                except:
                    print("input salah")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""input saldo salah Silahkan Ulangi /admin untuk menu utama...""", parse_mode='MARKDOWN', reply_markup=keyboard_admin_topup_acc)
                    bot.delete_message(message.chat.id, message.id)

            bot.register_next_step_handler(sent, add_saldo)

        if call.data == "menu":
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Silahkan pilih menu di bawa \n""", reply_markup=keyboard_list_menu)

        if call.data == "back":
            username_m = dbc("db",f"""SELECT username FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
            saldo_awal = dbc("db",f"""SELECT saldo FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
            reg_date = dbc("db",f"""SELECT dateRegister FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
            saldo_akhir = rupiah_format(saldo_awal)
            # print(saldo_akhir)
            text = f"""Selamat datang di Liz SSH premium!!\nHallo {username_m}!!\nSaldo : {saldo_akhir}\nRestered: {reg_date}\nID anda : `{teleid}`"""
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text ,parse_mode='markdown', reply_markup=keyboard_m)

        if call.data == "add_acc":
            print("ini add acc")
            server_z = dbc("db",f"""SELECT * FROM serverz""").fetchall()
            list_s = list_server(server_z)
            count_server = len(server_z)
            sent_l = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""{list_s}\nPilih dari [ 1 - {count_server} ]""", parse_mode='markdown')
            def input_ssh(message):
                # print(message)
                user_in = message.text
                exist_id = [z[0] for z in dbc("db",f"""SELECT id FROM serverz""").fetchall()]
                if user_in in exist_id:
                    print("angka ada ada di dalam list")
                    sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Silahkan masukan \nUsername + password\n Contoh: \n`lizadm,123`""", parse_mode='markdown')
                    bot.delete_message(message.chat.id, message.id)
                    def create_ssh(message):
                        try:
                            user_i = message.text.split(",")
                            username = user_i[0]
                            password = user_i[1]
                            id_ = dbc("db",f"""SELECT id FROM serverz WHERE id = '{user_in}'""").fetchone()[0]
                            domain = dbc("db",f"""SELECT domain FROM serverz WHERE id = '{user_in}'""").fetchone()[0]
                            harga = dbc("db",f"""SELECT harga FROM serverz WHERE id = '{user_in}'""").fetchone()[0]
                            saldo_akun = dbc("db",f"""SELECT saldo FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
                            exist_uname = [z[0] for z in dbc("db",f"""SELECT username FROM '{user_in}' WHERE status = '{status_active}'""").fetchall()]
                            ip_server = socket.gethostbyname(domain)
                            len_msg = len(user_i)
                            print(user_i)
                            if int(saldo_akun) < int(harga):
                                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Saldo anda tidak cukup Silahkan topup""", parse_mode='markdown')
                                bot.delete_message(message.chat.id, message.id)
                            elif str(len_msg) >= "3":
                                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format input lebih""", parse_mode='markdown')
                                bot.delete_message(message.chat.id, message.id)
                            elif username in exist_uname:
                                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Username sudah terdaftar""", parse_mode='markdown', reply_markup=keyboard_add_acc)
                                bot.delete_message(message.chat.id, message.id)
                            else:
                                url = "http://"+domain+f":6969/adduser/exp?user={username}&password={password}&exp=30"
                                headers = ({'AUTH_KEY':AUTH_KEY })
                                today = DT.date.today()
                                exp = "31"
                                exp = datetime.datetime.today() + datetime.timedelta(days=int(exp))
                                exp = exp.strftime("%Y-%m-%d")
                                try:
                                    requests.get(url, headers=headers, timeout=3)
                                    output_req = server_out(ip_server,domain,username,password,today,exp)
                                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=output_req, parse_mode='markdown')
                                    bot.delete_message(message.chat.id, message.id)
                                    dbc("db",f"""UPDATE userz SET saldo = '{str(int(saldo_akun) - int(harga))}' WHERE idtele = '{teleid}'""")
                                    dbc("db",f"""INSERT INTO '{user_in}' (idtele,username,register,expired,status) VALUES ('{teleid}','{username}','{today}','{exp}','{status_active}')""")
                                except:
                                    print("API Belum terinstall")
                                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Error server tidak terhubung dengan API bot", parse_mode='markdown')
                                    bot.delete_message(message.chat.id, message.id)
                        except:
                            print("tidak ada")
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Input salah atau Api tidak terhubung dengan server /start untuk ke menu utama """, parse_mode='markdown', reply_markup=keyboard_add_acc )
                            bot.delete_message(message.chat.id, message.id)
                    
                    bot.register_next_step_handler(sent, create_ssh)

                else:
                    print(f"Angka tidak ada di dalan list {user_in}")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Id server tidak ada di list Silahkan ulangi atau /start untuk ke menu utama """, parse_mode='markdown', reply_markup=keyboard_add_acc )
                    bot.delete_message(message.chat.id, message.id)

            bot.register_next_step_handler(sent_l, input_ssh)

        if call.data == "dell_acc":
            print("ini dell acc")
            server_z = dbc("db",f"""SELECT * FROM serverz""").fetchall()
            list_s = list_server(server_z)
            count_server = len(server_z)
            sent_l = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Pilih server yang akan di Hapus\n{list_s}\nPilih dari [ 1 - {count_server} ]\n""", parse_mode='markdown')
            def delete_ssh(message):
                user_in = message.text
                exist_id = [z[0] for z in dbc("db",f"""SELECT id FROM serverz""").fetchall()]
                if user_in in exist_id:
                    print("angka ada ada di dalam list")
                    ssh_z = dbc("db",f"""SELECT * FROM '{user_in}' WHERE idtele = '{teleid}'""").fetchall()
                    domain = dbc("db",f"""SELECT domain FROM serverz WHERE id = '{user_in}'""").fetchone()[0]
                    ssh_list = member_ssh(ssh_z)
                    print(ssh_z)
                    sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Silahkan masukan Username yang ada di list \n{ssh_list}""", parse_mode='markdown')
                    bot.delete_message(message.chat.id, message.id)
                    def create_ssh(message):
                        ssh_z = dbc("db",f"""SELECT * FROM '{user_in}' WHERE idtele = '{teleid}'""").fetchall()
                        exist_uname = [z[0] for z in dbc("db",f"""SELECT username FROM '{user_in}' WHERE status = '{status_active}'""").fetchall()]
                        user_i = message.text
                        len_msg = len(user_i)
                        url = "http://"+domain+f":6969/deluser?user={user_i}"
                        headers = ({'AUTH_KEY':AUTH_KEY })
                        if user_i in exist_uname:
                            try:
                                requests.get(url, headers=headers, timeout=3)
                                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""User id {user_i} Berhasil di hapus /start untuk ke menu""", parse_mode='markdown')
                                bot.delete_message(message.chat.id, message.id)
                                dbc("db",f"""DELETE FROM '{user_in}' WHERE username = '{user_i}'""")
                            except:
                                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Api server tidak terhubung /start untuk ke menu""", parse_mode='markdown')
                                bot.delete_message(message.chat.id, message.id)
                        else:
                            print("username tidak ada")
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""User id {user_i} Tidak terdatar /start untuk ke menu""", parse_mode='markdown')
                            bot.delete_message(message.chat.id, message.id)
                    bot.register_next_step_handler(sent, create_ssh)
                else:
                    print(f"Angka tidak ada di dalan list {user_in}")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Id server tidak ada di list Silahkan ulangi atau /start untuk ke menu utama """, parse_mode='markdown', reply_markup=keyboard_dell_acc )
                    bot.delete_message(message.chat.id, message.id)
            bot.register_next_step_handler(sent_l, delete_ssh)

        if call.data == "list_acc":
            print("ini list account")
            server_z = dbc("db",f"""SELECT * FROM serverz""").fetchall()
            list_s = list_server(server_z)
            count_server = len(server_z)
            sent_l = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""{list_s}\nPilih dari [ 1 - {count_server} ]\n""", parse_mode='markdown')
            def list_ssh_member(message):
                user_in = message.text
                exist_id = [z[0] for z in dbc("db",f"""SELECT id FROM serverz""").fetchall()]
                if user_in in exist_id:
                    print("angka ada ada di dalam list")
                    ssh_z = dbc("db",f"""SELECT * FROM '{user_in}' WHERE idtele = '{teleid}'""").fetchall()
                    domain = dbc("db",f"""SELECT domain FROM serverz WHERE id = '{user_in}'""").fetchone()[0]
                    ssh_list = member_ssh(ssh_z)
                    print(ssh_z)
                    sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""List member `{domain}` \n{ssh_list}""", parse_mode='markdown')
                    bot.delete_message(message.chat.id, message.id)
                else:
                    print(f"Angka tidak ada di dalan list {user_in}")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Id server tidak ada di list Silahkan ulangi atau /start untuk ke menu utama """, parse_mode='markdown', reply_markup=keyboard_dell_acc )
                    bot.delete_message(message.chat.id, message.id)
            bot.register_next_step_handler(sent_l, list_ssh_member)

        if call.data == "cpass":
            print("ini ganti pass")
            sent_l = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Silahkan masukan password saat ini""", parse_mode='markdown')
            def change_pw(message):
                print("input password")
                user_in = message.text
                pw_z = [z[0] for z in dbc("db",f"""SELECT password FROM userz WHERE idtele = '{teleid}'""").fetchall()]
                # pw_z = dbc("db",f"""SELECT password FROM userz WHERE idtele = '{teleid}'""").fetchone()
                print(user_in, pw_z)
                if user_in in pw_z:
                    sent_l = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Silahkan masukan password baru..""", parse_mode='markdown')
                    bot.delete_message(message.chat.id, message.id)
                    print("password benar")
                    def new_pw(message):
                        print(message.text)
                        pw_new = message.text
                        dbc("db",f"""UPDATE userz SET password = '{pw_new}' WHERE idtele = '{teleid}'""")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Password berhasil di update /start untuk menu utama""", parse_mode='markdown')
                        bot.delete_message(message.chat.id, message.id)
                    bot.register_next_step_handler(sent_l, new_pw)
                else:
                    print("passwordn salah")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Passowrd tidak sama..silahkan ulangi..""", parse_mode='markdown', reply_markup=keyboard_settings)
                    bot.delete_message(message.chat.id, message.id)
                
            bot.register_next_step_handler(sent_l, change_pw)

            

if __name__ == '__main__':
    try:
        print("Initializing Database...")
        db = create_engine(database, pool_pre_ping=True)
        dbc("db","CREATE TABLE IF NOT EXISTS userz (idtele varchar, username varchar, password varchar, saldo varchar DEFAULT 0, status varchar, dateRegister varchar DEFAULT 0)")
        dbc("db","CREATE TABLE IF NOT EXISTS transaksi (idsvr varchar, username varchar, tanggal varchar, akun varchar, harga varchar, status varchar)")
        dbc("db","CREATE TABLE IF NOT EXISTS serverz (id varchar, region varchar, isp varchar, domain varchar, harga varchar, totalakun varchar DEFAULT 0)")
        dbc("db","CREATE TABLE IF NOT EXISTS admin (idtele varchar, username varchar, password varchar, status varchar)")
        dbc("db",f"""INSERT INTO admin (idtele,username,password,status) VALUES ('{ADMIN_ID}','{ADMIN_USERNAME}','{ADMIN_PASSWORD}','{status_register}')""")
        print("Connected to the database")
        print("Bot Started")
        bot.infinity_polling()
    except Exception as error:
        print('Cause: {}'.format(error))