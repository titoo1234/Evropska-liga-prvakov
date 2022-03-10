import bottle
import sqlite3 as dbapi
import model
from dodajanje import *
from  iskanje_slike import *
conn = dbapi.connect('vaja_seminarska_v2.db')

@bottle.get('/')
def naslovna():
    klubi = model.Klub.najvec_zadetkov_klubi(conn, 4)
    igralci = model.Igralec.najbolsi_strelci_vsa_leta(conn, 4)
    return bottle.template('zacetna_stran.html', igralci=igralci, sezone = model.vse_sezone(conn),klubi = klubi)


@bottle.get('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='static')

@bottle.get('/klub/<ime>')
def klub(ime):

    return bottle.template('klub.html',ime = ime)

    

@bottle.get('/<ime>')
def igralec(ime):
#     try:
    url = poisci_url(ime)
    ide = najdi_igralec_id(conn, ime)
    objekt = model.Igralec(ide, ime)
    return bottle.template('igralec.html', skupno=objekt.koliko_golov_skupno(conn),nasezono=objekt.koliko_golov(conn), ime=ime,url=url)
#     except:
#         
#         return naslovna()
    
@bottle.get('/sezona/<sez1>' + '/<sez2>')
def sezona(sez1,sez2):
    
    tekme = model.Tekma.tekme_v_eni_sezoni(conn,sez1 + '/'+sez2)
    finale = tekme[-1]
    zmagovalec = finale.zmagovalec_finala()
    sezona = sez1+ '/'+sez2
    return bottle.template('sezona.html',sezona = sezona,tekme = tekme,zmagovalec = zmagovalec,url = poisci_url(zmagovalec + 'logo'))


bottle.run(debug=True)

