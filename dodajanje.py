import json
import os
import sqlite3 as dbapi



def dodaj_igralca(conn, oseba):

    cur = conn.cursor()
    cur.execute('''
                 SELECT ime from igralec;
    ''')
    igralci = cur.fetchall()
    if (oseba,) not in igralci:
        sql = '''
            INSERT INTO igralec
            (ime)
            VALUES
            (?)
        '''
        parametri = [
            oseba
        ]
        cur.execute(sql, parametri)
def dodaj_klub(conn, ime_kluba):
    cur = conn.cursor()
    cur.execute('''
                 SELECT ime from klub;
    ''')
    imena_klubov = cur.fetchall()
    sql = '''
        INSERT INTO klub
        (ime)
        VALUES
        (?)
    '''
    parametri = [
        ime_kluba
    ]
    if (ime_kluba,) not in imena_klubov:
        conn.execute(sql, parametri)
    
    
def dodaj_ekipo(conn, sezona,klub,igralec):
    poizvedba = '''
    SELECT id from igralec WHERE ime = ?
    '''
    parametri1 = igralec
    igralec_id = conn.execute(poizvedba, parametri1)
    poizvedba = '''
    SELECT id from klub WHERE ime = ?
    '''
    parametri1 = klub
    klub_id = conn.execute(poizvedba, parametri1)
    sql = '''
        INSERT INTO ekipa (sezona,klub,igralec)

        VALUES
        (?,?,?)
    '''
    parametri = [
        sezona,
        klub_id,
        igralec_id
    ]
    conn.execute(sql, parametri)
def dodaj_stadion(conn, ime_stadiona):
    sql = '''
        INSERT INTO stadion (ime)

        VALUES
        (?)
    '''
    cur = conn.cursor()
    cur.execute("SELECT ime FROM stadion;")
    stadioni = cur.fetchall()
    parametri = [
        ime_stadiona
    ]
    if (ime_stadiona,) not in stadioni:
        conn.execute(sql, parametri)
def dodaj_tekmo(conn, slovar):
    poizvedba = '''
    SELECT id from stadion WHERE ime = ?
    '''
    parametri1 = [slovar['stadion']]
    stadion_id = conn.execute(poizvedba, parametri1)
    sql = '''
        INSERT INTO tekma (sezona,datum,stadion)

        VALUES
        (?,?,?)
    '''
    parametri = [
        slovar['sezona'],
        slovar['datum'],
        stadion_id#morma poiskati id
    ]
    conn.execute(sql, parametri)
    
def dodaj_igra_klub(conn,slovar, klub,id_tekme):
    poizvedba = '''
    SELECT id from klub WHERE ime = ?
    '''
    parametri1 = [klub]
    klub_id = conn.execute(poizvedba, parametri1)
    sql = '''
        INSERT INTO igra_klub (tekma,sezona,klub,tip)

        VALUES
        (?,?,?,?)
    '''
    parametri = [
        id_tekme,
        slovar['sezona'],
        klub_id,
        'domači'
        
    ]
    conn.execute(sql, parametri)
def dodaj_igra_igralec(conn, slovar,klub,tekma_id):
    poizvedba = '''
    SELECT id from klub WHERE ime = ?
    '''
    parametri1 = [klub]
    klub_id = conn.execute(poizvedba, parametri1)
    poizvedba = '''
    SELECT id from igralec WHERE ime = ?
    '''
    parametri1 = [slovar['igralec']]
    igralec_id = conn.execute(poizvedba, parametri1)
    sql = '''
        INSERT INTO igra_igralec (tekma,sezona,klub,igralec)

        VALUES
        (?,?,?,?)
    '''
    parametri = [
        tekma_id,
        slovar['sezona'],
        klub_id,
        igralec_id
        
    ]
    conn.execute(sql, parametri)
    
def dodaj_zadetek(conn, slovar,klub,tekma_id,minuta):
    poizvedba = '''
    SELECT id from klub WHERE ime = ?
    '''
    parametri1 = [klub]
    klub_id = conn.execute(poizvedba, parametri1)
    poizvedba = '''
    SELECT id from igralec WHERE ime = ?
    '''
    parametri1 = [slovar['igralec']]
    igralec_id = conn.execute(poizvedba, parametri1)
    sql = '''
        INSERT INTO zadetek (tekma,klub,igralec,minuta)

        VALUES
        (?,?,?,?)
    '''
    parametri = [
        tekma_id,
        klub_id,
        igralec_id,
        minuta
    ]
    conn.execute(sql, parametri) 
