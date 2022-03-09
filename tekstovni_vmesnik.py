from model import *
import sqlite3 as dbapi
conn = dbapi.connect('vaja_seminarska_v2.db')


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
tekme = Tekma.tekme_v_eni_sezoni(conn, '2017/18')
for tekma in tekme:
    print(tekma)

conn.close()






