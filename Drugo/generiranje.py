import csv
import random

def generiraj_tekmo(ekipa1, ekipa2, tip):
    rez1 = random.randint(0,6)
    goli1 = []
    rez2 = random.randint(0,6)
    goli2 = []
    for gol in range(rez1):
        dal_gol = (random.choice(ekipa_igralci[ekipa1]), random.randint(0,90))
        goli1.append(dal_gol)
    for gol in range(rez2):
        dal_gol = (random.choice(ekipa_igralci[ekipa2]), random.randint(0,90))
        goli2.append(dal_gol)
    stadion = ekipa_stadion[ekipa1]
    return [ekipa1, ekipa2, rez1, rez2, goli1, goli2, stadion, tip]


def generiraj_tekme(tabela_ekip, tip):
    tekme = []
    for ekipa1 in tabela_ekip:
        for ekipa2 in tabela_ekip:
            if ekipa1 == ekipa2:
                continue
            tekma = generiraj_tekmo(ekipa1, ekipa2, tip)
            tekme.append(tekma)
    return tekme

def izberi_ekipe(n, skupina):
    ekipe_ki_grejo_naprej = set()
    while True:
        ekipe_ki_grejo_naprej.add(random.choice(skupina))
        if len(ekipe_ki_grejo_naprej) == n:
            ekipe_ki_grejo_naprej = list(ekipe_ki_grejo_naprej)
            return ekipe_ki_grejo_naprej
        
        
def zdruzi_po_dva(ekipe, tip):
    slovar_tekm[tip] = []
    i = 0
    while i < len(ekipe) - 1:
        if tip == "Finale":
            slovar_tekm[tip].append(generiraj_tekmo(ekipe[i], ekipe[i+1], tip))
        else:
            slovar_tekm[tip].append(generiraj_tekmo(ekipe[i], ekipe[i+1], tip))
            slovar_tekm[tip].append(generiraj_tekmo(ekipe[i+1], ekipe[i], tip))
        i += 1

if __name__ == '__main__':
    with open("ekipe.csv") as imena_ekip:
        reader = csv.reader(imena_ekip)
        ekipe = []
        for ekipa in reader:
            ekipe.append(ekipa[0])
            

    with open("igralci.csv") as imena:
        reader = csv.reader(imena)
        imena_igralcev = []
        for igralec in reader:
            imena_igralcev.append(igralec)
            
            
    with open("stadioni.csv") as imena_stadionov:
        reader = csv.reader(imena_stadionov)
        stadioni = []
        for stadion in reader:
            stadioni.append(stadion)

    slovar_ekip = {"A":ekipe[:4],"B":ekipe[4:8],"C":ekipe[8:12],"D":ekipe[12:16],"E":ekipe[16:20],"F":ekipe[20:24],"G":ekipe[24:28],"H":ekipe[28:32]}
    ekipa_stadion = {}        
    ekipa_igralci = {}
    slovar_tekm = {}

    k = 1
    for ekipa in ekipe:
        ekipa_igralci[ekipa] = imena_igralcev[(k-1)*20:k*20]
        ekipa_stadion[ekipa] = stadioni[k-1]
        k += 1          
                
    for skupina in slovar_ekip:
        slovar_tekm[skupina] = generiraj_tekme(slovar_ekip[skupina], skupina)
            
    ekipe_v_osmini = izberi_ekipe(16, ekipe)
    ekipe_v_cetrt = izberi_ekipe(8, ekipe_v_osmini)
    ekipe_v_pol = izberi_ekipe(4, ekipe_v_cetrt)
    ekipe_v_finalu = izberi_ekipe(2, ekipe_v_pol)

    zdruzi_po_dva(ekipe_v_osmini, "osmina")
    zdruzi_po_dva(ekipe_v_cetrt, "cetrt")
    zdruzi_po_dva(ekipe_v_pol, "polfinale")
    zdruzi_po_dva(ekipe_v_finalu, "Finale")

    print(slovar_tekm["Finale"])






        
        