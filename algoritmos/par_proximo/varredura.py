#!/usr/bin/env python
""" Algoritmo de Linha de Varredura """

from estruturas.segment import Segment
from estruturas.point import Point
import desenhos
from estruturas.prim import *
from estruturas.abbb import Abbb

class Node_point ():
    " nó que guardará os pontos na árvore "
    def __init__ (self, p):
        self.p = p
    def __eq__ (self, p2):
        return p2 != None and self.p == p2.p
    def __gt__ (self, p2):
        if p2 == None: return False
        if self.p.y > p2.p.y:
            return True
        if self.p.y < p2.p.y:
            return False
        if self.p.x > p2.p.x:
            return True
        return False
    def __str__ (self):
        return str (self.p)
    
def varre (l):
    "Algoritmo de divisão e conquista para encontrar o par de pontos mais proximo"
    "Recebe uma lista de pontos l"         

    if len (l) < 2: return None
    
    d = float ('inf')
    
    l = sorted (l, key = lambda x:x.x)
    
    par_min = None
    faixa = Abbb ()
    
    p_min = 0
    
    for i in range (len(l)):
        p = l[i]
        no_p = Node_point (p)
        
        # Caso degenerado -> pontos coincidentes
        # (não conseguimos adicionar na abbb, pois ja tem um clone dele)
        repetido = faixa.busca (no_p).elemento
        if repetido != None:
            if par_min != None:
                par_min.hide()
            par_min = Segment(p, repetido.p)
            break
        
        faixa.insere (no_p)
        p.hilight ()
        
        # Remove os pontos fora da faixa
        while p.x - l[p_min].x > d:
            l[p_min].unhilight()
            if l[p_min] in par_min.endpoints():
                l[p_min].hilight('orange')
            no_p_min = Node_point (l[p_min])
            faixa.deleta (no_p_min)
            p_min += 1
            

        # Desenha o quadradinho de candidatos
        linha_frente = desenhos.plot_vert_line (p.x, 'orange')
        if i > 1:
            linha_tras = desenhos.plot_vert_line (p.x - d, cor = 'firebrick')
            linha_cima  = Segment (Point (p.x, p.y + d), Point (p.x - d, p.y + d))
            linha_baixo = Segment (Point (p.x, p.y - d), Point (p.x - d, p.y - d))
            linha_cima.plot ('firebrick')
            linha_baixo.plot ('firebrick')
        desenhos.sleep()
        
        # Extrai os pontos da abbb até a distancia vertical ficar maior que d
        # Primeiro com os vizinhos de cima
        vizinho = faixa.sucessor (no_p)
        while vizinho != None and vizinho.p.y - p.y < d: 
            d2 = dist2 (p, vizinho.p)
            p.hilight ()
            vizinho.p.hilight ('firebrick')
            if d2 < d*d:
                d = d2**0.5
                
                if par_min is not None:
                    par_min.unhilight ()
                par_min = Segment (p, vizinho.p)
                par_min.hilight ('orange')
                desenhos.sleep()
                
            vizinho = faixa.sucessor (vizinho)
        # Depois com os vizinhos de baixo
        vizinho = faixa.predecessor (no_p)
        while vizinho is not None and p.y - vizinho.p.y < d:
            d2 = dist2 (p, vizinho.p)
            p.hilight()
            vizinho.p.hilight ('firebrick')
            if d2 < d*d:
                d = d2**0.5
                
                if par_min is not None:
                    par_min.unhilight()
                par_min = Segment (p, vizinho.p)
                par_min.hilight ('orange')
                desenhos.sleep()
                
            vizinho = faixa.predecessor (vizinho)
            
        # Apaga o quadradinho
        desenhos.plot_delete (linha_frente)
        if (i > 1):
            desenhos.plot_delete (linha_tras)
            linha_cima.hide ()
            linha_baixo.hide ()
            
        p.unhilight()
        l[i].hilight ('firebrick')
    
    "despinta quem sobrou na faixa"
    while (not faixa.vazia()):
        faixa.deleta_min().p.unhilight()
    par_min.hilight ('orange')
    