import bottle
import sqlite3 as dbapi
import model
from dodajanje import *
import iskanje_slike
conn = dbapi.connect('vaja_seminarska_v2.db')

@bottle.get('/')
def naslovna():
    return bottle.template('zacetna_stran.html', igralci=model.Igralec.najbolsi_strelci_vsa_leta(conn, 4), sezone = model.vse_sezone(conn))


@bottle.get('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='static')

@bottle.get('/<ime>')
def igralec(ime):
    try:
        url = iskanje_slike.poisci_url(ime)
        print(url)
        ide = najdi_igralec_id(conn, ime)
        objekt = model.Igralec(ide, ime)
        return bottle.template('igralec.html', skupno=objekt.koliko_golov_skupno(conn),nasezono=objekt.koliko_golov(conn), ime=ime,url=url)
    except:
        return naslovna()


bottle.run(debug=True)

