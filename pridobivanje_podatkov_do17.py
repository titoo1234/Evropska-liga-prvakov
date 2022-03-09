
import requests
import re

def poberi_ekipe(link):
    """
    pobere vse ekipe z karticami in jih shrani v tabelo (zaenkrat)
    """
    req = requests.get(link).text
    #ekipe = re.findall(r'<th scope="col" width="28"><a href="/wiki/.+" title=".+">.+', req)
    ekipe = re.findall(r'<th scope="row" style="text-align: left; white-space:nowrap;font-weight: normal;background-color:.+;"><span class="flagicon"><a href=".+" title=".+"><img alt=".+" src=".+" decoding="async" width=".+" height=".+" class="thumbborder" srcset=".+" data-file-width=".+" data-file-height=".+" /></a></span> <a href="/wiki/.+" title=".+">.+</a>', req)
    ekipe_v_tabeli = []
    for el in ekipe:
        ekipa = el.split('"')
        ime = ekipa[-2]
        if ime == "Galatasaray S.K. (football team)":
            ime = "Galatasaray S.K. (football)" # pač na wikipediji so retardirani in so jih različno poimenovali
        if ime not in ekipe_v_tabeli:
            ekipe_v_tabeli.append(ime) # včasih je prislo do tiebreakov med ekpami in so napisane potem v še eni tabeli, zato da jih ne podvojima
    return ekipe_v_tabeli

def poberi_ekipe_vec_let(zac_leto):
    """
    z rezličnimi leti poklice funkcijo poberi_ekipe
    """
    if zac_leto > 2020 or zac_leto < 2000:
        return []
    slovar = dict()
    for leto in range(zac_leto, 2021):
        zacetni_link = "https://en.wikipedia.org/wiki/20ž%E2%80%93Ž_UEFA_Champions_League_group_stage" #črka ž namesto letnic
        prvi_del_sezone = str(leto)[-2:]
        drugi_del_sezone = str(leto + 1)[-2:]
        pravi_link = zacetni_link.replace("ž", prvi_del_sezone)
        pravi_link = pravi_link.replace("Ž", drugi_del_sezone)
        slovar[leto] = poberi_ekipe(pravi_link)
    return slovar

#a = poberi_ekipe_vec_let(2000) #dela od 2000 naprej, za prejšnja leta bo treba še malo modifikacije, lahk pa tut rečema da je dost


def test_tekme_group(link):
    req = requests.get(link).text
    tekme = re.findall(r'class="fleft"><time><div class="fdate".+</a></span></div><div>Attendance:', req, re.DOTALL)
    tabela_tekm1 = tekme[0].split('<div class="fdate">')
    tabela_tekm = tabela_tekm1[1:]
    urejena_tabela_tekm = []
    prejsni1 = []
    prejsni2 = []
    min1=[]
    min2=[]
    for tekma in tabela_tekm:
        # print(tekma)

        stadion = re.findall(r'itemprop="name address.+</a>,',tekma)
        
        datum = re.findall(r'.+<span',tekma)
        
        try:
            datum = datum[0].split(';')

            datum = datum[0].split('&')[0] +' '+ datum[1][:-5] +' '+ datum[2][:4]
        except:
            pass
        rez = re.findall(r'fscore".+</th><th',tekma)[0][8:11]
        try:
            domaci,domaci_uradno = tekma.split('itemprop="name"><a href="/wiki/')[1].split('</a>')[0].split('title="')[1].split('">')
            
            # domaci,domaci_uradno = re.findall(r'"homeTeam".+</a> <span',tekma)[0].split('title="')[1][:-10].split('">')
        except:
            domaci,domaci_uradno=[0,0]
        # ads = domaci
        # domaci = re.findall(r'"homeTeam".+</a> <span',tekma)[0].split('<')[-3].split('>')[-1]
        try:
            gosti,gosti_uradno = tekma.split('</span> <a href="/wiki/')[-1].split('</a>')[0].split('title="')[1].split('">')

            #gosti,gosti_uradno = re.findall(r'awayTeam.+</a></span></th></tr><tr class="fgoals">',tekma)[0].split('title="')[1]
        except:
            gosti,gosti_uradno = [0,0]
        stadion = stadion[0].split('title=')[1].split('"')[1]
        
        if '<td class="fhgoal"></td>' in tekma:
            goli_d = []
            min1 = []
        else:
            goli_d=tekma.split('<td class="fhgoal"><div class="plainlist">')[1].split('Report</a></td>')[0].split('<li><a href="/wiki')[1:]
            min1=[]
            min_1 = [re.findall(r'<span>[1234567890+]+<span ',el)for el in goli_d]
            for el in min_1:
                trenutna = []
                for minuta in el:
                    trenutna.append(minuta.replace('<span>','').replace('<span ',''))
                min1.append(trenutna)
            igralci_domaci = [el.split('title="')[1].split('"')[0] for el in goli_d]
            goli_d = igralci_domaci
                    
        
        if '<td class="fagoal"></td>' in tekma:
            goli_g = []
            min2 = []
        else:
            goli_g = tekma.split('<td class="fagoal"><div class="plainlist">')[1].split('</tr></tbody></table><div')[0].split('<li><a href="/wiki')[1:]
            min2 = []
            min_2 = [re.findall(r'<span>[1234567890+]+<span ',el)for el in goli_g]
            for el in min_2:
                trenutna = []
                for minuta in el:
                    trenutna.append(minuta.replace('<span>','').replace('<span ',''))
                min2.append(trenutna)
            igralci_domaci = [el.split('title="')[1].split('"')[0] for el in goli_g]
            goli_g = igralci_domaci
            
        urejena_tabela_tekm.append((min1,min2,goli_d,goli_g,datum,domaci,domaci_uradno,rez,gosti,gosti_uradno,stadion))
    
    return urejena_tabela_tekm
