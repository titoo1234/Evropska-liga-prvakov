import bottle
import sqlite3 as dbapi
import hashlib
import model
from dodajanje import *
from  iskanje_slike import *
conn = dbapi.connect('vaja_seminarska.db')
def password_md5(s):
    """Vrni MD5 hash danega UTF-8 niza. Gesla vedno spravimo v bazo
       kodirana s to funkcijo."""
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

secret = "to skrivnost je zelo tezko uganiti 1094107c907cw982982c42"

def get_user():
    """Poglej cookie in ugotovi, kdo je prijavljeni uporabnik,
       vrni njegov username in ime. Če ni prijavljen, presumeri
       na stran za prijavo ali vrni None (advisno od auto_login).
    """
    # Dobimo username iz piškotka
    uporabniskoIme = bottle.request.get_cookie('uporabniskoIme', secret=secret)
    # Preverimo, ali ta uporabnik obstaja
    if uporabniskoIme is not None:
        r = model.Uporabnik(uporabniskoIme).jeUporabnik(conn)
        if r is not None:
            # uporabnik obstaja, vrnemo njegove podatke
            return uporabniskoIme
    # Če pridemo do sem, uporabnik ni prijavljen, naredimo redirect
    else:
        return None

# Pomozne funkcije
#-----------------------------------------------------------------------------------------------------------------------

# @bottle.get('/static/<filename:path>')
# def static(filename):
#     return static_file(filename, root='static')



@bottle.get('/login')
def login():
    return bottle.template('login.html', napaka=None)

@bottle.post('/login')
def login_post():
    '''Obdelaj izpolnjeno formo za prijavo'''
    # Uporabniško ime, ki ga je uporabnik vpisal v formo
    uporabniskoIme = bottle.request.forms.uporabniskoIme
    # Izračunamo MD5 has gesla, ki ga bomo spravili
    geslo = password_md5(bottle.request.forms.geslo)
    # Preverimo, ali se je uporabnik pravilno prijavil
    poizvedba = model.Uporabnik(uporabniskoIme, geslo).jeUporabnik_login(conn)
    if poizvedba is None:
        # Uporabnisko ime in geslo se ne ujemata
        return bottle.template('login.html', napaka='Uporabnik ne obstaja.')
    else:
        # Vse je vredu, nastavimo
        bottle.response.set_cookie('uporabniskoIme', uporabniskoIme, path='/', secret=secret)
        bottle.redirect('/')

@bottle.get('/logout')
def logout():
    '''Pobrisi cookie in preusmeri na login.'''
    bottle.response.delete_cookie('uporabniskoIme')
    bottle.redirect('/')

@bottle.get('/register')
def register():
    return bottle.template('register.html', uporabniskoIme=None, napaka=None)

@bottle.post('/register')
def register_post():
    print('trying to register')
    '''Registriraj novega uporabnika.'''
    uporabniskoIme = bottle.request.forms.uporabniskoIme
    licencna_st = bottle.request.forms.licenca
    geslo1 = bottle.request.forms.geslo1
    geslo2 = bottle.request.forms.geslo2
    licenca = model.Uporabnik().jePravaLicenca(licencna_st,conn)
    poizvedba1 = model.Uporabnik(uporabniskoIme=uporabniskoIme).jeUporabnik(conn)
    poizvedba2 = model.Uporabnik(licenca=licencna_st).jeUporabljenaLicenca(conn)
    if poizvedba1:
        print('Uporabnisko ime ze obstaja')
        # Uporabnisko ime ze obstaja
        return bottle.template('register.html', uporabniskoIme=uporabniskoIme, napaka='To uporabnisko ime ze obstaja.')
    elif poizvedba2:
        print('Licenca je ze uporabljena.')
        # Licenca je ze uporabljena
        return bottle.template('register.html', uporabniskoIme=uporabniskoIme, napaka='Ta licenca je ze uporabljena.')
    elif licenca:
        if not geslo1 == geslo2:
            print('gesli se ne ujemata')
            # Gesli se ne ujemata
            return bottle.template('register.html', uporabniskoIme=uporabniskoIme, napaka='Gesli se ne ujemata.')
        else:
            # Vse je vredu, vstavi novega uporabnika v bazo
            print('ustvarjamo novega uporabnika')

            geslo = password_md5(geslo1)
            model.Uporabnik(uporabniskoIme, geslo, licenca).vstaviUporabnika(conn)

            # Dodaj uporabniku cookie
            bottle.response.set_cookie('uporabniskoIme', uporabniskoIme, path='/', secret=secret)
            bottle.redirect('/')
    else:
        return bottle.template('register.html', uporabniskoIme=uporabniskoIme, napaka='Ta licenca ne obstaja.')



