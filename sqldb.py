import os, telebot, datetime
from sqlalchemy import *
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import datetime as DT
# load data base
basedir = 'database/'
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")

# bot token
API_TOKEN = '5868093119:AAHmp1MG5NRXXtJOSNRZeoZQTE1i-IgNftk'
bot = telebot.TeleBot(API_TOKEN)

# all status
status_register = "register"
status_login = "login"
status_logout = "logout"

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

@bot.message_handler(commands=['start'])
def any_msg(message):
    # print(message)
    teleid = str(message.from_user.id)
    exist_id = [z[0] for z in dbc("db","SELECT idtele FROM userz").fetchall()]
    exist_user = [z[0] for z in dbc("db","SELECT username FROM userz").fetchall()]
    print("Teleid /start:",teleid)
    if teleid in exist_id:
        print("ada")
        sts_r = dbc("db",f"""SELECT status FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
        username_m = dbc("db",f"""SELECT username FROM userz WHERE idtele = '{teleid}'""").fetchone()[0]
        if sts_r == status_register:
            bot.send_message(message.chat.id, "Silahkan Login Terlebih Dahulu", reply_markup=keyboard_r)
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
            text = f"""Selamat datang di Liz SSH premium!!\nHallo {username_m}😃\nSaldo: {saldo_akhir}\nRestered: 30/01/2023\nemail : -none\nAccount SSH : 0"""
            bot.send_message(message.chat.id, text=text ,parse_mode='markdown', reply_markup=keyboard_m)
    else:
        print("user belum registrasi")
        bot.send_message(message.chat.id, "Silahkan Register Terlebih Dahulu", reply_markup=keyboard_r)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        teleid = str(call.message.chat.id)
        if call.data == "register":
            # with db.engine.begin() as conn:
            # dbc("db",f"""INSERT INTO userz (idtele, username) VALUES ({teleid}, '{uname}')""")
            sent = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format Register 'R-username-passwd'""")
            today = DT.date.today()
            def register_p(message):
                try:
                    user_i = message.text.split("-")
                    # req_ = user_i[0] # The second (0) element is the telegramID
                    username = user_i[0] # The second (1) element is the username
                    password = user_i[1] # The second (2) element is the pawssword
                    user_log = message.chat.first_name
                    len_user = len(user_i)
                    uang = "239000"
                    # exist_u = [z[0] for z in  dbc("db","SELECT username FROM userz").fetchall()]
                    print(user_i)
                    # dbc("db",f"""INSERT INTO userz (idtele, username, saldo, password, status) VALUES ({teleid}, '{username}', '{uang}', '{password}', '{status_register}')""")
                    if len_user == 2:
                        print("format benar")
                    else:
                        print("format salah")

            #         if req_ == "R":
            #             if not username:
            #                 print("Invalid Username")
            #             elif not password:
            #                 print("Invalid password")
            #             elif username in exist_u:
            #                 bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Username already existed..""")
            #                 bot.delete_message(message.chat.id, message.id)
            #                 print("username Already Exist")
            #             else:
            #                 bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Registrasi {username} Success!! Silahkan login""", reply_markup=keyboard_l)
            #                 bot.delete_message(message.chat.id, message.id)
            #                 dbc("db",f"""INSERT INTO userz (idtele) VALUES ({teleid})""")
            #                 # db.execute("INSERT INTO userz (idtele,username,password,status,dateRegister) VALUES (?,?,?,?,?);", (teleid, username,password,status_register,today))
            #                 print(f"""Register as: {user_log}""")
            #         else:
            #             print("Gunakan 'R'-username-paswd untuk register")
            #             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Gunakan 'R'-username-paswd untuk register""")
            #             bot.delete_message(message.chat.id, message.id)
                except:
                    print("error")
            #         print("Format Register salah!!")
            #         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Format Register salah Silahkan ulangi /start""")
            #         bot.delete_message(message.chat.id, message.id)
            #     return
            bot.register_next_step_handler(sent, register_p)



if __name__ == '__main__':
    try:
        print("Initializing Database...")
        # Connect to local database
        db = create_engine(database, pool_pre_ping=True)
        dbc("db","CREATE TABLE IF NOT EXISTS userz (idtele varchar, username varchar, password varchar, saldo varchar DEFAULT 0, status varchar, dateRegister varchar DEFAULT 0)")
        dbc("db","CREATE TABLE IF NOT EXISTS transaksi (username varchar, tanggal varchar, akun varchar, harga varchar, status varchar)")
        dbc("db","CREATE TABLE IF NOT EXISTS serverz (id INTEGER PRIMARY KEY, region varchar, isp varchar, domain varchar, harga varchar, totalakun varchar DEFAULT 0)")
        dbc("db","CREATE TABLE IF NOT EXISTS admin (idtele varchar, username varchar, password varchar, status varchar)")
        print("Connected to the database")
        print("Bot Started")
        bot.infinity_polling()

    except Exception as error:
        print('Cause: {}'.format(error))