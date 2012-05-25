#! /usr/bin/python
# encoding: utf-8
#
# Programa que permet practicar mecanografia
# Recull seqüències de un fitxer i les demana fins que ¡
# l'usuari les escriu prou vegades sense error.
#
import os, sys, time
import termios, fcntl
import codecs
import pickle
#
N_COPS = 2      # nombre de cops que cal fer bé una seqüència
                # per passar a la següent a la sessió actual
N_REPS = 10     # nombre de cops que com a màxim es repetirà una 
                # seqüencia abans de passar a la següent
#
FITXER_DAT = "./typeme.dat" # fitxer amb la info d'execucions anteriors.
FITXER_SEQ = "./sequencies.txt" # fitxer amb les seqüències a treballar
#
# Utilitats obtingudes de http://code.activestate.com/recipes/576503-linux-terminal-color-setter/
def reset():
    sys.stdout.write("\x1bc\x1b[!p\x1b[?3;4l\x1b[4l\x1b>")
    default()
#
def default():
    sys.stdout.write("\x1b[10m")
    sys.stdout.write("\x1b[00m")

def clear():
    sys.stdout.write("\x1b[H\x1b[2J")
#
def red():
    sys.stdout.write("\x1b[01;05;37;31m")
#
def blue():
    sys.stdout.write("\x1b[01;05;37;34m")
#
# getc() obtingut de http://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
def getch():
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
    try:
        while 1:
            try:
                c = (codecs.getreader('utf-8')(sys.stdin)).read(1)
                break
            except IOError: pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    return c
#
def carrega_sequencies():
    """ carrega les seqüències.
    Surt del programa en cas que no hi siguin """
    if os.path.exists(FITXER_SEQ):
        f = codecs.open(FITXER_SEQ, 'rb', 'utf-8')
        sequencies = f.read().strip().split("\n")
        f.close()
    else:
        print >> sys.stderr, "No es troba el fitxer", FITXER_SEQ
        sys.exit(1)
    return sequencies
#
def llegeix_resposta(sequencia):
    """ llegeix la resposta de l'entrada estàndard i la retorna
    en forma de string amb un màxim de len(sequencia) caràcters 
    Remarca en vermell els caràcters que no coincideixen.
    Retorna també el % d'errors detectats i les polsacions per minut.
    Surt si <esc> i <enter>
    """
    resposta = []
    temps = 0
    nerrors = 0
    i = 0
    while i < len(sequencia):
        cs = sequencia[i]
        c = getch()
        if i==0: temps = time.time()   # inicia el comptador
        i += 1
        if ord(c) == 195:       # és un caràcter especial (com ara ñ)
            c = unichr(ord(c) + ord(getch()))
        if ord(c) == 27:    # <esc>
            return 'x',0,0    # finalitza
        if ord(c) == 127:   # <del>
            red()
            sys.stdout.write(" No es permet l'ús del DEL\n")
            blue()
            sys.stdout.write("".join(resposta))
            default()
            i -= 1
        elif c == "\n":     # vol finalitzar aquesta entrada
            red()
            sys.stdout.write(" Línia cancel·lada\n")
            default()
            nerrors += len(sequencia) - i
            break
        else:
            resposta.append(c)
            if c == cs:
                blue()
            else:
                red()
                nerrors += 1
            if c == " ":
                sys.stdout.write("·")
            else:
                sys.stdout.write(c)
            default()
    temps = time.time() - temps;
    ppm = int(round(60 * len(sequencia) / temps))
    percent = (len(sequencia) * 1.0 - nerrors) / len(sequencia)
    return "".join(resposta), percent, ppm
#
def carrega_resultats(numres):
    """ carrega els resultats passats.
    Si no els troba, els inicialitza i comença des del principi"""
    resultats = []
    try:
        resultats = pickle.load(open(FITXER_DAT))
    except:
        pass
    resultats += [ 2 for x in range(numres - len(resultats))]
    return resultats
#
#########################################
#
sequencies = carrega_sequencies()
resultats = carrega_resultats(len(sequencies))
ini = 0     # posició de la primera seqüència a realitzar
for n in range(len(resultats)):
    if resultats[n] > 0:
        ini = n
        break
#
for i in range(ini, len(sequencies)):
    sequencia = sequencies[i]
    nencerts = 0        # nombre d'encerts seguits
    nintents = 0        # nombre d'intents
    #clear()
    while resultats[i] > 0 and nintents < N_REPS and nencerts < N_COPS:
        sys.stdout.write("\n%s\n"%sequencia)
        #resposta = raw_input().strip()
        resposta, percent, ppm = llegeix_resposta(sequencia)
        if resposta == 'x':
            reset()
            print "finalitzat"
            pickle.dump(resultats, open(FITXER_DAT, 'w'))
            sys.exit(0)
        nintents += 1
        if percent == 1:
            resultats[i] -= 1
            nencerts += 1
            blue();
            sys.stdout.write("\t(%0.1f ppm)"%ppm)
        else:
            if percent < 0.95:       # només incrementa amb < 95% encert
                resultats[i] = min(N_REPS, resultats[i] + 1)
            nencerts = 0
            red()
        sys.stdout.write("\t%0.2f%%\n"%(percent*100))
        default()
#
print "Finalitzats tots els exercicis!"
pickle.dump(resultats, open(FITXER_DAT, 'w'))
