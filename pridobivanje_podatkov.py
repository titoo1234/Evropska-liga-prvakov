import requests
import re
import json


def test_tekme_group(link):
    '''
    poberi podatke za skupinski del v neki sezoni
    '''
    req = requests.get(link).text
    tekme = re.findall(r'class="fleft"><time><div class="fdate".+</a></span></div><div>Attendance:', req, re.DOTALL)
    tabela_tekm1 = tekme[0].split('<div class="fdate">')

    tabela_tekm = tabela_tekm1[1:]
    tabela_tekm = [el.split('<table class="wikitable" style="text-align:center;">')[0] for el in tabela_tekm]
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
def test_tekme_knock(link):
    '''
    poberi podatke za izločilne boje v neki sezoni
    '''
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

# a = test_tekme_group("https://en.wikipedia.org/wiki/2019%E2%80%9320_UEFA_Champions_League_group_stage")
# b = test_tekme_knock('https://en.wikipedia.org/wiki/2018%E2%80%9319_UEFA_Champions_League_knockout_phase')
# c = test_tekme_knock('https://en.wikipedia.org/wiki/2011%E2%80%9312_UEFA_Champions_League_knockout_phase')



def poberi_leta(od):
    '''
    Pobere vse podatke iz spleta od leta 2017 naprej
    '''
    del1 = "https://en.wikipedia.org/wiki/20"
    del2a = "_UEFA_Champions_League_group_stage"
    del2b = '_UEFA_Champions_League_knockout_phase'
    vmes = '%E2%80%93'
    slovar = dict()
    for leto in range(od,22):
        link1 = del1+str(leto)+vmes+str(leto+1)+del2a
        link2 = del1+str(leto)+vmes+str(leto+1)+del2b
        group = test_tekme_group(link1)
        knock = test_tekme_knock(link2)
        slovar[leto] = [group,knock]
    return slovar
# sl = poberi_leta(17)

if __name__ == '__main__':
    sl = poberi_leta(17)
    with open('vsi_podatki.json', 'w') as dat:
        json.dump(sl, dat)
    



        
    
        