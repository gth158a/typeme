#! /usr/bin/env python
# encoding: utf-8
#
#
# Programa que permet practicar mecanografia
# Recull paraules d'un fitxer, en construeix frases (no
# necessàriament amb sentit) i les demana fins que 
# l'usuari és capaç d'escriure cada paraula
# prou vegades sense error.
#
# Les paraules són agrupades segons un pes. El pes es calcula a
# partir d'un algorisme que considera, entre altres elements, les
# els errors de l'usuari en teclejar els caracters que la composen.
#
# Aquesta versió és monousuari. Per tant, cada cop que es faci 
# servir, els pesos es calcularan en funció de l'usuari anterior.
#
# Requereix rebre per paràmetre el nom d'un fitxer accessible per 
# lectura amb les paraules.

#
import os, sys
import random
import optparse
#
DESCR_FUNCIONAMENT="Practica mecanografia."
SENTENCE_MAX_LENGTH = 70    # max lenght of a sentence
#
class Dit:
    """ encapsula la informació de quin dit cal per teclejar un caràcter """    # definició dels dits
    # els dits queden numerats:
    #   del 0 al 9 començant pel petit esquerre quan és un sol dit
    #   del 10 al 19 quan cal prèmer la tecla de majúscules
    #   del 20 al 29 quan cal prèmer la tecla Alt-Gr
    #   del 30 al 39 quan cal prèmer un accent (ex. per 'è')
    # per cada caràcter teclejable, s'indiquen els dits requerits
    # Algunes numeracions poden no aparéixer mai donat que
    # no hi ha cap caràcter "estàndard" associat. Ex. 33 (AltGr+f)
    # En tot cas, si es requereix, hi cap. Ex. al meu teclat '«' s'obté 
    # de AltGr+z i potser em pot ser interessant practicar-ho!
    # TODO: aquesta és una part que s'ha de poder configurar a cada
    # usuari. Hauria d'aparéixer a algun fitxer de configuració.
    dits = {
            "ª" : 10,
            "º" : 0,
            "\\": 20,
            "\t": 0,
            "!" : 10,
            "1" : 0,
            "|" : 20,
            "q" : 0,
            "Q" : 10,
            "a" : 0,
            "A" : 10,
            "<" : 0,
            ">" : 10,
            "z" : 0,
            "Z" : 10,
            "2" : 1,
            "\"": 11,
            "@" : 21,
            "w" : 1,
            "W" : 11,
            "s" : 1,
            "S" : 11,
            "x" : 1,
            "X" : 11,
            "3" : 2,
            "·" : 12,
            "#" : 22,
            "e" : 2,
            "E" : 12,
            "€" : 22,
            "d" : 2,
            "D" : 12,
            "c" : 2,
            "C" : 12,
            "4" : 3,
            "$" : 13,
            "~" : 23,
            "r" : 3,
            "R" : 13,
            "f" : 3,
            "F" : 13,
            "v" : 3,
            "V" : 13,
            "5" : 3,
            "%" : 13,
            "t" : 3,
            "T" : 13,
            "g" : 3,
            "G" : 13,
            "b" : 3,
            "B" : 13,
            "6" : 6,
            "&" : 16,
            "y" : 6,
            "Y" : 16,
            "h" : 6,
            "H" : 16,
            "n" : 6,
            "N" : 16,
            "7" : 6,
            "/" : 16,
            "u" : 6,
            "U" : 16,
            "j" : 6,
            "J" : 16,
            "m" : 6,
            "M" : 16,
            "8" : 7,
            "(" : 17,
            "i" : 7,
            "I" : 17,
            "k" : 7,
            "K" : 17,
            "," : 7,
            ";" : 17,
            "9" : 8,
            ")" : 18,
            "o" : 8,
            "O" : 18,
            "l" : 8,
            "L" : 18,
            "." : 8,
            ":" : 18,
            "0" : 9,
            "=" : 19,
            "p" : 9,
            "P" : 19,
            "ñ" : 9,
            "Ñ" : 19,
            "-" : 9,
            "_" : 19,
            "'" : 9,
            "?" : 19,
            "[" : 29,
            "{" : 29,
            "¡" : 9,
            "¿" : 19,
            "+" : 9,
            "*" : 19,
            "]" : 29,
            "ç" : 9,
            "Ç" : 19,
            "}" : 29,
            "à" : 30,
            "á" : 30,
            "è" : 32,
            "é" : 32,
            "í" : 37,
            "ò" : 38,
            "ó" : 38,
            "ú" : 36 
    }

    @staticmethod
    def corresponent(caracter):
        """ retorna el dit corresponent al caràcter.
        Si no està registrat, retorna el dit -1."""
        return Dit.dits.get(caracter, -1)
#
class Pes:
    """ encapsula tota la informació requerida per a calcular els pesos """
    def __init__(self):
        pass
    def default(self):
        """ calcula els valors per defecte del pes """
        # caracters amb un pes superior al de per defecte (0)
        # inicialment no hi ha cap caràcter especial
        self.caracters = dict() # {char: pes}

        # parelles de caracters amb un pes superior al de 
        # per defecte.
        # inicialment no hi ha cap parella especial
        self.parella_caracters= dict()  # { chars: pes }

        # dits amb un pes especial al de per defecte
        # inicialment no hi ha cap dit especial
        self.dits = dict()

        # parelles de dits amb un pes especial al de per defecte
        # inicialment no hi ha cap parella de dits especial
        self.parella_dits = dict()

    def registra_error(self, paraula, pos):
        """ registra l'error a la posició pos de la paraula """