@bottle.get('/')
def naslovna():
    vsi_klubi = model.Klub.najvec_zadetkov_klubi(conn, 500)
    klubi = vsi_klubi[:4]
    vsi_igralci = model.Igralec.najbolsi_strelci_vsa_leta(conn, 10000)
    igralci = vsi_igralci[:4]
    vsi = model.Klub.vsi_klubi(conn)
    return bottle.template('zacetna_stran.html', igralci=igralci, sezone = model.vse_sezone(conn),klubi = klubi,vsi=vsi,vsi_igralci = vsi_igralci,vsi_klubi = vsi_klubi,user=get_user())


@bottle.get('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='static')

@bottle.get('/klub/<ime>')
def klub(ime):
    url = poisci_url(ime +' logo')
    stadion = model.Klub.domaci_stadion(conn, ime)
    url_stadion = poisci_url(stadion)
    sezona_gol = model.Klub.koliko_golov(conn, ime)
    vsota = 0
    for sezona, goli in sezona_gol:
        vsota += goli
    return bottle.template('klub.html',user=get_user(),ime=ime, url=url,stadion = stadion,goli=sezona_gol, vsota=vsota,url_stadion = url_stadion)

    

@bottle.get('/<ime>')
def igralec(ime):
    try:
        url = poisci_url(ime)
        ide = najdi_igralec_id(conn, ime)
        objekt = model.Igralec(ide, ime)
        return bottle.template('igralec.html',user=get_user(), skupno=objekt.koliko_golov_skupno(conn),nasezono=objekt.koliko_golov(conn), ime=ime,url=url)
    except:
        return naslovna()
    
@bottle.get('/sezona/<sez1>' + '/<sez2>')
def sezona(sez1,sez2):
    
    tekme = model.Tekma.tekme_v_eni_sezoni(conn,sez1 + '/'+sez2)
    finale = tekme[-1]
    zmagovalec = finale.zmagovalec_finala()
    sezona = sez1+ '/'+sez2
    return bottle.template('sezona.html',user=get_user(),sezona = sezona,tekme = tekme,zmagovalec = zmagovalec,url = poisci_url(zmagovalec + 'logo'))

@bottle.get('/to/se/more/ujemat')
def iskanje_igralca():
    prebrano = bottle.request.query.getunicode('ime')
    bottle.redirect("/" + prebrano)
#     return bottle.template("/Robert%20Lewandowski")

@bottle.get('/to/se/more/ujemat2')
def iskanje_kluba():
    prebrano = bottle.request.query.getunicode('ime2')
    bottle.redirect("/klub/" + prebrano)

@bottle.get('/uredi')
def uredi(Napaka1 = None,Napaka2 = None):
    return bottle.template('uredi.html',user=get_user(),Napaka1=Napaka1,Napaka2 = Napaka2)

@bottle.post('/uredi')
def dodaj_igralca():
    '''Obdelaj izpolnjeno formo za prijavo'''
    # Dodamo igralca
    ime = bottle.request.forms.Vstavi_igralca
    klub = bottle.request.forms.Vstavi_klub
    #Pogledamo, če je že v bazi
    if ime:
        try:
            model.Igralec.dodaj_igralca(conn, ime)
            return bottle.template('uredi.html',user=get_user(),Napaka1 = 'Uspelo',Napaka2 = None)

        
    #         bottle.redirect('/uredi',user=get_user(), napaka1='Uspešno dodan igralec',Napaka2 = None)
        except:
            return bottle.template('uredi.html',user=get_user(),Napaka1 = 'Ta igralec že obstaja',Napaka2 = None)
    if klub:
        try:
            model.Klub.dodaj_klub(conn, klub)
            return bottle.template('uredi.html',user=get_user(),Napaka1 = None,Napaka2 = 'Uspelo')

        except:
            return bottle.template('uredi.html',user=get_user(),Napaka1 = None,Napaka2 = 'Ta klub že obstaja')



bottle.run(debug=True)

