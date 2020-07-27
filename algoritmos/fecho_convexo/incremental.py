""" Algoritmo aleatorizado Incremental para determinação do fecho convexo """

from estruturas.prim import right, left, collinear
from desenhos import sleep
from random import shuffle

def draw_hull (H, cor):
    H[0].hilight (cor)
    for i in range(1, len(H)):
        H[i].hilight(cor)
        H[i].remove_lineto (H[i - 1])
        H[i].lineto (H[i - 1], cor)
    H[-1].remove_lineto (H[0])
    H[-1].lineto (H[0], cor)
    
def pertence (H, p):
    """ Confere se o ponto p está no fecho convexo H """
    p.hilight('green')
    for i in range (len(H)):
        j = (i + 1)%len(H)
        H[i].remove_lineto(H[j])
        H[i].lineto (H[j], 'green')
        sleep()
        H[i].remove_lineto(H[j])
        H[i].lineto (H[j], 'orange')
        if right(H[i], H[j], p):
            p.hilight('red')
            H[i].remove_lineto(H[j])
            H[i].lineto (H[j], 'red')
            sleep()
            p.unhilight()
            H[i].remove_lineto(H[j])
            H[i].lineto (H[j], 'orange')
            return False
    p.unhilight()
    return True

def desenha_teste(p, q):
    q.hilight('firebrick')
    q.lineto(p, 'firebrick')
    sleep()
    q.hilight('orange')
    q.remove_lineto(p)

def insere_ponto (H, p):
    """ Monta um fecho convexo dos pontos do fecho convexo H
        junto do ponto p """
        
    i = 0
    n = len(H)
    p.hilight('firebrick')
    desenha_teste (p, H[i])
    while left (H[i - 1], H[i], p) == left (H[i], H[(i + 1)%n], p):
        i = (i + 1)%n
        desenha_teste (p, H[i])
    H[i].hilight('firebrick')
    p.lineto(H[i], 'firebrick')
    j = (i + 1)%n
    desenha_teste (p, H[j])
    while left (H[j - 1], H[j], p) == left (H[j], H[(j + 1)%n], p):
        j = (j + 1)%n
        desenha_teste (p, H[j])
    p.hilight('orange')
    H[i].hilight('orange')
    p.remove_lineto(H[i])
    p.remove_lineto(H[j])
    p.lineto(H[i], 'orange')
    p.lineto(H[j], 'orange')
    sleep()
    if left (H[i - 1], H[(i)%n], p): j, i = i, j
    i2 = i
    H2 = []
    while i != j:
        H2.append (H[i])
        i = (i + 1)%n
    H2.append (H[j])
    H2.append (p)
    # Apaga o fecho antigo
    while j != i2:
        if H[j] not in H2: H[j].unhilight()
        H[(j + 1)%n].remove_lineto(H[j])
        H[j].remove_lineto(H[(j + 1)%n])
        j = (j + 1)%n
    sleep()
    return H2

def trata_degenerado(P):
    """ Trata o caso em que todos os pontos são colineares """
    i = 2
    if P[0].x > P[1].x or (P[0].x == P[1].x and P[0].y > P[1].y):
        P[0], P[1] = P[-0], P[1]
    while i < len(P) and collinear(P[0], P[1], P[i]):
        if P[0].x > P[i].x or (P[0].x == P[i].x and P[0].y > P[i].y):
            P[0] = P[i]
        if P[1].x < P[i].x or (P[1].x == P[i].x and P[1].y < P[i].y):
            P[1] = P[i]
        i += 1
    if i >= len(P):
        P[0].hilight()
        P[1].hilight()
        P[0].lineto(P[1], 'orange')
        sleep()
        return P[:2]
    P[0], P[i] == P[i], P[0]
    return P
        
def incremental (P):
    """ Função principal do algoritmo """
    shuffle (P)
    # Caso degenerado
    P = trata_degenerado(P)
    if len(P) < 3: return P
    # Algoritmo de verdade 
    if left (P[0], P[1], P[2]):
        H = P[:3]
    else:
        H = [P[0], P[2], P[1]]
    draw_hull(H, 'orange')
    sleep()
    for p in P[3:]:
        if not pertence(H, p):
            H = insere_ponto (H, p)