import bottle
import sqlite3 as dbapi
import hashlib
import model
from dodajanje import *
from  iskanje_slike import *
conn = dbapi.connect('vaja_seminarska11.db')
month = {	'01':'Janauary',
		'02':'February',
		'03':'March',
		'04':'April',
		'05':'May',
		'06':'June',
		'07':'July',
		'08':'August',
		'09':'September',
		'10':'October',
		'11':'November',
		'12':'December'		}
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
    sezone = model.vse_sezone(conn)
    klubi = vsi_klubi[:len(sezone)]
    vsi_igralci = model.Igralec.najbolsi_strelci_vsa_leta(conn, 10000)
    igralci = vsi_igralci[:len(sezone)]
    vsi = model.Klub.vsi_klubi(conn)
    return bottle.template('zacetna_stran.html', igralci=igralci, sezone = sezone,klubi = klubi,vsi=vsi,vsi_igralci = vsi_igralci,vsi_klubi = vsi_klubi,user=get_user())


@bottle.get('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='static')

@bottle.get('/klub/<ime>')
def klub(ime):
    try:
        url = poisci_url(ime +' logo')
        stadion = model.Klub.domaci_stadion(conn, ime)
        url_stadion = poisci_url(stadion)
        sezona_gol = model.Klub.koliko_golov(conn, ime)
        vsota = 0
        for sezona, goli in sezona_gol:
            vsota += goli
        return bottle.template('klub.html',user=get_user(),ime=ime, url=url,stadion = stadion,goli=sezona_gol, vsota=vsota,url_stadion = url_stadion)
    except:
        bottle.redirect("/")
    

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
    sezona = sez1+ '/'+sez2
    tekme = model.Tekma.tekme_v_eni_sezoni(conn,sezona)
    koliko_golov = model.koliko_golov_sezona(conn,sezona)
    najdel = False
    for tekma in tekme[::-1]:
        if tekma.tip == "FINALE":
            zmagovalec = tekma.zmagovalec_finala()
            najdel = True
            break
    
    if not najdel:
        zmagovalec = 'V tej sezoni še ni bilo odigranega finala'
    return bottle.template('sezona.html',koliko_golov = koliko_golov, user=get_user(),sezona = sezona,najdel = najdel,tekme = tekme,zmagovalec = zmagovalec,url = poisci_url(zmagovalec + 'logo'))

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
def uredi(Napaka1 = None):
    vsi_klubi = model.Klub.najvec_zadetkov_klubi(conn, 500)
    vsi_igralci = model.Igralec.najbolsi_strelci_vsa_leta(conn, 10000)
    vsi_stadioni = model.Stadion.vsi_stadioni(conn)
    return bottle.template('uredi.html',vsi_stadioni = vsi_stadioni,vsi_klubi = vsi_klubi,vsi_igralci=vsi_igralci,user=get_user(),Napaka1=Napaka1)

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

@bottle.get('/uredi/to/se/more/ujemat3')
def dodajanje_tekme():
    #TODO treba napisat v redu datum
    datum = bottle.request.query.getunicode("trip-start")
    #2018-07-22
    
    sezona = int(datum[2:4])
    if int(datum[5:7]) < 9:
        sezona -= 1
    if model.je_finale(conn,sezona):
        vsi_klubi = model.Klub.najvec_zadetkov_klubi(conn, 500)
        vsi_igralci = model.Igralec.najbolsi_strelci_vsa_leta(conn, 10000)
        vsi_stadioni = model.Stadion.vsi_stadioni(conn)
        return bottle.template('uredi.html',vsi_stadioni = vsi_stadioni,vsi_klubi = vsi_klubi,vsi_igralci=vsi_igralci,user=get_user(),Napaka1='To sezono je že bilo odigrano finale')
        
    
    datum = str(int(datum[-2:]))+ ' ' + month[datum[5:7]] +' '+ datum[:4]
    klub1 = bottle.request.query.getunicode("klub1")
    klub2 = bottle.request.query.getunicode("klub2")
    goli1 = int(bottle.request.query.getunicode("goli1"))
    goli2 = int(bottle.request.query.getunicode("goli2"))
    tip = bottle.request.query.getunicode("tipi")
    stadion = bottle.request.query.getunicode("stadion")
    dodaj_klub(conn,klub1)#samo če ga ni ga vstavi
    dodaj_klub(conn,klub2)
    dodaj_stadion(conn,stadion)
    
#     klub_id1 = najdi_klub_id(conn,klub1)
#     klub_id2 = najdi_klub_id(conn,klub2)
#     stadion_id = najdi_stadion_id(conn,stadion)
    rezultat = str(goli1)+'-'+str(goli2)
    dodaj_tekmo(conn,sezona,datum,rezultat,stadion,tip)
    dodaj_igra_klub(conn, sezona, datum, klub1, 'domaci', stadion)
    dodaj_igra_klub(conn, sezona, datum, klub2, 'gostje', stadion)
    for i in range(goli1):
        igralec = bottle.request.query.getunicode("igralec1" + str(i))
        minuta = bottle.request.query.getunicode("minuta1" + str(i))
        if igralec == "" or minuta == "":
            vsi_klubi = model.Klub.najvec_zadetkov_klubi(conn, 500)
            vsi_igralci = model.Igralec.najbolsi_strelci_vsa_leta(conn, 10000)
            vsi_stadioni = model.Stadion.vsi_stadioni(conn)
            return bottle.template('uredi.html',vsi_stadioni = vsi_stadioni,vsi_klubi = vsi_klubi,vsi_igralci=vsi_igralci,user=get_user(),Napaka1='Nisi označil pravilno')
        dodaj_igralca1(conn,igralec)
        dodaj_ekipo(conn, sezona, klub1, igralec)     
        dodaj_zadetek(conn, klub1, igralec, minuta, sezona, datum, stadion)
        
        
    for i in range(goli2):
        igralec = bottle.request.query.getunicode("igralec2" + str(i))
        minuta = bottle.request.query.getunicode("minuta2" + str(i))
        if igralec == "" or minuta == "":
            vsi_klubi = model.Klub.najvec_zadetkov_klubi(conn, 500)
            vsi_igralci = model.Igralec.najbolsi_strelci_vsa_leta(conn, 10000)
            vsi_stadioni = model.Stadion.vsi_stadioni(conn)
            return bottle.template('uredi.html',vsi_stadioni = vsi_stadioni,vsi_klubi = vsi_klubi,vsi_igralci=vsi_igralci,user=get_user(),Napaka1='Nisi označil pravilno')     
        dodaj_igralca1(conn,igralec)
        dodaj_ekipo(conn, sezona, klub2, igralec)
        dodaj_zadetek(conn, klub2, igralec, minuta, sezona, datum, stadion)
    

    conn.commit()
#     print(datum)
    bottle.redirect("/uredi")

bottle.run(debug=True)

