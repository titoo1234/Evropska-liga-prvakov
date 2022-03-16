import sqlite3 as dbapi
import model
from dodajanje import *
import sqlite3 as dbapi
import difflib
conn = dbapi.connect('finalna.db')


#TO DELA
#tab= Klub.vsi_klubi_sezona(conn,"2017/18")

#tab = Klub.vsi_klubi(conn) 
#tab = Igralec.najbolsi_strelci_vsa_leta(conn, 10)
# test = Igralec(22,'Lionel Messi')
# tab = test.koliko_golov(conn)
# 
# for el in tab:
#     print(el)
#     
# print(len(tab))

#DELA, TREBA BIT V PYTHONU BOL NATANČEN KER STOLPEC ŽELIŠ
# tekme = Tekma.tekme_v_eni_sezoni(conn, '2017/18')
# for tekma in tekme:
#     print(tekma)

while True:
    print("")
    print("Na voljo so različni podatki, izberi med naslednjimi tako, da vpišeš željeno številko.")
    print("1.) Določena sezona")
    print("2.) Določen igralec")
    print("3.) Določen klub")
    print("4.) Splošni podatki")
    print("5.) Končaj")



    while True:
        try:
            stevka = int(input())
            break
        except:
            print('Napačen vnos. Vnesti morate število med 1 in 5.')
    if stevka == 1:
        sezone = [el for (el,) in model.vse_sezone(conn)]
        print('Na voljo so naslednje sezone:')
        stevec = 1
        for sezona in sezone:
            print("{:>20s} | {:s}".format(str(stevec) +") sezona",sezona))
            stevec +=1
            
        while True:
            try:
                vnos = int(input("Vnesi zaporedno številko željene sezone: "))
                if vnos not in range(1,len(sezone)+1):
                    print("Neveljaven vnos, poskusite znova!")
                    #izpiše katera leta?
                else:
                    break
            except:
                print("Neveljaven vnos, poskusite znova!")
        tekme = model.Tekma.tekme_v_eni_sezoni(conn,sezone[vnos-1])
        najdel = False
        for tekma in tekme[::-1]:
            if tekma.tip == "FINALE":
                zmagovalec = tekma.zmagovalec_finala()
                najdel = True
                break

        if not najdel:
            zmagovalec = 'V tej sezoni še ni bilo odigranega finala.'
        for te in tekme:
            print(te)
        
        print('Zmagovalec: ' + zmagovalec)
        print('Število odigranih tekem: ' + str(len(tekme)))
        st_golov = model.koliko_golov_sezona(conn,sezone[vnos-1])
        print('Skupno število golov: ' + str(st_golov))

 
    elif stevka == 2:
        print()
        igralci = model.Igralec.vsi_igralci(conn)
        igralci1 = [el for (el,) in igralci]
        print("Vnesi ime igralca oblike Ime Priimek!")
        while True:
            igralec_vhod = input("Igralec: ")
            print()
            if (igralec_vhod,) in igralci:
                print(igralec_vhod)
                objekt = model.Igralec(najdi_igralec_id(conn, igralec_vhod),igralec_vhod)
                goli = objekt.koliko_golov_sezona_klub(conn)
                print("{:>20s} | {:s} | {:s}".format("Sezona","Goli","Ekipa"))
                for a,b,c in goli:
                    print("{:>20s} | {:4s} | {:s}".format(str(a), str(b), str(c)))
                print()
                print("{:>20s} | {:4s}".format("Skupno", str(objekt.koliko_golov_skupno(conn)[0][0])))

                print()
                break
            elif len(difflib.get_close_matches(igralec_vhod, igralci1)) > 0:
                print("Ste morda mislili katerega od naslednjiih nogometašev?")
                print(", ".join(difflib.get_close_matches(igralec_vhod, igralci1)))
                
            else:
                print("Napačen vnos, poskusite znova!")
            
            
            
    elif stevka == 3:
        print()
        klubi = model.Klub.vsi_klubi(conn)
        vsi_klubi = [klub.ime for klub in klubi]
        while True:
            print("Vnesi ime kluba!")
            klub_vhod = input("Klub: ")
            
            print()
      
            if klub_vhod in vsi_klubi:
                stevilo_golov = model.Klub.koliko_golov(conn, klub_vhod)
                skupno = 0
                print(klub_vhod)
                print("Domači stadion: " + model.Klub.domaci_stadion(conn, klub_vhod)[0][0])
                for a,b in stevilo_golov:
                    print(a, b)
                    skupno += b
                print("Skupno: " + str(skupno))
                
                print()
                break

            elif len(difflib.get_close_matches(klub_vhod, vsi_klubi)) > 0:
                print("Ste morda mislili katerega od naslednjiih klubov?")
                print(", ".join(difflib.get_close_matches(klub_vhod, vsi_klubi)))
                
            else:
                print("Klub ne obstaja! Poskusite znova!")
            
    elif stevka == 4:
        print()
        najbolsi_strelci = model.Igralec.najbolsi_strelci_vsa_leta(conn, 5)
        najbolsi_klubi = model.Klub.najvec_zadetkov_klubi(conn, 5)
        print("Najboljši igralci in klubi!")
        print("{:>20s}   {:s}  {:>20s}   {:s}".format("Ime igralca","Število golov", "Ime kluba", "Število golov"))
        for a,b in zip(najbolsi_strelci,najbolsi_klubi):
            print("{:>20s} | {:s}  {:>31s} | {:s}".format(a[0],str(a[1]), b[0], str(b[1])))
                
            
    
        
        
        
    elif stevka == 5:
        print("")
        print("Hvala!")
        break
    else:
        print('Vnesiti morate število med 1 in 5!')





conn.close()







