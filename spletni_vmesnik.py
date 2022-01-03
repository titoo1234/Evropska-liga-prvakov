import bottle

@bottle.get('/')
def naslovna():
    return bottle.template("zacetna_stran.html")


@bottle.get('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='static')


bottle.run(reloader=True, debug=True)

