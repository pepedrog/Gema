# -*- coding: utf-8 -*-
""" Algoritmo do embrulho de presente (Jarvis March)
    para determinação do fecho convexo
"""

from estruturas.prim import right, collinear, dist2
from desenhos import sleep

def embrulho(P):
    """ Função principal do algoritmo """
    p_esq = P[0]
    for p in P:
        if p.x < p_esq.x or (p.x == p_esq.x and p.y < p_esq.y):
            p_esq = p 
    p_esq.hilight('orange')
    sleep()
    H = [p_esq]
    while True:
        if P[0] == H[-1]: p_i = P[1]
        else: p_i = P[0]
        p_i.hilight('firebrick')
        H[-1].lineto(p_i, 'firebrick')
        sleep()
        for p_j in P:
            if p_j == H[-1] or p_j == p_i: continue
            H[-1].lineto(p_j, 'gray')
            sleep()
            H[-1].remove_lineto(p_j)
            if (right(H[-1], p_i, p_j) or 
               (collinear(H[-1], p_i, p_j) and dist2(H[-1], p_i) < dist2(H[-1], p_j))):
                H[-1].remove_lineto(p_i)
                p_i.unhilight()
                if p_i in H: p_i.hilight('orange')
                p_i = p_j
                H[-1].lineto(p_i, 'firebrick')
                p_i.hilight('firebrick')
        H[-1].lineto(p_i, 'orange')
        p_i.hilight('orange')
        if p_i == H[0]: break
        H.append(p_i)
    return H            