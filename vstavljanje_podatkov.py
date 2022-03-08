from pridobivanje_podatkov import *
from dodajanje import *
conn = dbapi.connect('vaja_seminarska.db')
slovar = poberi_leta(19)
for leto in slovar:
    skupinski_del,izlocilni_boji = slovar[leto]
    for tekma in skupinski_del:
        igralci1 = tekma[2]
        for igralec in igralci1:
            dodaj_igralca(conn, igralec)
            #dodamo ga v bazo
        igralci2 = tekma[3]
        for igralec in igralci2:
            dodaj_igralca(conn, igralec)
            #dodamo ga v bazo
        dodaj_klub(conn, tekma[6]) #dodamo prvo ekipo, nisem dal uradna imena, ker niso konstantna
        dodaj_klub(conn, tekma[9]) #dodamo drugo ekipo
        dodaj_stadion(conn, tekma[10]) #dodamo stadion


conn.commit()
conn.close()

