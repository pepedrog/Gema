#!/usr/bin/env python
""" Algoritmo de Linha de Varredura """

from geocomp.common.segment import Segment
from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.common.abbb import Abbb

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
        return str(self.p)
def Varre (l):
    "Algoritmo de divisão e conquista para encontrar o par de pontos mais proximo"
    "Recebe uma lista de pontos l"         

    if len (l) < 2: return None
    
    d = float("inf")
    
    l = sorted(l, key = lambda x:x.x)
    
    par_min = None
    faixa = Abbb ()
    
    p_min = 0
    
    for i in range (len(l)):
        p = l[i]
        no_p = Node_point (p)
        faixa.insere (no_p)
        p.hilight ()
        faixa.printa_arvore()
        # Remove os pontos fora da faixa
        while p.x - l[p_min].x > d:
            
            l[p_min].unhilight()
            # Se o ponto está no par_min, pinto de vermelho denovo
            if par_min != None and l[p_min] in par_min.endpoints():
                l[p_min].hilight ("red")
            no_p = Node_point (l[p_min])
            faixa.deleta (no_p)
            p_min += 1

        # Desenha o quadradinho de candidatos
        linha_frente = control.plot_vert_line (p.x)
        if i > 1:
            linha_tras = control.plot_vert_line (p.x - d, color = "blue")
            linha_cima  = Segment (Point (p.x, p.y + d), Point (p.x - d, p.y + d))
            linha_baixo = Segment (Point (p.x, p.y - d), Point (p.x - d, p.y - d))
            linha_cima.plot ("blue")
            linha_baixo.plot ("blue")
        control.sleep()
        
        # Extrai os pontos da abbb até a distancia vertical ficar maior que d
        # Primeiro com os vizinhos de cima
        vizinho = faixa.sucessor (no_p)
        while vizinho != None and vizinho.p.y - p.y < d:
            d2 = dist2 (p, vizinho.p)
            if d2 < d*d:
                d = d2**0.5
                
                # Despinta os pontos e o par anterior e pinta o novo par
                vizinho.p.unhilight()
                vizinho.p.hilight("red")
                p.unhilight()
                p.hilight( "red")
                if par_min != None:
                    par_min.hide ()
                par_min = Segment (p, vizinho.p)
                par_min.plot ("red")
                control.sleep()
                
            vizinho = faixa.sucessor (vizinho)
        # Depois com os vizinhos de baixo
        vizinho = faixa.predecessor (no_p)
        while vizinho != None and p.y - vizinho.p.y < d:
            d2 = dist2 (p, vizinho.p)
            if d2 < d*d:
                d = d2**0.5
                
                if par_min != None:
                    par_min.hide()
                par_min = Segment (p, vizinho.p)
                par_min.hilight ("red", "red")
                control.sleep()
                
            vizinho = faixa.predecessor (vizinho)
            
        # Apaga o quadradinho
        control.plot_delete (linha_frente)
        if (i > 1):
            control.plot_delete (linha_tras)
            linha_cima.hide ()
            linha_baixo.hide ()
            
        p.unhilight()
        p.hilight ("blue")
        
        
    l[-1].unhilight()