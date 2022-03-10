import bottle
import sqlite3 as dbapi
import model

conn = dbapi.connect('vaja_seminarska_v2.db')

@bottle.get('/')
def naslovna():
    return bottle.template('zacetna_stran.html', podatki=model.Igralec.najbolsi_strelci_vsa_leta(conn, 10))


@bottle.get('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='static')


bottle.run(reloader=True, debug=True)

