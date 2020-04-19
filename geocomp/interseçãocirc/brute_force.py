from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import disc
from geocomp.common.control import sleep
from geocomp import config

def Brute_force (l):
    "Algoritmo força bruta para encontrar todos as interseções entre uma lista de círculos"

    for i in l:
        i.hilight()
        for j in l:
            j.hilight()
            sleep()
            for p in i.intersection(j):
                p.hilight('red')
            j.unhilight()
        i.unhilight()
    
    
