from sqlite3 import *
def stvori_bazu():
        b=connect('rijeci.sqlite3')
        c=b.cursor()
        upit='''CREATE TABLE Riječi(
          ID INTEGER PRIMARY KEY AUTOINCREMENT,
          Riječ TEXT NOT NULL)'''
        c.execute(upit)
        b.commit()
        b.close()

def dodaj_riječ(rijec):
    conn=connect('rijeci.sqlite3')
    c=conn.cursor()
    upit='''INSERT INTO Riječi
            (Riječ)
            VALUES ("{}")
         '''.format(rijec)
    c.execute(upit)   
    conn.commit()
    conn.close()
while 1==1:
        a=input('Unesi riječ: ')
        a=a.upper()
        dodaj_riječ(a)
        print('Riječ uspješno dodana u bazu')

