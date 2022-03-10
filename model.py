import sqlite3 as dbapi


class Igralec:
    def __init__(self, ide, ime):
        self.id = ide
        self.ime = ime
        
    def __str__(self):
        return self.ime
    
    def koliko_golov(self, conn):
        curr = conn.cursor()
        poizvedba = '''SELECT 
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
        curr.execute(poizvedba,[self.ime])
        podatki = curr.fetchall()
        return podatki
    
    def koliko_golov_skupno(self, conn):
        curr = conn.cursor()
        poizvedba = '''SELECT COUNT( * ) 
                      FROM zadetek
                       JOIN
                       igralec ON igralec.id = zadetek.igralec
                       JOIN
                       tekma ON tekma.id = zadetek.tekma
                         WHERE ime = ?
                         GROUP BY ime
                         ORDER BY COUNT( * ) DESC;'''
        curr.execute(poizvedba,[self.ime])
        podatki = curr.fetchall()
        return podatki
    
    @staticmethod
    def najbolsi_strelci_vsa_leta(conn, koliko):
        curr = conn.cursor()
        poizvedba = '''SELECT ime,
                           count( * ) 
                      FROM zadetek
                           JOIN
                           igralec ON igralec.id = zadetek.igralec
                     GROUP BY igralec.id
                     ORDER BY COUNT( * ) DESC LIMIT ?;'''
        curr.execute(poizvedba, [koliko])
        podatki = curr.fetchall()
        return podatki
    
    
class Tekma:
    def __init__(self, sezona, datum, stadion, tip, domaci, gostje, rezultat):
        self.sezona = sezona
        self.datum = datum
        self.stadion = stadion
        self.tip = tip
        self.domaci = domaci
        self.gostje = gostje
        self.rezultat = rezultat
        
    def __str__(self):
        return f"{self.sezona}, {self.datum}, {self.tip}, {self.domaci} {self.rezultat} {self.gostje}, {self.stadion}"
    
    @staticmethod
    def tekme_v_eni_sezoni(conn,sezona):
        curr = conn.cursor()
        poizvedba = '''SELECT 
            tekma.datum,
           stadion.ime,
           tekma.tip,
           kl1.ime,
           kl2.ime,
           tekma.rezultat
      FROM tekma
           JOIN
           igra_klub AS k1 ON tekma.id = k1.tekma
           JOIN
           igra_klub AS k2 ON (tekma.id = k2.tekma AND 
                               k1.klub <> k2.klub) 
           JOIN
           klub AS kl1 ON (k1.klub = kl1.id) 
           JOIN
           klub AS kl2 ON (k2.klub = kl2.id) 
           JOIN
           stadion ON tekma.stadion = stadion.id
     WHERE tekma.sezona = ? AND 
           k1.tip = 'domaci';'''
        tab = []
        curr.execute(poizvedba,[sezona])
        podatki = curr.fetchall()
        for datum, stadion, tip, domaci, gostje, rezultat in podatki:
            tab.append(Tekma(sezona, datum, stadion, tip, domaci, gostje, rezultat))
        return tab
    
    
class Klub:
    def __init__(self, ide, ime):
        self.id = ide
        self.ime = ime
        
    def __str__(self):
        return self.ime
    
    @staticmethod
    def vsi_klubi(conn):
        curr = conn.cursor()
        poizvedba = '''SELECT id,ime
                       FROM klub;'''
        curr.execute(poizvedba)
        podatki = curr.fetchall()
        tab = []
        for ide, ime in podatki:
            tab.append(Klub(ide, ime))
        return tab
        
    @staticmethod
    def vsi_klubi_sezona(conn, sezona):
        curr = conn.cursor()
        poizvedba = '''SELECT DISTINCT id,ime
                          FROM klub
                               JOIN
                               ekipa ON ekipa.klub = klub.id
                         WHERE sezona = ?;'''
        curr.execute(poizvedba,[sezona])
        podatki = curr.fetchall()
        tab = []
        for ide, ime in podatki:
            tab.append(Klub(ide,ime))
        return tab

class Stadion:
    def __init__(self, ide, ime):
        self.id = ide
        self.ime = ime
        
    def __str__(self):
        return self.ime
    
    @staticmethod
    def vsi_stadioni(conn):
        curr = conn.cursor()
        poizvedba = '''SELECT id,ime
                          FROM stadion;'''
        curr.execute(poizvedba)
        podatki = curr.fetchall()
        tab = []
        for ide, ime in podatki:
            tab.append(Stadion(ide, ime))
        return tab



def vse_sezone(conn):
    curr = conn.cursor()
    poizvedba = '''SELECT DISTINCT sezona
                          FROM tekma;'''
    curr.execute(poizvedba)
    podatki = curr.fetchall()
    return podatki
    