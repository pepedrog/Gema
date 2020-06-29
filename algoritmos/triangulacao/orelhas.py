#!/usr/bin/env python
"""
Algoritmo de Remoção de Orelhas para Triangulação de Polígonos
Pedro Gigeck Freire - nUSP 10737136
"""

from estruturas.point import Point
from estruturas.segment import Segment
from estruturas.polygon import Polygon
from estruturas.prim import left, left_on
from desenhos import sleep

def intersecta_borda (u, w, P):
    """ Função que recebe dois vértices u e w do polígono P e retorna se o 
        segmento uw intersecta alguma aresta de P
        (equivalente a função QuaseDiagonal dos slides)
    """
    borda = P.edges()
    uw = Segment (u, w)
    for aresta in borda:
        aresta.plot ('green')
        sleep()
        if (u not in aresta.endpoints()) and (w not in aresta.endpoints()):
            if (uw.intersects (aresta)):
                aresta.hide()
                aresta.plot('red')
                sleep()
                aresta.hide()
                return True
        aresta.hide()
        
    return False

def dentro_do_poligono (u, w, P):
    """ Função que recebe dois vértices u e w do polígono P e retorna se a 
        candidata a diagonal uw está pra dentro do polígono
        (equivalente a função NoCone dos slides)
    """
    prevU = u.prev
    nextU = u.next
    if (left_on (prevU, u, nextU)):
        resposta = (left (u, w, prevU) and left (w, u, nextU))
    else:
        resposta = not (left_on (u, w, nextU) and left_on (w, u, prevU))
    
    if not resposta:
        uw = Segment (u, w)
        uw.plot ('red')
        sleep()
        uw.hide()

    return resposta

def is_diagonal (u, w, P):
    """ Função que recebe dois vértices u e w do polígono P e retorna se uw é 
        uma diagonal de P
    """
    # colore a candidata a diagonal
    uw = Segment (u, w)
    uw.plot ('green')
    sleep()

    # Como o dentroDoPoligono é O(1) é muito prudente fazer esse teste primeiro
    result = dentro_do_poligono (u, w, P) and (not intersecta_borda (u, w, P))
    uw.hide()
    return result

def is_orelha (v, P):
    " Função que recebe um vértice v do polígono P e retorna se v é uma ponta de orelha "
    v.hilight('green')

    resposta = is_diagonal (v.prev, v.next, P)
    v.unhilight()
    
    if resposta:
        v.hilight()
    sleep()
    return resposta


def orelhas (poligono):
    """ Algoritmo que usa a estratégia de encontrar e remover orelhas para
        triangular o polígono
    """
    # Cria uma cópia pra não zoar o input original
    novo = []
    for p in poligono.vertices():
        novo.append (Point (p.x, p.y))
    P = Polygon (novo)
    
    n = len(P.vertices())
    
    # Dicionario que relaciona os vértices a um booleano que indica se é orelha
    # Aproveitando que os pontos são 'hashables'
    orelha = dict()
    
    #PreProcessamento dos vértices
    v = P.pts
    orelha[v] = is_orelha (v, P)
    v = v.next
    while v != P.pts:
        orelha[v] = is_orelha (v, P)
        v = v.next
    
    while n > 3:
        # Procura uma orelha
        while not orelha[v]:
            v = v.next
        
        # Sinaliza qual orelha eu escolhi
        v.hilight('firebrick')
        # Desenha a diagonal e desmarca a orelha
        v.prev.lineto (v.next, 'orange')
        orelha[v] = False
        sleep()
        
        # Tira v do polígono
        u = v.prev
        w = v.next
        w.prev = u
        u.next = w
        # Essa parte é pra lista sempre ficar circular
        # (P.pts podia ficar inacessivel dai o algoritmo entrava em loop)
        if v == P.pts:
            P.pts = P.pts.next
        
        # Confere se não criei nenhuma orelha
        orelha[u] = is_orelha (u, P)
        orelha[w] = is_orelha (w, P)
        
        v.unhilight()
        n -= 1
        
    # Despinta alguma orelha que tenha sobrado
    while not orelha[v]:
            v = v.next
    v.unhilight ()
    