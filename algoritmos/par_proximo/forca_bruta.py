#!/usr/bin/env python
"""Algoritmo forca-bruta"""

from estruturas.segment import Segment
from geocomp.common.prim import *
from desenhos import sleep
import math

def forca_bruta (l):
    "Algoritmo forca bruta para encontrar o par de pontos mais proximo"
    "Recebe uma lista de pontos l"

    if len (l) < 2: return None
    
    closest = float("inf")
    a = b = None

    for i in range (len(l)):
        for j in range (i + 1, len (l)):
            l[i].lineto(l[j], 'orange')
            sleep()
            l[i].remove_lineto(l[j])
            
            dist = dist2 (l[i], l[j])
            if dist < closest:
                if a is not None: 
                    a.unhilight ()
                    b.unhilight ()
                    a.remove_lineto (b)

                closest = dist
                a = l[i]
                b = l[j]

                a.hilight ("green")
                b.hilight ("green")
                a.lineto (b, "green")
                sleep()

    a.hilight('orange')
    b.hilight('orange')
    a.lineto (b, 'orange')
    ret = Segment (a, b)
    return ret