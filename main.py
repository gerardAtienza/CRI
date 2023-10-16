import numpy as np
import copy
#Implementació dels mots encreuats utilitzant backtracking


class slot:
    def __init__(self, posIn = (-1,-1), long = -1, orientacio = -1, id = -1):
        self.posIn = posIn #Posicio Inicial
        self.long = long #Longitud del slot
        self.orientacio = orientacio #0 = Horitzontal, 1 = Vertical
        self.id = id #Identificador del slot
        self.pars = [] #Paraules adients al slot
        

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

def ordenaISeleccionaParaules(paraules, slots): #Funcio que inicialitza la llista de paraules del atribut pars de la classe slot
    for slot in slots:
        for paraula in paraules:
            p = paraula.strip()
            if slot.long == len(p):
                slot.pars.append(p)

def dividirTauler(tauler): #Funcio que inicialitza els slots en si
    slots = []
    id = 1

    #Horitzontals
    for i, fila in enumerate(tauler): #Coordenada y
        c = 0
        for j, el in enumerate(fila):
            if el == '0':
                c+=1
                if (c == 6 or j == 5):
                    if c > 1:
                        tupla=(i, (j-c)+1)
                        slots.append(slot(tupla , c , 0, id))
                        id+=1
                        c=0
            else:
                if c > 1:
                    tupla = (i, (j-c))
                    slots.append(slot(tupla, c, 0, id))
                    id+=1
                c=0
    
    #verticals
    for z, col in enumerate(tauler.T):
        c1 = 0
        for y, ele in enumerate(col):
            if ele == '0':
                c1+=1
                if (c1 == 7 or y == 6):
                    if c1 > 1:
                        tupla=(z, (y-c1)+1) #
                        slots.append(slot(tupla , c1 , 1, id))
                        id+=1
                        c1=0
            else:
                if c1 > 1:
                    a1 = slot((z,y-c1), c1, 1, id)
                    id+=1
                    slots.append(a1)
                c1=0

    return slots

def satisfaRestriccions(paraula, slot, tauler):
    p = list(paraula)
    if len(p) == slot.long:
        if slot.orientacio == 0:  # Horizontal
            f = slot.posIn[0]
            c = slot.posIn[1]
            for j in range(slot.long):
                if tauler[f][c + j] != '0' and tauler[f][c + j] != p[j]:
                    return False
        else:  # Vertical
            if paraula == 'RA':
                print("a")
            f = slot.posIn[0]
            c = slot.posIn[1]
            for j in range(slot.long):
                if tauler[c + j][f] != '0' and tauler[c + j][f] != p[j]:
                    return False
        return True
    return False
    
    
def solucio(tauler, slots): #Comprovacio de si el tauler es una solucio completa o no
    for fila in tauler:
        if '0' in fila:
            return False
    print(tauler)
    return True
    
def backtracking(tauler, slots, slot_id, palabras_utilizadas):
    if slot_id == len(slots): #Si hem omplert tots els slots mirem si es una solucio completa
        return solucio(tauler, slots)

    slot = slots[slot_id] #Slot que estem mirant actualment
    for par in slot.pars: #Per cada una de les paraules que van be en el slot
        if par not in palabras_utilizadas and satisfaRestriccions(par, slot, tauler): #Comprovem si satisfà les restriccions i que no l'haguem utilitzat abans
            estatAnterior = copy.deepcopy(tauler) #Guardem el estat anterior del tauler per si fallem i hem de tornar enrere
            if slot.orientacio == 0: #Horizontal (Insertem la paraula en l'slot)
                f = slot.posIn[0]
                c = slot.posIn[1]
                for i, lletra in enumerate(par):
                    tauler[f][c + i] = par[i]
            else: #Vertical (Insertem la paraula en l'slot)
                f = slot.posIn[0]
                c = slot.posIn[1]
                for i, lletra in enumerate(par):
                    tauler[c + i][f] = par[i]
            palabras_utilizadas.append(par) #Afegim la paraula a la llista de paraules ja utilitzades
            if backtracking(tauler, slots, slot_id + 1, palabras_utilizadas): #Ens movem al següent slot
                return True
            # Si falle, desfem els canvis fets en la ultima iteració i treiem la paraula que hem provat del llistat de paraules usades per tal de que els altres slots també la puguin utilitzar
            if par in palabras_utilizadas:
                palabras_utilizadas.remove(par)
            tauler = estatAnterior #Si el backtracking falla, restaurem el tauler i provem una altra paraula en l'slot
    return False

            

paraules, tauler = llegeixFitxers('diccionari_CB_v3.txt', 'crossword_CB_v3.txt')
slots = dividirTauler(tauler)
ordenaISeleccionaParaules(paraules, slots)
pars = []
if backtracking(tauler, slots, 0, pars) == False:
    print("No hi ha una solucio completa")