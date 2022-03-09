import sqlite3 as dbapi
def vse_ekipe_sezona(conn,sezona):
    curr = conn.cursor()
    poizvedba = '''SELECT DISTINCT ime
                      FROM klub
                           JOIN
                           ekipa ON ekipa.klub = klub.id
                     WHERE sezona = ?;'''
    curr.execute(poizvedba,[sezona])
    podatki = curr.fetchall()
    return podatki

def vse_ekipe(conn):
    curr = conn.cursor()
    poizvedba = '''SELECT ime
                   FROM klub;'''
    curr.execute(poizvedba)
    podatki = curr.fetchall()
    return podatki

def vsi_stadioni(conn):
    curr = conn.cursor()
    poizvedba = '''SELECT ime
                      FROM stadion;'''
    curr.execute(poizvedba)
    podatki = curr.fetchall()
    return podatki

def najbolsi_strelci_vsa_leta(conn):
    curr = conn.cursor()
    poizvedba = '''SELECT ime,
                       count( * ) 
                  FROM zadetek
                       JOIN
                       igralec ON igralec.id = zadetek.igralec
                 GROUP BY igralec.id
                 ORDER BY COUNT( * ) DESC;'''
    curr.execute(poizvedba)
    podatki = curr.fetchall()
    return podatki

def goli_igralec(conn,igralec):
    curr = conn.cursor()
    poizvedba = '''SELECT ime,
                       sezona,
                       COUNT( * ) 
                  FROM zadetek
                       JOIN
                       igralec ON igralec.id = zadetek.igralec
                       JOIN
                       tekma ON tekma.id = zadetek.tekma
                 WHERE ime = ?
                 GROUP BY ime,
                          sezona
                 ORDER BY COUNT( * ) DESC;'''
    curr.execute(poizvedba,[igralec])
    podatki = curr.fetchall()
    return podatki

# POPRAVI, V    SQL DELA TUKAJ NEVEM ZAKAJ NE
# def tekme_v_eni_sezoni(conn,sezona):
#     curr = conn.cursor()
#     poizvedba = '''SELECT sezona,stadion,tip,kl1.ime,kl2.ime
#                   FROM tekma
#                        JOIN
#                        igra_klub AS k1 ON tekma.id = k1.tekma
#                        JOIN
#                        igra_klub AS k2 ON (tekma.id = k2.tekma AND 
#                                            k1.klub <> k2.klub) 
#                        join klub as kl1 on (k1.klub = kl1.id)
#                        join klub as kl2 on (k2.klub = kl2.id)
#                  WHERE tekma.sezona = ? and k1.tip = 'domaci';'''
#     curr.execute(poizvedba,[sezona])
#     podatki = curr.fetchall()
#     return podatki
    

    
 
    
    
    
