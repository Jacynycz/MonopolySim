import random
import time
import seaborn as sns; sns.set()
import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.image as mpimg

dinero_inicial = 1500

class Dados:
    def roll(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        return [d1+d2,d1==d2]

class Jugador:
    dinero = dinero_inicial
    propiedades = []
    ficha = ""
    pos = 0

    def __init__(self,n):
        self.ficha = n

    def __str__(self):
        return self.ficha+"("+str(self.dinero)+")"

    def __repr__(self):
        return self.ficha+"("+str(self.dinero)+")"


class Casilla:
    """Class casilla"""
    nombre = ''
    hits = 0
    pos = []
    def trigger(self,player):
        self.hits += 1

    def __init__(self,n,pos):
        self.pos = pos
        self.nombre = n

class Salida(Casilla):
    def __init__(self,pos):
        self.pos = pos
        self.nombre = "Salida"

    def trigger(self,player):
        super().trigger(player)
        player.dinero +=200
        #print(player.ficha + " hits salida")

class CajaComunidad(Casilla):
    def __init__(self,pos):
        self.pos = pos
        self.nombre = "Caja Comunidad"

    def trigger(self,player):
        super().trigger(player)
        #print(player.ficha + " hits caja")

class Suerte(Casilla):
    def __init__(self,pos):
        self.pos = pos
        self.nombre = "Suerte"

    def trigger(self,player):
        super().trigger(player)
        #print(player.ficha + " hits suerte")

class Carcel(Casilla):
    def __init__(self,pos):
        self.pos = pos
        self.nombre = "Carcel"

    def trigger(self,player):
        super().trigger(player)
        #print(player.ficha + " hits carcel")

class Estacion(Casilla):
    def __init__(self,n,pos):
        self.pos = pos
        self.nombre = "Estacion " + n

    def trigger(self,player):
        super().trigger(player)
        #print(player.ficha + " hits estaación "+ self.nombre)

class Servicio(Casilla):
    def __init__(self,n,pos):
        self.pos = pos
        self.nombre = "Servicio "+n

    def trigger(self,player):
        super().trigger(player)
        #print(player.ficha + " hits servicio "+ self.nombre)

class Impuesto(Casilla):
    valor = 0

    def __init__(self,v,pos):
        self.pos = pos
        valor = v

    def trigger(self,player):
        super().trigger(player)
        #print(player.ficha + " hits impuesto de "+ str(self.valor))


class Propiedad(Casilla):
    comprada = False
    precio = [0,0,0,0,0,0]
    compra = []
    estado = 0
    propietario = None
    tier = 0

    def trigger(self,player):
        super().trigger(player)
        #print(player.ficha + " hits propiedad "+ self.nombre)

    def __init__(self,n,p,c,t,pos):
        self.pos = pos
        self.nombre = n
        self.precio = p
        self.compra = c
        self.tier = t

    def __repr__(self):
        s =  "{Nombre: "+ str(self.nombre) +",\nPrecios: "+ str(self.precio) + ",\nCoste de construcción: "+ str(self.compra) + ",\nEstado: "+ str(self.estado)
        if(self.propietario is None):
            s+=",\nPropietario: none"+ "}"
        else:
            s+=",\nPropietario: "+str(self.propietario)+ "}"
        return s

    def __str__(self):
        print('Nombre: '+ self.nombre)
        print('Precios: '+ self.precio)
        print('Coste de consstrucción: '+ self.costecasas)
        print('Estado: '+ self.estado)

    def comprar(self, jugador):
        if(not self.comprada):
            if(jugador.dinero>=self.compra[0]):
                jugador.dinero -= self.compra[0]
                self.comprada = True
                self.propietario = jugador

    def mejora(self):
        if(self.comprada and self.checkSametier()):
            if(self.propietario.dinero>=self.compra[1]):
                self.propietario.dinero -= self.compra[1]
                self.estado += 1

    def checkSametier(self):
        return False

def reset(tablero):
    for cas in tablero:
        cas.hits = 0

tablero = [
Salida([10,0]),
Propiedad('Ronda de Valencia',[2,4,10,30,90,160,250],[60,50],1,[9,0]),
CajaComunidad([8,0]),
Propiedad('Plaza Lavapiés',[4,8,20,60,180,320,450],[60,50],1,[7,0]),
Impuesto(200,[6,0]),
Estacion('Goya',[5,0]),
Propiedad('Glorieta Cuatro Caminos',[6,12,30,90,270,400,550],[100,50],2,[4,0]),
Suerte([3,0]),
Propiedad('Avenida Reina Victoria',[6,12,30,90,270,400,550],[100,50],2,[2,0]),
Propiedad('Calle Bravo Murillo',[8,16,40,100,300,450,600],[120,50],2,[1,0]),
Casilla("Carcel",[0,0]),
Propiedad('Glorieta Bilbao',[10,20,50,150,450,625,750],[140,100],3,[0,1]),
Servicio("Electricidad",[0,2]),
Propiedad('Calle Alberto Aguilera',[10,20,50,150,450,625,750],[140,100],3,[0,3]),
Propiedad('Calle Fuencarral',[12,24,60,180,500,700,900],[160,100],3,[0,4]),
Estacion('Delicias',[0,5]),
Propiedad('Avenida Felipe II',[14,28,70,200,550,750,950],[180,100],4,[0,6]),
CajaComunidad([0,7]),
Propiedad('Calle Velázquez',[14,28,70,200,550,750,950],[180,100],4,[0,8]),
Propiedad('Calle Serrano',[16,32,80,220,600,800,1000],[200,100],4,[0,9]),
Casilla("Parking",[0,10]),
Propiedad('Avenida de América',[18,36,90,250,700,875,1050],[220,150],5,[1,10]),
Suerte([2,10]),
Propiedad('Calle María de Molina',[18,36,90,250,700,875,1050],[220,100],5,[3,10]),
Propiedad('Calle Cea Bermúdez',[20,40,100,300,750,925,1100],[240,150],5,[4,10]),
Estacion('Mediodía',[5,10]),
Propiedad('Avenida Reyes Católicos',[22,44,110,330,800,975,1150],[260,150],6,[6,10]),
Propiedad('Calle Bailén',[22,44,110,330,800,975,1150],[260,150],6,[7,10]),
Servicio("Aguas",[8,10]),
Propiedad('Plaza de España',[24,48,120,360,850,1025,1200],[280,150],6,[9,10]),
Carcel([10,10]),
Propiedad('Puerta del Sol',[26,52,130,390,900,110,1275],[300,200],7,[10,9]),
Propiedad('Calle Acalá',[26,52,130,390,900,1100,1275],[300,200],7,[10,8]),
CajaComunidad([10,7]),
Propiedad('Gran Vía',[28,56,150,450,1000,1200,1400],[320,200],7,[10,6]),
Estacion("Norte",[10,5]),
Suerte([10,4]),
Propiedad('Paseo de la castellana',[35,70,175,500,1100,1300,1500],[550,200],8,[10,3]),
Impuesto(100,[10,2]),
Propiedad('Paseo del prado',[50,100,200,600,1400,1700,1500],[900,200],8,[10,1])
]

tiers = [[],[1,3],[6,8,9],[11,13,14],[16,18,19],[21,23,24],[26,27,29],[31,32,34],[37,39]]

fichas = ["plancha","sombrero","gato","perro","barco","coche","dino","pato"]


hm = np.zeros((11,11),dtype=float)
mask = np.full((11,11), True, dtype=bool)

numcarcel = 0

for iterations in range(0,int(sys.argv[3])):

    jugadores = []
    for i in range(0,int(sys.argv[1])):
        jugadores.append(Jugador(fichas[i]))

    numplayers = int(sys.argv[1])

    dice = Dados()
    steps = int(sys.argv[2])
    for p in range(0,steps):
        for p in jugadores:
            doublecount = 0
            roll = dice.roll()
            p.pos = (p.pos + roll[0]) %  40
            tablero[p.pos].trigger(p)
            while doublecount < 3 and roll[1]:
                #print("-------------- DOUBE")
                doublecount += 1
                roll = dice.roll()
                p.pos = (p.pos + roll[0]) %  40
                tablero[p.pos].trigger(p)
            if doublecount == 3:
                numcarcel += 1

    for casilla in tablero:
        mask[casilla.pos[1],casilla.pos[0]]=False
        porcx = (float(casilla.hits) / float(steps*numplayers)) * 100
        porc = float("{0:.3f}".format(porcx))
        hm[casilla.pos[1],casilla.pos[0]]=hm[casilla.pos[1],casilla.pos[0]]*0.83+porcx*0.17
        #print(casilla.nombre+ ": "+str(porc)+"% ("+str(casilla.hits)+")")

    reset(tablero)
print("% Carcel: "+str(numcarcel/float(sys.argv[3])*100))

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

ax.invert_yaxis()


plt.imshow(map_img,aspect = ax.get_aspect(),
extent = ax.get_xlim() + ax.get_ylim(),
zorder = 0)
plt.show()
ax.get_figure().savefig("norules_"+sys.argv[1]+"p_"+sys.argv[2]+"rolls_"+sys.argv[3]+"its.png")
