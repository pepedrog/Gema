# -*- coding: utf-8 -*-
""" Algoritmo de Graham (Graham Scan) para determinação do Fecho Convexo """

from estruturas.prim import right, collinear, dist2, area2
from desenhos import sleep

eps = 1e-4

def compara (p_min, p1, p2):
    " Comparação angular para pré-processamento dos pontos "
    p_min.lineto(p1, 'gray')
    p_min.lineto(p2, 'gray')
    p1.lineto(p2, 'gray')
    sleep()
    p_min.remove_lineto(p1)
    p_min.remove_lineto(p2)
    p1.remove_lineto(p2)
    if (right(p_min, p1, p2) or 
       (abs(area2(p_min, p1, p2)) < eps and dist2(p_min, p1) < dist2(p_min, p2))): 
        return 1
    return 0

def intercala (p_esq, p_dir, p_min):
    " Intercala do MergeSort "
    ini_esq = ini_dir = 0
    P = []
    while ini_esq < len(p_esq) and ini_dir < len(p_dir):
        if compara(p_min, p_esq[ini_esq], p_dir[ini_dir]):
            P.append (p_dir[ini_dir])
            ini_dir += 1
        else:
            P.append (p_esq[ini_esq])
            ini_esq += 1
    while ini_dir < len(p_dir):
        P.append (p_dir[ini_dir])
        ini_dir += 1
    while ini_esq < len(p_esq):
        P.append (p_esq[ini_esq])
        ini_esq += 1
    return P
            
def ordena_angular (P, p_min):
    " MergeSort para ordenar pelo angulo "
    if len(P) == 1: return P
    q = int(len(P)/2)
    p_esq = ordena_angular(P[:q], p_min) 
    p_dir = ordena_angular(P[q:], p_min)
    P = intercala(p_esq, p_dir, p_min)
    return P
    
def pre_processa (P):
    for i in range(len(P)):
        if(P[i].y < P[0].y or 
          (P[i].y == P[0].y and P[i].x > P[0].x)): 
            P[0], P[i] = P[i], P[0]
    P[0].hilight('orange')
    P[1:] = ordena_angular(P[1:], P[0])
    return P
    
def graham (P):
    """ Função principal do algooritmo """
    P = pre_processa(P)
    if len(P) < 3: return P
    P[1].hilight('orange')
    P[0].lineto(P[1], 'orange')
    P[2].hilight('orange')
    P[1].lineto(P[2], 'orange')
    sleep()
    H = P[:3]
    
    for p in P[3:]:
        p.hilight ('orange')
        H[-1].lineto (p, 'orange')
        sleep()
        while (right (H[-2], H[-1], p) or
              (abs(area2(H[-2], H[-1], p)) < eps and dist2(H[-2], H[-1]) < dist2(H[-2], p))):
            H[-1].hilight ('firebrick')
            H[-2].remove_lineto (H[-1])
            H[-1].remove_lineto (p)
            H[-2].lineto (H[-1], 'firebrick')
            H[-1].lineto (p, 'firebrick')
            sleep()
            H[-1].unhilight()
            H[-2].remove_lineto (H[-1])
            H[-1].remove_lineto (p)
            H.pop()
            H[-1].lineto (p, 'orange')
            sleep()
        H.append(p)
    if collinear (H[-2], H[-1], H[0]):
        H[-2].remove_lineto(H[-1])
        H[-1].unhilight()
        H.pop()
    H[-1].lineto (H[0], 'orange')
    return H