def test_tekme_knock(link):
    req = requests.get(link).text
    tekme = re.findall(r'class="fleft"><time><div class="fdate".+</a></span></div><div>Attendance:', req, re.DOTALL)
    tabela_tekm1 = tekme[0].split('<div class="fdate">')
    tabela_tekm = tabela_tekm1[1:]
    urejena_tabela_tekm = []
    prejsni1 = []
    prejsni2 = []
    min1=[]
    min2=[]
    gosti,gosti_uradno = (0,0)
    povratna = False
    # stari,stari_uradno = 0,0
    for tekma in tabela_tekm:
        # print(tekma)

        stadion = re.findall(r'itemprop="name address.+</a>,',tekma)
        
        datum = re.findall(r'.+<span',tekma)
        
        try:
            datum = datum[0].split(';')

            datum = datum[0].split('&')[0] +' '+ datum[1][:-5] +' '+ datum[2][:4]
            
        except:
            pass
        rez = re.findall(r'fscore".+</th><th',tekma)[0][8:11]
        try:
            domaci,domaci_uradno = tekma.split('itemprop="name"><a href="/wiki/')[1].split('</a>')[0].split('title="')[1].split('">')
            
            # domaci,domaci_uradno = re.findall(r'"homeTeam".+</a> <span',tekma)[0].split('title="')[1][:-10].split('">')
            povratna = False
        except:
            stari,stari_uradno = domaci,domaci_uradno
            domaci,domaci_uradno = gosti,gosti_uradno
            povratna = True
        # ads = domaci
        # domaci = re.findall(r'"homeTeam".+</a> <span',tekma)[0].split('<')[-3].split('>')[-1]
        if not povratna:
            try:
                gosti,gosti_uradno = tekma.split('</span> <a href="/wiki/')[-1].split('</a>')[0].split('title="')[1].split('">')
    
                #gosti,gosti_uradno = re.findall(r'awayTeam.+</a></span></th></tr><tr class="fgoals">',tekma)[0].split('title="')[1]
            except:
                gosti,gosti_uradno = [0,0]
        else:
            gosti,gosti_uradno = stari,stari_uradno
        stadion = stadion[0].split('title=')[1].split('"')[1]
        
        
        
        
        if '<td class="fhgoal"><div class="plainlist">' not in tekma:
            goli_d = []
            min1 = []
        else:
            goli_d=tekma.split('<td class="fhgoal"><div class="plainlist">')[1].split('Report</a></td>')[0].split('<li><a href="/wiki')[1:]
            min1=[]
            min_1 = [re.findall(r'<span>[1234567890+]+<span ',el)for el in goli_d]
            for el in min_1:
                trenutna = []
                for minuta in el:
                    trenutna.append(minuta.replace('<span>','').replace('<span ',''))
                min1.append(trenutna)
            igralci_domaci = [el.split('title="')[1].split('"')[0] for el in goli_d]
            goli_d = igralci_domaci
                    
        
        if '<td class="fagoal"><div class="plainlist">' not in tekma:
            goli_g = []
            min2 = []
        else:
            goli_g = tekma.split('<td class="fagoal"><div class="plainlist">')[1].split('</tr></tbody></table><div')[0].split('<li><a href="/wiki')[1:]
            min2 = []
            min_2 = [re.findall(r'<span>[1234567890+]+<span ',el)for el in goli_g]
            for el in min_2:
                trenutna = []
                for minuta in el:
                    trenutna.append(minuta.replace('<span>','').replace('<span ',''))
                min2.append(trenutna)
            igralci_domaci = [el.split('title="')[1].split('"')[0] for el in goli_g]
            goli_g = igralci_domaci
            
            
       
        urejena_tabela_tekm.append((min1,min2,goli_d,goli_g,datum,domaci,domaci_uradno,rez,gosti,gosti_uradno,stadion))
    
    return urejena_tabela_tekm

a = test_tekme_group("https://en.wikipedia.org/wiki/2015%E2%80%9316_UEFA_Champions_League_group_stage")
# b = test_tekme_knock('https://en.wikipedia.org/wiki/2018%E2%80%9319_UEFA_Champions_League_knockout_phase')
# c = test_tekme_knock('https://en.wikipedia.org/wiki/2011%E2%80%9312_UEFA_Champions_League_knockout_phase')



def poberi_leta(od):
    '''dela od leta 2016!!!'''
    del1 = "https://en.wikipedia.org/wiki/20"
    del2a = "_UEFA_Champions_League_group_stage"
    del2b = '_UEFA_Champions_League_knockout_phase'
    vmes = '%E2%80%93'
    slovar = dict()
    for leto in range(od,17):
        link1 = del1+str(leto)+vmes+str(leto+1)+del2a
        link2 = del1+str(leto)+vmes+str(leto+1)+del2b
        group = test_tekme_group(link1)
        knock = test_tekme_knock(link2)
        slovar[leto] = [group,knock]
    return slovar
# sl = poberi_leta(15)
        
    
        