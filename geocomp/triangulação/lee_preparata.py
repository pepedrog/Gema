#!/usr/bin/env python
"""
Algoritmo de Remoção de Orelhas para Triangulação de Polígonos
Pedro Gigeck Freire - nUSP 10737136
"""

from geocomp.common.segment import Segment
from geocomp.common.prim import right
from geocomp.common import control
from .monotono import Monotono
    
def monotonos (P):
    """ Função que recebe um polígono P e particiona P em vários polígonos monótonos
        Através da inserção de diagonais
        Retorna a lista de polígonos monótonos e a lista de diagonais adicionadas
    """
    # Ordena os vértices pela Y-coordenada
    v = P.vertices()
    v = sorted(v, key = lambda x:(-x.y))
    
    # os vértices são os pontos eventos da linha de varredura
    for p in v:
        p.hilight()
        control.plot_horiz_line (p.y)
        control.sleep()
        
        viz_cima = p.next
        viz_baixo = p.prev
        if viz_cima.y < viz_baixo.y:
            viz_cima, viz_baixo = viz_baixo, viz_cima
        
        if viz_cima.y > p.y and p.y > viz_baixo.y:
            trata_caso_meio()
        elif viz_baixo.y > p.y:
            trata_ponta_pra_baixo()
        else:
            trata_ponta_pra_cima()
        
        
    
    control.sleep()
        
    

def triangula (P, d):
    """ Função que recebe um polígono monótono P e triangula P, adicionando diagonais
        Concatena as diagonais adicionadas em d
    """
    # Quem faz o trabalho na verdade é a função implementada para o algoritmo
    # de triangulação de polígonos monótonos
    for diag in Monotono ([P]):
        d.append (diag)

def Lee_Preparata (p):
    # Essa é a forma que eu recebo o polígono do front-end :/
    P = p[0]
    
    m, diagonais = monotonos (P)
    for pm in m:
        triangula (pm, diagonais)
    
    return diagonais