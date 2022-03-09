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
 
    
    
    
