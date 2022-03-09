from model import *
import sqlite3 as dbapi
conn = dbapi.connect('vaja_seminarska_v2.db')


#TO DELA
# tab= vse_ekipe_sezona(conn,"2017/18")
# tab = vse_ekipe(conn) 
# tab = najbolsi_strelci_vsa_leta(conn)
# igralec = goli_igralec(conn,'Haris Seferovic')



#DELA, TREBA BIT V PYTHONU BOL NATANČEN KER STOLPEC ŽELIŠ
# tekme = tekme_v_eni_sezoni(conn, '2017/18')
# print(len(tekme))

conn.close()






