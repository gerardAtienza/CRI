import numpy as np
import copy
#Implementació dels mots encreuats utilitzant backtracking


class slot:
    def __init__(self, posIn = (-1,-1), long = -1, orientacio = -1, cross = [((-1, -1), -1)], id = -1):
        self.posIn = posIn #Posicio Inicial
        self.long = long #Longitud del slot
        self.orientacio = orientacio #0 = Horitzontal, 1 = Vertical
        self.cross = cross #Llista d'encreuaments ((x, y), id)
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
        for j, el in enumerate(fila): #Coordenada x
            if el == '0':
                c+=1
                if (c == 6 or j == 5):
                    if c > 1:
                        tupla=(i, (j-c)+1)
                        slots.append(slot(tupla , c , 0, None, id))
                        id+=1
                        c=0
            else:
                if c > 1:
                    tupla = (i, (j-c))
                    slots.append(slot(tupla, c, 0, None, id))
                    id+=1
                c=0
    
    #verticals
    for z, col in enumerate(tauler.T):
        c1 = 0
        crosses = []
        for y, ele in enumerate(col):
            if ele == '0':
                c1+=1
                if (c1 == 6 or y == 6):
                    if c1 > 1:
                        tupla=(z, (y-c1)+1) #
                        slots.append(slot(tupla , c1 , 1, crosses, id))
                        id+=1
                        c1=0
            else:
                if c1 > 1:
                    a1 = slot((y-c1,z), c1, 1, crosses, id)
                    id+=1
                    slots.append(a1)
                c1=0

    return slots

def satisfaRestriccions(paraula, slot, tauler): #Funcio que mira si la paraula escollida compleix les restriccions imposades.
    p = list(paraula)
    if len(p) == slot.long:
        if slot.orientacio == 0:
            satisfa = True
            for j in range(slot.long-1):
                f = slot.posIn[0]
                c = slot.posIn[1]
                if tauler[f][c+j] != '0' and tauler[f][c+j] != p[j]:
                    satisfa = False
                    break
        else:
            satisfa = True
            for j in range(slot.long):
                f = slot.posIn[1]
                c = slot.posIn[0]
                if j+f > slot.long + slot.posIni[1]:
                    if tauler[f+j][c] != '0' and tauler[f+j][c] != p[j]:
                        satisfa = False
                        break
        return satisfa
    
    
def solucio(tauler, slots): #Comprovacio de si el tauler es una solucio completa o no
    for fila in tauler:
        if '0' in fila:
            return False
    return True
    
def backtracking(tauler, slots, slot_id):
    if slot_id == len(slots): #Si hem passat per tots els slots comprovem si es una solucio completa
        return solucio(tauler, slots)

    slot = slots[slot_id] #Slot que estem mirant ara
    for par in slot.pars: #Per una de les paraules de la llista pars
        if satisfaRestriccions(par, slot, tauler): #Mirem si satisfa les restriccions
            estatAnterior = copy.deepcopy([fila[:] for fila in tauler]) #Guardem el estatAnterior a aquesta iteracio del backtracking per si falla i hem de tirar enrere

            if slot.orientacio == 0: #Horitzontal (Enxufem la paraula al slot)
                f = slot.posIn[0]
                c = slot.posIn[1]
                for i, lletra in enumerate(par):
                    tauler[f][c+i] = par[i]
            else: #Vertical (Enxufem la paraula al slot)
                f = slot.posIn[1]
                c = slot.posIn[0]
                for i, lletra in enumerate(par):
                    tauler[f+i][c] = par[i]
            
            for slot in slots: #Treiem la paraula de la llista de paraules perque no l'hem de fer servir mes
                if slot.long == len(par):
                    slot.pars.remove(par)
            
            if backtracking(tauler, slots, slot_id+1): #Anem a per el següent slot
                
                return True
            
            tauler = [fila[:] for fila in estatAnterior] #Si backtracking falla tornem el tauler al seu estat anterior per provar una nova paraula al slot i tirar endavant a veure si funciona
    return False
            

paraules, tauler = llegeixFitxers('diccionari_CB_v3.txt', 'crossword_CB_v3.txt')
slots = dividirTauler(tauler)
ordenaISeleccionaParaules(paraules, slots)
if backtracking(tauler, slots, 0):
    print(tauler)
else:
    print("No hi ha solucio bro")
