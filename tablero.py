import sys

class Casilla:
    """Class casilla"""
    nombre = ''
    hits = 0
    perc = 0
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
        self.nombre = "ve a la Carcel"

    def trigger(self,player):
        if sys.argv[5] == "v":
            print (player.ficha + " hits gotojail")
        super().trigger(player)
        player.gotojail()
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
        self.nombre = "Impuesto de mierda"
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

class Tablero(object):
    """docstring for Tablero."""

    b = []
    rolls = 0
    tiers = [[],[1,3],[6,8,9],[11,13,14],[16,18,19],[21,23,24],[26,27,29],[31,32,34],[37,39]]
    numcarcel = 0

    def __init__(self):
        self.rolls = 0
        self.b = [
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

    def reset(self):
        self.rolls = 0
        for cas in self.b:
            cas.hits = 0
