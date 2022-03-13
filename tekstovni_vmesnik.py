import sqlite3 as dbapi
import model
from dodajanje import *
import sqlite3 as dbapi
conn = dbapi.connect('vaja_seminarska1.db')


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
                vnos = int(input("Vnesi število željenege sezone: "))
                if vnos not in range(1,len(sezone)+1):
                    print("Neveljavno vnos, poskusite znova!")
                    #izpiše katera leta?
                else:
                    break
            except:
                print("Neveljaven vnos, poskusite znova!")
        tekme = model.Tekma.tekme_v_eni_sezoni(conn,sezona[vnos])
        print(tekme)
        
        
        
    elif stevka == 5:
        print("")
        print("Hvala!")
        break
    else:
        print('Vnesiti morate število med 1 in 5!')





conn.close()








