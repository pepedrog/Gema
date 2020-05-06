#!/usr/bin/env python
""" Algoritmo de Linha de Varredura """

from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.guiprim import *

# distancia global para manter atualizada
d = float("inf")

def Varre (l):
    "Algoritmo de divisão e conquista para encontrar o par de pontos mais proximo"
    "Recebe uma lista de pontos l"         

    if len (l) < 2: return None
    
    global d
    d = float("inf")
    
    l = sorted(l, key = lambda x:x.x)
    
    par_min = None
    
    p_min = 0
    l[0].hilight ()
    linha_frente = control.plot_vert_line (l[0].x)
    control.sleep()
    
    control.plot_delete (linha_frente)
    l[0].unhilight()
    l[0].hilight("blue")
    linha_tras = control.plot_vert_line (l[0].x, color = "blue")
    
    for i in range (1, len(l)):
        p = l[i]
        p.hilight ()
        linha_frente = control.plot_vert_line (p.x)
        control.sleep()
        
        while p.x - l[p_min].x > d:
            control.plot_delete (linha_tras)
            l[p_min].unhilight()
            p_min += 1
            linha_tras = control.plot_vert_line (l[p_min].x, color = "blue")
        control.sleep()
            
        for q in l [p_min : i]:
            d2 = dist2 (p, q)
            if d2 < d*d:
                d = d2**0.5
                
                if par_min != None:
                    par_min.unhilight()
                
                par_min = Segment (p, q)
                par_min.hilight (color_line = "red")
                control.sleep()
        
        control.plot_delete (linha_frente)
        p.unhilight()
        l[i].hilight ("blue")
    
    control.plot_delete (linha_tras)