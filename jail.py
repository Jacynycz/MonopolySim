import random
import time
import seaborn as sns; sns.set()
import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.image as mpimg
from tablero import *

dinero_inicial = 1500

class Dados:
    def roll(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        return [d1+d2,d1==d2]

class Jugador:
    dinero = dinero_inicial
    tablero = []
    propiedades = []
    ficha = ""
    pos = 0
    carcel = False
    carcelturnos = 3
    dice = Dados()

    def __init__(self,n,tablero):
        self.ficha = n
        self.tablero = tablero

    def __str__(self):
        return self.ficha+"("+str(self.dinero)+")"

    def __repr__(self):
        return self.ficha+"("+str(self.dinero)+")"

    def roll(self,doublecount):
        roll = self.dice.roll()
        if self.carcel:
            self.carcelturnos -= 1
            if sys.argv[5] == "v":
                print (self.ficha + " intenta salir de la carcel con  " + str(roll[0]))
            if self.carcelturnos > 0:
                if not roll[1]:
                    if sys.argv[5] == "v":
                        print (self.ficha + " se queda en la carcel durante "+ str(self.carcelturnos)+" turnos más")
                    return
            if sys.argv[5] == "v":
                print (self.ficha + " sale de la carcel")
            self.carcel = False
            self.carcelturnos = 3
        if doublecount == 2 and roll[1]:
            self.gotojail()
        else:
            self.pos = (self.pos + roll[0]) %  40
            tablero.b[self.pos].trigger(self)
            if sys.argv[5] == "v":
                print (self.ficha + " rolls " + str(roll[0]) + " and hits "+self.tablero[self.pos].nombre)
            tablero.rolls += 1
            if roll[1]:
                if sys.argv[5] == "v":
                    print (self.ficha + " vuelve a tirar")
                self.roll(doublecount+1)


    def gotojail(self):
        if sys.argv[5] == "v":
            print (self.ficha + " va a la carcel")
        # self.tablero[10].hits += 1
        self.carcel = True
        self.pos = 10
        self.tablero.numcarcel += 1

tablero = Tablero()

fichas = ["plancha","sombrero","gato","perro","barco","coche","dino","pato"]

hm = np.zeros((11,11),dtype=float)
mask = np.full((11,11), True, dtype=bool)
nsims = 1
totalrolls = 0

for iterations in range(0,int(sys.argv[3])):

    jugadores = []
    for i in range(0,int(sys.argv[1])):
        jugadores.append(Jugador(fichas[i],tablero))

    numplayers = int(sys.argv[1])
    steps = int(sys.argv[2])
    for p in range(0,steps):
        for p in jugadores:
            p.roll(0)

    for casilla in tablero.b:
        mask[casilla.pos[1],casilla.pos[0]]=False
        porcx = casilla.hits / tablero.rolls
        casilla.perc += casilla.hits#float("{0:.4f}".format(porcx*0.83+casilla.perc*0.17))
        hm[casilla.pos[1],casilla.pos[0]]=casilla.perc
        #print(casilla.nombre+ ": "+str(porc)+"% ("+str(casilla.hits)+")")
    if iterations%100 == 0:
        print("Simulando... "+str(float("{0:.1f}".format(nsims/int(sys.argv[3])*100)))+"%")
    nsims+=1
    totalrolls += tablero.rolls
    tablero.reset()

print("% Carcel: "+str(tablero.numcarcel/totalrolls*100))

if int(sys.argv[4]) > 0:
    minval = np.inf
    for casilla in tablero:
        if hm[casilla.pos[1],casilla.pos[0]] < minval:
            minval = hm[casilla.pos[1],casilla.pos[0]]
    for i in range(1,10):
        for j in range(1,10):
            hm[i,j]=minval

map_img = mpimg.imread('mono.png')

if int(sys.argv[4]) > 0:
    ax = sns.heatmap(hm, cmap="hot_r",mask = mask,center = minval,cbar = False)
else:
    ax = sns.heatmap(hm, cmap="hot_r",mask = mask,cbar = False)
sum = 0
for casilla in tablero.b:
    sum+=casilla.perc/totalrolls
    print(casilla.nombre+": "+"{0:.2f}".format(casilla.perc/totalrolls*100)+"%")

print("Total "+str(sum*100))
ax.invert_yaxis()


plt.imshow(map_img,aspect = ax.get_aspect(),
extent = ax.get_xlim() + ax.get_ylim(),
zorder = 0)
plt.show()
ax.get_figure().savefig("jail_"+sys.argv[1]+"p_"+sys.argv[2]+"rolls_"+sys.argv[3]+"its.png")
