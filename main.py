#Implementació dels mots encreuats utilitzant backtracking

#Llegim fitxers
def llegeixFitxers(fitxer1, fitxer2):
    dicc = open(fitxer1)
    paraules = dicc.readlines()

    dicc = open(fitxer2)
    tauler = ''.join(dicc.readlines()).replace('\n',';')

    return paraules, tauler

def ordenaISeleccionaParaules(paraules):
    pars = {}
    for paraula in paraules:
        if len(paraula) > 2 and len(paraula) <= 5:
            p = paraula.strip() #Treu el \n.
            l = len(p)

            if l in pars.keys():
                pars[l].append(p)
            else:
                pars[l] = [p]

    pars = sorted(pars.items())
    return pars

def aplicaRestriccions(paraules, tauler):
    col = 
    

paraules, tauler = llegeixFitxers('diccionari_CB_v3.txt', 'crossword_CB_v3.txt')
words = ordenaParaules(paraules)
print(words)