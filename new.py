#!/bin/python3

import telebot, psycopg2, os
import datetime as DT

API_TOKEN = '5868093119:AAHmp1MG5NRXXtJOSNRZeoZQTE1i-IgNftk'
bot = telebot.TeleBot(API_TOKEN)
today = DT.date.today()

# Get starterd
@bot.message_handler(commands=['start'])
def any_msg(message):
    #print(message)
    teleid = str(message.from_user.id)
    exist_id = db.execute("SELECT idtele FROM userz;")
    x = exist_id.fetchall()
    #db.execute("DELETE FROM userz WHERE idtele = %s", (teleid,) )
    conn.commit()
    print(teleid, x)


##### MAIN
if __name__ == '__main__':
    try:
        print("Initializing Database...")
        # Connect to local database
        # db = create_engine(database, pool_pre_ping=True)
        conn = psycopg2.connect(host="157.245.196.93", port="5432", dbname="lizdb", user="postgres", password="1234")
        db = conn.cursor()
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
        conn.commit()
    except Exception as error:
        print('Cause: {}'.format(error))