# TODO: cal fer ús de la posició per guardar, a més del caràcter amb error
# la parella que forma amb l'anterior.
# També seria interesant trobar la manera com gestionar el backspace
        pass

    def registra_temps(self, paraula, pos, temps):
        """ registra el temps requerit per a escriure el caràcter de
        la posició pos dins de la paraula """
        # TODO: cal definir el model de dades que suporti aquesta informació. També cal que el mètode que registra les entrades de l'usuari, vagi guardant informació de temps relatiu per cada caràcter de cada paraula!
        pass
        # TODO: caldrà definir funcions que permetin recalcular
# pesos en funció del caràcter que s'ha fallat, la parella amb el caràcter previ, i el dit que corresponia al caràcter i els dits que corresponen a les parelles de caràcters.
#
def obte_arguments():
    """ retorna els arguments de la crida al programa en forma d'opcions de optparse """
    p = optparse.OptionParser(description = DESCR_FUNCIONAMENT, version="1.0")
    p.add_option("-f", "--fitxer_entrenament", action="store", help=u"Número identificador de l'exercici", nargs=1, dest="fitxer")
    opcions, _ = p.parse_args()
    return opcions
#
def valida_arguments(opcions):
    """ valida els arguments d'un optparse.
    Retorna True si tot correcte o finalitza l'execució altrament. """
    if not opcions.fitxer:
        print >> sys.stderr, "Error: cal especificar el fitxer amb " +\
                "les paraules d'entrenament"
        sys.exit(1)
    #
    if not os.access(opcions.fitxer, os.R_OK):
        print >> sys.stderr, "Error: no es pot llegir %s"\
            %opcions.fitxer
        sys.exit(2)
    #
    return True
#
def calcula_pes(paraula, pesos):
    """ a partir dels pesos, retorna el pes d'una paraula """
    return len(paraula)
#
def carrega_paraules(fitxer, pesos):
    """ carrega les paraules del fitxer, les assigna un pes i les 
    retorna en forma de diccionari { pes: [paraules] } 
    Si no pot carregar les paraules, surt """
    paraules = dict()
    try:
        f = open(fitxer)
        contingut = f.readlines()
        f.close()
    except IOError, e:
        print >> sys.stderr, "Error: no s'ha pogut llegir %s"%fitxer
        sys.exit(2)
    #
    for p in [x.strip() for x in contingut]:
        pes = calcula_pes(p, pesos)
        if pes in paraules.keys():
            if p not in paraules[pes]: # ignora repetits
                paraules[pes].append(p)
        else:
            paraules[pes]=[p]
    return paraules
#
def selecciona_paraula(paraules, longitud_max):
    """ selecciona una paraula del diccionari de paraules
    tal que maximitzi el pes i la seva longitud no
    sigui superior a longitud_max.
    Si la troba, l'elimina de paraules i la retorna.
    Si no la troba, retorna la cadena buida """
    p = ""
    claus = paraules.keys()
    claus.sort()
    claus.reverse()
    for c in claus:
        random.shuffle(paraules[c])
        for v in paraules[c]:
            if len(v) <= longitud_max:
                p = v
                paraules[c].remove(v)
                if len(paraules[c])==0:
                    del(paraules[c])
                break
        if p <> "":
            break
    return p
#
def composa_frase(paraules):
    """ mira de composar una frase a partir del diccionari
    paraules ({pes:[paraules]} de llargaria no superior però pròxima
    a SENTENCE_MAX_LENGTH """
    llista = list() # llista de paraules seleccionades
    longitud_disponible = SENTENCE_MAX_LENGTH + 1 # +1 for simplify blanks
    paraules_disponibles = len(paraules.values()) # optimització
    continua = len(paraules.keys()) > 0
    while paraules_disponibles > 0 and longitud_disponible > 0:
        p = selecciona_paraula(paraules, longitud_disponible)
        if p == "":
            break
            continua = False
        else:
            longitud_disponible -= 1 + len(p)
            llista.append(p)
    random.shuffle(llista)
    return llista
#
def juga_frase(frase, pesos):
    """ proposa la frase (llista de paraules) a l'usuari perquè 
    la intenti teclejar.
    Retorna True si l'usuari vol continuar jugant.
    Modifica els pesos en funció de la realització de l'usuari """
    print " ".join(frase)
    # cw = 0
    # while cw < len(frase):
    #     current_word = frase[0]
    return True
#
def proposa_joc(paraules, pesos):
    """ a partir d'un diccionari { pes: [paraules] } proposa
    el joc tot combinant les paraules maximitzant el pes """
    while True:
        frase = composa_frase(paraules)
        if frase == []:             # si no queden frases, finalitza
            print "S'han completat totes les frases. Enhorabona!"
            break
        if not juga_frase(frase, pesos):   # si no vol continuar, finalitza
            print "Finalitzada la sessió"
            break
#
def carrega_pesos():
    """ carrega la informació de pesos guardada a FITXER_PESOS 
    i la retorna """
    return Pes()
#
def guarda_pesos(pesos):
    """ guarda els pesos calculats en aquesta sessió """
    pass
#
def main():
    opcions = obte_arguments()
    valida_arguments(opcions)
    pesos = carrega_pesos()
    paraules = carrega_paraules(opcions.fitxer, pesos)
    proposa_joc(paraules, pesos)
    guarda_pesos(pesos)
    return 0
    #
#
if __name__=="__main__":
    sys.exit(main())

