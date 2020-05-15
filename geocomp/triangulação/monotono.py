#!/usr/bin/env python
"""
Algoritmo de Remoção de Orelhas para Triangulação de Polígonos
Pedro Gigeck Freire - nUSP 10737136
"""

from geocomp.common.segment import Segment
from geocomp.common.prim import left, left_on
from geocomp.common.control import sleep


def separaBordas (P):
    """ Função que recebe um polígono monótono P e retorna duas listas de vértices:
        a curva polígonal da esquerda e direita, ambas ordenadas pela y coordenada
    """    
    # acha os extremos do polígono
    cima = baixo = P.pts
    p = P.pts.next
    while p != P.pts:
        if p.y > cima.y:
            cima = p
        if p.y < baixo.y:
            baixo = p
        p = p.next
    
    # constroi as bordas
    borda_esq = borda_dir = []
    p = cima
    while p != baixo:
        p.hilight ("red")
        borda_esq.append (p)
        p = p.next
    p = cima.prev
    while p != baixo:
        p.hilight ("blue")
        borda_dir.append (p)
        p = p.prev
    baixo.hilight ("blue")
    borda_dir.append (baixo)
    
    sleep()
    return borda_esq, borda_dir
    
    
def Monotono (p):
    
    # Essa é a forma que eu recebo o polígono do front-end :/
    P = p[0]
    n = len(P.vertices())
    
    borda_esq, borda_dir = separaBordas (P)
    
    