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
    return " ".join(llista)
#
def proposa_joc(paraules, pesos):
    """ a partir d'un diccionari { pes: [paraules] } proposa
    el joc tot combinant les paraules maximitzant el pes """
    while True:
        frase = composa_frase(paraules)
        if frase == "":
            break
        print frase
#
def carrega_pesos():
    """ carrega la informació de pesos guardada a FITXER_PESOS 
    i la retorna """
    pass
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

