
import sqlite3 as dbapi
def ustvari_bazo():
    ime_db = 'vaja_seminarska_v3.db'
    ime_skripte = 'ustvari_bazo_v2.txt'
    pov = dbapi.connect(ime_db)
    cur = pov.cursor()
    with open(ime_skripte, 'r') as datoteka:
        skripta_sql = datoteka.read()
    cur.executescript(skripta_sql)
    pov.commit()
    cur.close()
    pov.close()
if __name__=='__main__':
    ustvari_bazo()