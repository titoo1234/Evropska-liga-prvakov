import bottle
import sqlite3 as dbapi
import model
from dodajanje import *
from  iskanje_slike import *
conn = dbapi.connect('vaja_seminarska_v2.db')

@bottle.get('/')
def naslovna():
    vsi_klubi = model.Klub.najvec_zadetkov_klubi(conn, 500)
    klubi = vsi_klubi[:4]
    vsi_igralci = model.Igralec.najbolsi_strelci_vsa_leta(conn, 10000)
    igralci = vsi_igralci[:4]
    vsi = model.Klub.vsi_klubi(conn)
    return bottle.template('zacetna_stran.html', igralci=igralci, sezone = model.vse_sezone(conn),klubi = klubi,vsi=vsi,vsi_igralci = vsi_igralci,vsi_klubi = vsi_klubi)


@bottle.get('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='static')

@bottle.get('/klub/<ime>')
def klub(ime):
    url = poisci_url(ime +' logo')
    stadion = model.Klub.domaci_stadion(conn, ime)
    sezona_gol = model.Klub.koliko_golov(conn, ime)
    vsota = 0
    for sezona, goli in sezona_gol:
        vsota += goli
    return bottle.template('klub.html',ime=ime, url=url,stadion = stadion,goli=sezona_gol, vsota=vsota)

    

@bottle.get('/<ime>')
def igralec(ime):
    try:
        url = poisci_url(ime)
        ide = najdi_igralec_id(conn, ime)
        objekt = model.Igralec(ide, ime)
        return bottle.template('igralec.html', skupno=objekt.koliko_golov_skupno(conn),nasezono=objekt.koliko_golov(conn), ime=ime,url=url)
    except:
        return naslovna()
    
@bottle.get('/sezona/<sez1>' + '/<sez2>')
def sezona(sez1,sez2):
    
    tekme = model.Tekma.tekme_v_eni_sezoni(conn,sez1 + '/'+sez2)
    finale = tekme[-1]
    zmagovalec = finale.zmagovalec_finala()
    sezona = sez1+ '/'+sez2
    return bottle.template('sezona.html',sezona = sezona,tekme = tekme,zmagovalec = zmagovalec,url = poisci_url(zmagovalec + 'logo'))

@bottle.get('/to/se/more/ujemat')
def iskanje_igralca():
    prebrano = bottle.request.query.getunicode('ime')
    bottle.redirect("/" + prebrano)
#     return bottle.template("/Robert%20Lewandowski")

@bottle.get('/to/se/more/ujemat2')
def iskanje_kluba():
    prebrano = bottle.request.query.getunicode('ime')
    prebrano
    print(prebrano)
    bottle.redirect("/klub/" + prebrano)



bottle.run(debug=True)

