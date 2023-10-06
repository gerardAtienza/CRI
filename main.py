import numpy as np
#Implementació dels mots encreuats utilitzant backtracking


class slot:
    def __init__(self, posIn = (-1,-1), long = -1, orientacio = -1, cross = [((-1, -1), -1)], id = -1):
        self.posIn = posIn #Posicio Inicial
        self.long = long #Longitud del slot
        self.orientacio = orientacio #0 = Horitzontal, 1 = Vertical
        self.cross = cross #Llista d'encreuaments ((x, y), id)
        self.id = id #Identificador del slot
        



#Llegim fitxers
def llegeixFitxers(fitxer1, fitxer2):
    dicc = open(fitxer1)
    paraules = dicc.readlines()

    dicc = open(fitxer2)
    lineas = dicc.readlines()
    tauler = []
    fila = []
    for linea in lineas:
        vals = linea.strip().split()
        fila = [val for val in vals]
        tauler.append(fila)
    tauler = np.array(tauler)

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

def dividirTauler(tauler):
    slots = []
    id = 1
    comprova = np.zeros(tauler.shape) #Matriu per comprovar els crossings

    #Horitzontals
    for i, fila in enumerate(tauler): #Coordenada y
        c = 0
        for j, el in enumerate(fila): #Coordenada x
            if el == '0':
                c+=1
                if (c == 6 or j == 5):
                    if c > 1:
                        tupla=(i, (j-c)+1)
                        slots.append(slot(tupla , c , 0, None, id))
                        for k in range((j-c)+1, j+1):
                            comprova[i][k] = id
                        id+=1
                        c=0
            else:
                if c > 1:
                    tupla = (i, (j-c))
                    a = slot(tupla, c, 0, None, id)
                    for k in range(j-c, j):
                        comprova[i][k] = id
                    id+=1
                    slots.append(a)
                c=0
    
    #Verticals
    for z, col in enumerate(tauler.T):
        c1 = 0
        crosses = []
        for y, ele in enumerate(col):
            if ele == '0':
                c1+=1
                if(comprova[y][z] != 0):
                    crosses.append(((y, z), comprova[y][z]))
                if (c1 == 6 or y == 6):
                    if c1 > 1:
                        tupla=(z, (y-c1)+1)
                        slots.append(slot(tupla , c1 , 1, crosses, id))
                        id+=1
                        c1=0
            else:
                if c1 > 1:
                    a1 = slot((y-c1,z), c1, 1, crosses, id)
                    id+=1
                    slots.append(a1)
                c1=0

    return slots, comprova

paraules, tauler = llegeixFitxers('diccionari_CB_v3.txt', 'crossword_CB_v3.txt')
words = ordenaISeleccionaParaules(paraules)
slots, comprova = dividirTauler(tauler)
print(comprova)

for slot in slots:
    print(slot)