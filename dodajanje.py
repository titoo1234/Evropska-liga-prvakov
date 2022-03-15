import json
import os
import sqlite3 as dbapi

def najdi_klub_id(conn, klub):
    '''
    poišče id kluba 'klub'    
    '''
    poizvedba = '''
    SELECT id from klub WHERE ime = ?
    '''
    klub_id = conn.execute(poizvedba, [klub])
    klub_id = klub_id.fetchall()[0][0]
    return klub_id

def najdi_igralec_id(conn, igralec):
    '''
    poišče id igralca 'gralec'
    '''
    poizvedba = '''
    SELECT id from igralec WHERE ime = ?
    '''
    igralec_id = conn.execute(poizvedba, [igralec])
    igralec_id = igralec_id.fetchall()[0][0]
    return igralec_id

def najdi_stadion_id(conn, stadion):
    '''
    poišče id stadiona 'stadion'    
    '''
    poizvedba = '''
    SELECT id from stadion WHERE ime = ?
    '''
    stadion_id = conn.execute(poizvedba, [stadion])
    stadion_id = stadion_id.fetchall()[0][0]
    return stadion_id

def najdi_tekma_id(conn, sezona, datum, stadion):
    '''
    poišče id tekme    
    '''
    sezona = "20"+str(sezona)+"/"+str(int(sezona)+1)
    stadion_id = najdi_stadion_id(conn, stadion)
    poizvedba = '''SELECT id FROM tekma WHERE sezona = ? AND datum = ? AND stadion = ?; '''
    tekma_id = conn.execute(poizvedba, [sezona, datum, stadion_id])
    tekma_id = tekma_id.fetchall()[0][0]
    return tekma_id

def dodaj_igralca1(conn, oseba):
    '''
    v bazo doda igralca 'oseba'   
    '''
    cur = conn.cursor()
    cur.execute('''
                 SELECT ime from igralec;
    ''')
    igralci = cur.fetchall()
    sql = '''
            INSERT INTO igralec
            (ime)
            VALUES
            (?)
        '''
    parametri = [oseba]
    if (oseba,) not in igralci:
        cur.execute(sql, parametri)
        
def dodaj_klub(conn, ime_kluba):
    '''
    V tabelo Klubi doda klub 'ime_kluba'    
    '''
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
    parametri = [ime_kluba]
    if (ime_kluba,) not in imena_klubov:
        conn.execute(sql, parametri)
    
    
def dodaj_ekipo(conn, sezona, klub,igralec):
    '''
    V bazo doda ekipo  
    '''
    igralec_id = najdi_igralec_id(conn, igralec)
    klub_id = najdi_klub_id(conn, klub)
    sql = '''
        INSERT INTO ekipa (sezona,klub,igralec)

        VALUES
        (?,?,?)
    '''
    sezona = "20"+str(sezona)+"/"+str(int(sezona)+1)
    parametri = [
        sezona,
        klub_id,
        igralec_id
    ]
    preveri = ''' SELECT sezona, igralec FROM ekipa; '''
    cur = conn.cursor()
    cur.execute(preveri)
    vse = cur.fetchall()
    if (sezona, igralec_id) not in vse:
        conn.execute(sql, parametri)
        
def dodaj_stadion(conn, ime_stadiona):
    '''
    V bazo doda stadion 'stadion'   
    '''
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
        
def dodaj_tekmo(conn, sezona, datum, rezultat, stadion, skupina):
    '''
    V bazo doda tekmo  
    '''
    stadion_id = najdi_stadion_id(conn, stadion)
    sezona = "20"+str(sezona)+"/"+str(int(sezona)+1)
    sql = '''
        INSERT INTO tekma (sezona,datum,rezultat,stadion, tip)

        VALUES
        (?,?,?,?,?)
    '''
    parametri = [
        sezona,
        datum,
        rezultat,
        stadion_id,
        skupina
    ]
    preveri = ''' SELECT sezona, datum, stadion FROM tekma; '''
    cur = conn.cursor()
    cur.execute(preveri)
    vse = cur.fetchall()
    if (sezona, datum, stadion_id) not in vse:
        conn.execute(sql, parametri)
    
def dodaj_igra_klub(conn, sezona, datum, klub, tip, stadion):
    '''
    V tabelo igra_klub doda tekma,sezona,klub,tip  
    '''
    tekma_id = najdi_tekma_id(conn, sezona, datum, stadion)
    sezona = "20"+str(sezona)+"/"+str(int(sezona)+1)
    sql = '''
        INSERT INTO igra_klub (tekma,sezona,klub,tip)

        VALUES
        (?,?,?,?)
    '''
    parametri = [
        tekma_id,
        sezona,
        najdi_klub_id(conn, klub),
        tip
        
    ]
    preveri = ''' SELECT tekma,tip FROM igra_klub; '''
    cur = conn.cursor()
    cur.execute(preveri)
    vse = cur.fetchall()
    if (tekma_id, tip) not in vse:
        conn.execute(sql, parametri)
    
# def dodaj_igra_igralec(conn, slovar,klub,tekma_id):
#     poizvedba = '''
#     SELECT id from klub WHERE ime = ?
#     '''
#     parametri1 = [klub]
#     klub_id = conn.execute(poizvedba, parametri1)
#     poizvedba = '''
#     SELECT id from igralec WHERE ime = ?
#     '''
#     parametri1 = [slovar['igralec']]
#     igralec_id = conn.execute(poizvedba, parametri1)
#     sql = '''
#         INSERT INTO igra_igralec (tekma,sezona,klub,igralec)
# 
#         VALUES
#         (?,?,?,?)
#     '''
#     parametri = [
#         tekma_id,
#         slovar['sezona'],
#         klub_id,
#         igralec_id
#         
#     ]
#     conn.execute(sql, parametri)
    
def dodaj_zadetek(conn, klub, igralec, minuta, sezona, datum, stadion):
    '''
    V tabelo zadetkov doda zadetek
    '''
    tekma_id = najdi_tekma_id(conn, sezona, datum, stadion)
    klub_id = najdi_klub_id(conn, klub)
    igralec_id = najdi_igralec_id(conn, igralec)
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
    preveri = ''' SELECT tekma, klub, igralec, minuta FROM zadetek; '''
    cur = conn.cursor()
    cur.execute(preveri)
    vse = cur.fetchall()
    if (tekma_id, klub_id, igralec_id, minuta) not in vse:
        conn.execute(sql, parametri) 
