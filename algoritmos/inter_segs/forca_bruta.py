from estruturas import prim
from desenhos import sleep

def forca_bruta (l):
    "Algoritmo força bruta para encontrar todos as interseções entre uma lista de segmentos"

    for s in l:
        s.plot()

    for i in range(0, len(l) - 1):
        l[i].plot ('orange')
        sleep()
        for j in range(i + 1, len(l)):
            l[j].plot ('green')
            sleep()
            if (l[i].intersects(l[j])):
                inter = l[i].intersection(l[j])
                inter.hilight('orange')
                sleep()
                l[j].hide()
            l[j].hide()
        l[i].hide()
