from pridobivanje_podatkov import *
from dodajanje import *
conn = dbapi.connect('vaja_seminarska_v2.db')
slovar = poberi_leta(17)
skupine = "ABCDEFGH"
boji = ["OF"] * 16 + ["CF"] * 8 + ["PF"] * 4 + ["FINALE"]
boji19 = ["OF"] * 16 + ["CF"] * 4 + ["PF"] * 2 + ["FINALE"]
for leto in slovar:
    skupinski_del,izlocilni_boji = slovar[leto]
    stevec = 0
    for tekma in skupinski_del:
        dodaj_klub(conn, tekma[6]) #dodamo prvo ekipo, nisem dal uradna imena, ker niso konstantna
        dodaj_klub(conn, tekma[9]) #dodamo drugo ekipo
        dodaj_stadion(conn, tekma[10]) #dodamo stadion
        igralci1 = tekma[2]
        for igralec in igralci1:
            dodaj_igralca(conn, igralec)
            dodaj_ekipo(conn, leto, tekma[6], igralec)
            #dodamo ga v bazo
        igralci2 = tekma[3]
        for igralec in igralci2:
            dodaj_igralca(conn, igralec)
            dodaj_ekipo(conn, leto, tekma[9], igralec)
            #dodamo ga v bazo
        dodaj_tekmo(conn, leto, tekma[4], tekma[10], skupine[stevec // 12])
        dodaj_igra_klub(conn, leto, tekma[4], tekma[6], 'domaci', tekma[10])
        dodaj_igra_klub(conn, leto, tekma[4], tekma[9], 'gostje', tekma[10])
        stevec += 1
        
        for i in range(len(tekma[0])):
            igralec = igralci1[i]
            goli = tekma[0][i]
            for minuta in goli:
                dodaj_zadetek(conn, tekma[6], igralec, minuta, leto, tekma[4], tekma[10])
        for i in range(len(tekma[1])):
            igralec = igralci2[i]
            goli = tekma[1][i]
            for minuta in goli:
                
                dodaj_zadetek(conn, tekma[9], igralec, minuta, leto, tekma[4], tekma[10])
    stevec = 0
    for tekma in izlocilni_boji:
        if leto != 19:
            dodaj_stadion(conn, tekma[10])
            igralci1 = tekma[2]
            for igralec in igralci1:
                dodaj_igralca(conn, igralec)
            igralci2 = tekma[3]
            for igralec in igralci2:
                dodaj_igralca(conn, igralec)
            dodaj_tekmo(conn, leto, tekma[4], tekma[10], boji[stevec])
            dodaj_igra_klub(conn, leto, tekma[4], tekma[6], 'domaci', tekma[10])
            dodaj_igra_klub(conn, leto, tekma[4], tekma[9], 'gostje', tekma[10])
            stevec += 1
            for i in range(len(tekma[0])):
                igralec = igralci1[i]
                goli = tekma[0][i]
                for minuta in goli:
                    dodaj_zadetek(conn, tekma[6], igralec, minuta, leto, tekma[4], tekma[10])
            for i in range(len(tekma[1])):
                igralec = igralci2[i]
                goli = tekma[1][i]
                for minuta in goli:
                
                    dodaj_zadetek(conn, tekma[9], igralec, minuta, leto, tekma[4], tekma[10])
        else:
            dodaj_stadion(conn, tekma[10])
            igralci1 = tekma[2]
            for igralec in igralci1:
                dodaj_igralca(conn, igralec)
            igralci2 = tekma[3]
            for igralec in igralci2:
                dodaj_igralca(conn, igralec)
            dodaj_tekmo(conn, leto, tekma[4], tekma[10], boji19[stevec])
            dodaj_igra_klub(conn, leto, tekma[4], tekma[6], 'domaci', tekma[10])
            dodaj_igra_klub(conn, leto, tekma[4], tekma[9], 'gostje', tekma[10])
            stevec += 1
            for i in range(len(tekma[0])):
                igralec = igralci1[i]
                goli = tekma[0][i]
                for minuta in goli:
                    dodaj_zadetek(conn, tekma[6], igralec, minuta, leto, tekma[4], tekma[10])
            for i in range(len(tekma[1])):
                igralec = igralci2[i]
                goli = tekma[1][i]
                for minuta in goli:
                    
                    dodaj_zadetek(conn, tekma[9], igralec, minuta, leto, tekma[4], tekma[10])
            
            
            
        
        


conn.commit()
conn.close()

