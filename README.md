# MonopolySim

Scripts de simulación del monopoly para generar estadísticas.

Para poder utilzar la simulación se requiere Python3, matplotlib y seaborn.

Descarga el zip del repositorio o utiliza el comando:

```
git clone https://github.com/Jacynycz/MonopolySim
```
## Diferentes archivos de simulación

#### norules.py

Lanza una simulación básica del tablero sin tener en cuenta las normas de ir a la carcel ni las cartas de Caja de Comunidad y suerte.

La simulación dispone de una serie de argumentos para personalizar la ejecución. El comando de lanzamiento es:

```
python norules.py <numplayers> <numrolls> <numsims> <normalize>
```

- numplayers: Define el número de jugdores para la simulación
- numrolls:  Define el número de tiradas que hace cada jugador
- numsims: Define el número de simulaciónes que ejecuta
- normalize: Usa el valor 0 si cada simulación tiene menos de 100 tiradas. Si cada simulación tiene muchas tiradas utiliza el valor 1  

Ejemplo de simulación de 3 jugadores, 10 tiradas cada jugador, 10000 simulaciones sin normalizar

```
python norules.py 3 10 10000 0
```

La simulación generará un mapa de calor con las casillas más visitadas y generará una imagen en la carpeta principal.
