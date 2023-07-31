from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import select, table, column
import psycopg2

db = create_engine('postgresql+psycopg2://postgres:1234@db.lizserver.me/lizdb')
con = psycopg2.connect(host='localhost', port='5432', database='lizdb', user='postgres',password='1234')

z = "SELECT * FROM userz;"
sv = "sg-do.lizserver.me"

with db.begin() as conn:
    result = conn.execute(text("SELECT domain FROM serverz"))
    #conn.execute(text("INSERT INTO userz (username) VALUES ('lizadm')"))
    conn.commit()
    #print(result)

foo = table("serverz", column("domain"))

with db.connect() as connection:
    # use connection.execute(), not engine.execute()
    # select() now accepts column / table expressions positionally
    result = connection.execute(select(foo.c.domain))
    rs = result.fetchall()
    #print(rs)
    #if sv in rs:
    #    print("ada")
    #else:
    #    print("tidak ada")

with con:
    cur = con.cursor()
    y = con.cursor()
    cur.execute('SELECT domain FROM serverz;')
    y.execute('SELECT harga FROM serverz;')
    version = cur.fetchall()
    yy = y.fetchall()
    i = [z[0] for z in version]
    yyy = [z[0] for z in yy]
    print(yyy)
    print(version)
    if sv in i:
        print("ada")
    else:
        print("tidak ada")
