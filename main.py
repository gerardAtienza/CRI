import numpy as np
import copy
import time
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
                if (c == tauler.shape[1] or j == tauler.shape[1]-1):
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
                if (c1 == tauler.shape[0] or y == tauler.shape[0]-1):
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
            f = slot.posIn[0]
            c = slot.posIn[1]
            for j in range(slot.long):
                if tauler[c + j][f] != '0' and tauler[c + j][f] != p[j]:
                    return False
        return True
    return False
    
    
def solucio(tauler): #Comprovacio de si el tauler es una solucio completa o no
    for fila in tauler:
        if '0' in fila:
            return False
    print(tauler)
    return True
    
def backtracking(tauler, slots, slot_id, palabras_utilizadas):
    if slot_id == len(slots): #Si hem omplert tots els slots mirem si es una solucio completa
        return solucio(tauler)

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

def ActualitzaDominis(tauler, slots, paraules_usades): #El que farà la funció es eliminar paraules de la llista de paraules dels slots si no compleixen les restriccions, per tal de reduir el temps de busqueda
    for slot in slots:
        if not slot.pars:  # Si el slot ya está lleno, continúa con el siguiente
            continue

        palabras_validas = []
        f, c = slot.posIn[0], slot.posIn[1]

        for par in slot.pars:
            if par not in paraules_usades and satisfaRestriccions(par, slot, tauler):
                if slot.orientacio == 0:
                    # Verificar la letra actual del slot horizontal
                    i = c - slot.posIn[1]
                    if i >= 0 and tauler[f][c + i] != par[i]:
                        continue
                    i = c - slot.posIn[1] + len(par) - 1
                    if i < len(tauler[f]) and tauler[f][i] != par[i]:
                        continue
                else:
                    # Verificar la letra actual del slot vertical
                    i = f - slot.posIn[0]
                    if i >= 0 and tauler[f + i][c] != par[i]:
                        continue
                    i = f - slot.posIn[0] + len(par) - 1
                    if i < len(tauler) and tauler[f + i][c] != par[i]:
                        continue

                palabras_validas.append(par)

        slot.pars = palabras_validas

        if not palabras_validas:
            return False  # No hay palabras válidas para esta ranura

    return True


def backForwardChecking(tauler, slots, slot_id, palabras_utilizadas, anterior):
    if slot_id == len(slots):
        return solucio(tauler)

    slot = slots[slot_id]

    if not slot.pars:
        return backForwardChecking(tauler, slots, slot_id + 1, palabras_utilizadas, anterior)

    palabras_validas = [par for par in slot.pars if par not in palabras_utilizadas and satisfaRestriccions(par, slot, tauler)]

    for par in palabras_validas:
        palabras_utilizadas.append(par)

        estatAnterior = copy.deepcopy(tauler)

        if slot.orientacio == 0:
            f, c = slot.posIn[0], slot.posIn[1]
            for i, lletra in enumerate(par):
                tauler[f][c + i] = par[i]
        else:
            f, c = slot.posIn[0], slot.posIn[1]
            for i, lletra in enumerate(par):
                tauler[c + i][f] = par[i]

        # Realizar forward checking después de colocar la palabra
        if ActualitzaDominis(tauler, slots, palabras_utilizadas):
            if backForwardChecking(tauler, slots, slot_id + 1, palabras_utilizadas, anterior):
                return True

        tauler = estatAnterior
        palabras_utilizadas.remove(par)
    return False


            
print("BACKTRACKINGS AMB DICCIONARI PETIT")
paraules, tauler = llegeixFitxers('diccionari_CB_v3.txt', 'crossword_CB_v3.txt')
slots = dividirTauler(tauler)
ordenaISeleccionaParaules(paraules, slots)
pars = []
temps_ini = time.time()
print("Solucio backtracking senzill")
if not backtracking(tauler, slots, 0, pars):
    print("No hi ha una solucio completa")
temps_fi = time.time()

print(f'Temps backtracking senzill: {temps_fi - temps_ini}')

paraules1, tauler1 = llegeixFitxers('diccionari_CB_v3.txt', 'crossword_CB_v3.txt')
slots1 = dividirTauler(tauler1)
ordenaISeleccionaParaules(paraules1, slots1)
pars1 = []
anterior = []
temps_ini1 = time.time()
print("Solucio backtracking amb fw checking")
if not backForwardChecking(tauler1, slots1, 0, pars1, anterior):
    print("No hi ha una solucio completa pel fw checking")
temps_fi1 = time.time()

print(f'Temps del backtracking amb fw checking: {temps_fi1 - temps_ini1}')

print("BACKTRACKING AMB DICCIONARI TOXISIMO")
paraules2, tauler2 = llegeixFitxers('diccionari_A.txt', 'crossword_A.txt')
slots2 = dividirTauler(tauler2)
ordenaISeleccionaParaules(paraules2, slots2)
pars2 = []
temps_ini2 = time.time()
print("Solucio backtracking gran amb fw checking")
if not backForwardChecking(tauler2, slots2, 0, pars2):
    print("No hi ha una solucio completa pel fw checking")
temps_fi2 = time.time()

print(f'Temps del backtracking gran amb fw checking: {temps_fi2 - temps_ini2}')