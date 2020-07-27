""" Algoritmo de divisão e conquista MergeHull 
    para determinação do fecho convexo 
"""

from desenhos import sleep
from estruturas.prim import right, left, collinear, dist2

def draw_hull (H, cor):
    H[0].hilight (cor)
    for i in range(1, len(H)):
        H[i].hilight(cor)
        H[i].remove_lineto (H[i - 1])
        H[i].lineto (H[i - 1], cor)
    H[-1].remove_lineto (H[0])
    H[-1].lineto (H[0], cor)
    
def hide_hull (H):
    for i in range(len(H)):
        H[i].unhilight()
        H[i - 1].remove_lineto (H[i])
        H[i].remove_lineto (H[i - 1])

def tangente_inferior(h_esq, h_dir):
    """ Encontra os pontos i, j tais que a linha h_esq[i] - h_dir[j]
        deixa todos os demais pontos acima dela """
    n_esq = len(h_esq)
    n_dir = len(h_dir)
    i = j = 0
    for k in range(len(h_esq)):
        if h_esq[k].x > h_esq[i].x or (h_esq[k].x == h_esq[i].x and h_esq[k].y > h_esq[i].y): 
            i = k
    for k in range(len(h_dir)):
        if h_dir[k].x < h_dir[j].x or (h_dir[k].x == h_dir[j].x and h_dir[k].y < h_dir[j].y):
            j = k
    
    h_esq[i].remove_lineto (h_dir[j])
    h_esq[i].lineto (h_dir[j], 'blue')
    sleep()
    prox_i = (i - 1 + n_esq)%n_esq
    prox_j = (j + 1)%n_dir
    desceu = True
    while desceu:
        desceu = False
        while (right (h_esq[i], h_dir[j], h_esq[prox_i]) or 
              (collinear (h_esq[i], h_dir[j], h_esq[prox_i]) and 
               dist2(h_esq[i], h_dir[j]) < dist2(h_esq[prox_i], h_dir[j]))):
            desceu = True
            h_esq[i].remove_lineto (h_dir[j])
            i = prox_i
            prox_i = (i - 1 + n_esq)%n_esq
            h_esq[i].lineto (h_dir[j], 'blue')
            sleep()
        while (right (h_esq[i], h_dir[j], h_dir[prox_j]) or 
              (collinear (h_esq[i], h_dir[j], h_dir[prox_j]) and 
               dist2(h_dir[j], h_esq[i]) < dist2(h_dir[prox_j], h_esq[i]))):
            desceu = True
            h_esq[i].remove_lineto (h_dir[j])
            j = prox_j
            prox_j = (j + 1)%n_dir
            h_esq[i].lineto (h_dir[j], 'blue')
            sleep()
    h_esq[i].remove_lineto (h_dir[j])
    h_esq[i].lineto (h_dir[j], 'firebrick')
    sleep()
    return i, j
        
def tangente_superior(h_esq, h_dir):
    """ Encontra os pontos i, j tais que a linha h_esq[i] - h_dir[j]
        deixa todos os demais pontos abaixo dela """
    n_esq = len(h_esq)
    n_dir = len(h_dir)
    i = j = 0
    for k in range(len(h_esq)):
        if h_esq[k].x > h_esq[i].x or (h_esq[k].x == h_esq[i].x and h_esq[k].y > h_esq[i].y): 
            i = k
    for k in range(len(h_dir)):
        if h_dir[k].x < h_dir[j].x or (h_dir[k].x == h_dir[j].x and h_dir[k].y < h_dir[j].y):
            j = k
            
    h_dir[j].remove_lineto (h_esq[i])
    h_dir[j].lineto (h_esq[i], 'blue')
    sleep()
    prox_i = (i + 1)%n_esq
    prox_j = (j - 1 + n_dir)%n_dir
    subiu = True
    while subiu:
        subiu = False
        while (left (h_esq[i], h_dir[j], h_esq[prox_i]) or 
              (collinear (h_esq[i], h_dir[j], h_esq[prox_i]) and 
               dist2(h_esq[i], h_dir[j]) < dist2(h_esq[prox_i], h_dir[j]))):
            subiu = True
            h_dir[j].remove_lineto (h_esq[i])
            i = prox_i
            prox_i = (i + 1)%n_esq
            h_dir[j].lineto (h_esq[i], 'blue')
            sleep()
        while (left (h_esq[i], h_dir[j], h_dir[prox_j]) or 
              (collinear (h_esq[i], h_dir[j], h_dir[prox_j]) and 
               dist2(h_dir[j], h_esq[i]) < dist2(h_dir[prox_j], h_esq[i]))):
            subiu = True
            h_dir[j].remove_lineto (h_esq[i])
            j = prox_j
            prox_j = (j - 1 + n_dir)%n_dir
            h_dir[j].lineto (h_esq[i], 'blue')
            sleep()
    h_dir[j].remove_lineto (h_esq[i])
    h_dir[j].lineto (h_esq[i], 'firebrick')
    sleep()
    return i, j

def get_shell(h, ini, fim):
    """ Devolve a concha externa do fecho h[ini..fim] """
    H = []
    i = ini
    while i != fim:
        H.append(h[i])
        i = (i + 1)%len(h)
    H.append(h[fim])
    return H

def merge (h_esq, h_dir):
    """ Cria o fecho convexo dados pelos 2 fechos convexos h_esq e h_dir """
    esq_inf, dir_inf = tangente_inferior(h_esq, h_dir)
    esq_sup, dir_sup = tangente_superior(h_esq, h_dir)
    H = get_shell (h_esq, esq_sup, esq_inf)
    H.extend (get_shell (h_dir, dir_inf, dir_sup))
    return H

def mergehull_rec(P):
    """ Função que faz a divisão e conquista, principal do algoritmo """
    if len(P) == 1: return [P[0]]
    q = int(len(P)/2)
    h_esq = mergehull_rec (P[:q])
    draw_hull(h_esq, 'green')
    h_dir = mergehull_rec (P[q:])
    draw_hull(h_dir, 'red')
    sleep()
    m = merge (h_esq, h_dir)
    hide_hull(h_esq)
    hide_hull(h_dir)
    return m

def mergehull (P):
    """ Função principal, que na verdade só dispara a função recursiva """
    P = sorted (P, key = lambda x:(x.x*10000 + x.y))
    H = mergehull_rec (P)
    draw_hull (H, 'orange')
    sleep()
    