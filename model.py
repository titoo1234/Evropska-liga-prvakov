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
                          sezona;'''
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
    
    @staticmethod
    def vsi_igralci(conn):
        curr = conn.cursor()
        poizvedba = '''SELECT ime
                      FROM igralec;'''
        curr.execute(poizvedba)
        podatki = curr.fetchall()
        return podatki
    @staticmethod
    def dodaj_igralca(conn, oseba):
        cur = conn.cursor()
        sql = '''
                INSERT INTO igralec
                (ime)
                VALUES
                (?)
            '''
        parametri = [oseba]
        cur.execute(sql, parametri)
        conn.commit()
#         cur.commit()
    
    
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
    def zmagovalec_finala(self):
        '''zgolj za določitev zmagovalca finala'''
        if self.rezultat[0] > self.rezultat[2]:
            return self.domaci
        return self.gostje
    
    
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
    def najvec_zadetkov_klubi(conn, koliko):
        curr = conn.cursor()
        poizvedba = '''SELECT ime,
                           count( * ) 
                      FROM zadetek
                           JOIN
                           klub ON klub.id = zadetek.klub
                     GROUP BY klub.id
                     ORDER BY COUNT( * ) DESC LIMIT ?;'''
        curr.execute(poizvedba, [koliko])
        podatki = curr.fetchall()
        return podatki
        
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
    
    @staticmethod
    def domaci_stadion(conn, ime):
        curr = conn.cursor()
        poizvedba = '''SELECT stadion.ime
  FROM klub
       JOIN
       igra_klub ON klub.id = igra_klub.klub
       JOIN
       tekma ON igra_klub.tekma = tekma.id
       JOIN
       stadion ON tekma.stadion = stadion.id
 WHERE igra_klub.tip = 'domaci' and klub.ime = ?
 GROUP BY klub.ime
 ORDER BY count(stadion.ime) DESC;'''
        curr.execute(poizvedba,[ime])
        podatki = curr.fetchall()
        return podatki
    
    @staticmethod
    def koliko_golov(conn, ime_kluba):
        curr = conn.cursor()
        poizvedba = '''SELECT sezona,
       COUNT( * ) 
  FROM zadetek
       JOIN
       klub ON klub.id = zadetek.klub
       JOIN
       tekma ON tekma.id = zadetek.tekma
 WHERE klub.ime = ?
 GROUP BY klub.ime,
          sezona;'''
        curr.execute(poizvedba,[ime_kluba])
        podatki = curr.fetchall()
        return podatki
    @staticmethod
    def dodaj_klub(conn, ime_kluba):
        cur = conn.cursor()
        sql = '''
            INSERT INTO klub
            (ime)
            VALUES
            (?)
        '''
        parametri = [ime_kluba]
        conn.execute(sql, parametri)
        conn.commit()
    

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
                  FROM tekma
                 ORDER BY sezona;'''
    curr.execute(poizvedba)
    podatki = curr.fetchall()
    return podatki
def je_finale(conn,sezona):
    sezona = "20"+str(sezona)+"/"+str(sezona+1)
    curr = conn.cursor()
    poizvedba = '''SELECT *
                      FROM tekma
                     WHERE tip = 'FINALE' AND 
                           sezona = ?;'''
    curr.execute(poizvedba,[sezona])
    podatki = curr.fetchall()
    if len(podatki) > 0:
        return True
    return False
def koliko_golov_sezona(conn,sezona):
    curr = conn.cursor()
    poizvedba = '''SELECT 
                           count( * ) 
                      FROM tekma
                           JOIN
                           zadetek ON tekma.id = zadetek.tekma
                     where sezona = ?;'''
    curr.execute(poizvedba,[sezona])
    podatki = curr.fetchall()
    return podatki[0][0]
    

class Uporabnik:

    def __init__(self, uporabniskoIme=None, geslo=None, licenca=None):
        self.uporabniskoIme = uporabniskoIme
        self.geslo = geslo
        self.licenca = licenca

    def __str__(self):
        return self.uporabniskoIme

    def jeUporabnik(self,conn):
        sql = '''
        SELECT * FROM uporabnik
        WHERE uporabniskoIme= ?;'''
        poizvedba = conn.execute(sql,[self.uporabniskoIme])
        if poizvedba.fetchone():
            return poizvedba
        return None
    def jeUporabnik_login(self,conn):
        sql = '''
        SELECT * FROM uporabnik
        WHERE uporabniskoIme=? and geslo = ? ;'''
        poizvedba = conn.execute(sql,[self.uporabniskoIme,self.geslo])
        if poizvedba.fetchone():
            return poizvedba
        return None

    def jeUporabljenaLicenca(self,conn):
        sql = '''
        SELECT * FROM uporabnik
        WHERE licenca= ?;'''
        poizvedba = conn.execute(sql,[self.licenca])
        if poizvedba.fetchone():
            return poizvedba
        return None

    def vstaviUporabnika(self,conn):
        sql = '''
        INSERT INTO uporabnik (uporabniskoIme, geslo, licenca) VALUES (?,?,?);'''
        conn.execute(sql,[self.uporabniskoIme, self.geslo, self.licenca])
        conn.commit()

    @staticmethod
    def jePravaLicenca(licencna_st,conn):
        sql = '''
        SELECT id FROM licenca
        WHERE id= ?'''
        poizvedba = conn.execute(sql,[licencna_st]).fetchone()
        print(poizvedba)
        if poizvedba:
            return poizvedba[0]
        return None