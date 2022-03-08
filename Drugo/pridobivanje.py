# -*- coding: utf-8 -*-
import requests
import re
import json


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


def test_tekme(link):
    req = requests.get(link).text
    tekme = re.findall(r'class="fleft"><time><div class="fdate".+</a></span></div><div>Attendance:', req, re.DOTALL)
    tabela_tekm = tekme[0].split('<div class="fleft"><time>')
    tabela_tekm = tabela_tekm[1:]
    urejena_tabela_tekm = []
    prejsni1 = []
    prejsni2 = []
    slovar = dict()   
    for tekma in tabela_tekm:
        stadion = re.findall(r'itemprop="name address.+</a>,',tekma)
        
        datum = re.findall(r'fdate">.+<span',tekma)
        
        try:
            datum = datum[0].split(';')
            datum = datum[0].split('&')[0].split('>')[1] +' '+ datum[1][:-5] +' '+ datum[2][:4]
        except:
            pass
        rez = re.findall(r'fscore".+</th><th',tekma)[0][8:11]
        domaci,domaci_uradno = re.findall(r'"homeTeam".+</a> <span',tekma)[0].split('title="')[1][:-10].split('">')
        # ads = domaci
        # domaci = re.findall(r'"homeTeam".+</a> <span',tekma)[0].split('<')[-3].split('>')[-1]
        gosti,gosti_uradno = re.findall(r'awayTeam.+</a></span></th></tr><tr class="fgoals">',tekma)[0].split('</a></span></th></tr><tr class="fgoals"')[0].split('title="')[-1].split('">')
        stadion = stadion[0].split('title=')[1].split('"')[1]
        if '<td class="fhgoal"></td>' in tekma:
            goli_d = []
        else:  
            goli = re.findall(r'<td class="fhgoal".+<td class="fagoal"',tekma,re.DOTALL)[0].split('title=')
            goli_d = [el.split('"')[1]for el in goli if '</a> <link' in el]
            minute = [el.split('&#')[1:-1] for el in goli if '/>&#32;<span>' in el]
            min1 = []
            
            for minuta in minute:
                zacasno= []
                for el in minuta:
                    p = el.split('<span ')[0]
                    try:
                        zacasno.append(p.split('<span>')[1])
                    except:
                        pass
                min1.append(zacasno)
            #[el.split('/>&#32;<span>')[1].split('<span')[0] for el in goli if '/>&#32;<span>' in el]
        if '<td class="fagoal"></td>' in tekma:
            goli_g = []
            min2=[]
        else:
             goli = re.findall(r'<td class="fagoal".+</span></li></ul></div></td>',tekma,re.DOTALL)[0].split('title=')
             goli_g = [el.split('"')[1]for el in goli if '</a> <link' in el]
             minute = [el.split('&#')[1:-1] for el in goli if '/>&#32;<span>' in el]
             min2 = []
             
             for minuta in minute:
                zacasno= []
                for el in minuta:
                    p = el.split('<span ')[0]
                    try:
                        zacasno.append(p.split('<span>')[1])
                    except:
                        pass
                min2.append(zacasno)
        # <td class="fhgoal"
        # <td class="fagoal"
        if min1 == prejsni1:
            min1 = []
        else:
            prejsni1 = min1
        if min2 == prejsni2:
            min2 = []
        else:
            prejsni2 = min2
        slovar['domaci'] = domaci
        slovar['domaci_uradno'] = domaci_uradno
        slovar['gosti'] = gosti
        slovar['gosti_uradnno'] = gosti_uradno
        slovar['rezultat'] = rez
        slovar['stadion'] = stadion
        slovar['datum'] = datum
        # urejena_tabela_tekm.append((min1,min2,goli_d,goli_g,datum,domaci,domaci_uradno,rez,gosti,gosti_uradno,stadion))
        urejena_tabela_tekm.append(slovar.copy())
    return urejena_tabela_tekm
    


def pisi_na_datoteko(tabela):
    with open('data.json', 'w') as jsonfile:
        json.dump(tabela, jsonfile)
if __name__ == '__main__':
    a = test_tekme("https://en.wikipedia.org/wiki/2019%E2%80%9320_UEFA_Champions_League_group_stage")
    # b = test_tekme('https://en.wikipedia.org/wiki/2019%E2%80%9320_UEFA_Champions_League_knockout_phase')
#     pisi_na_datoteko(a)
        