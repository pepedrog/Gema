#!/usr/bin/env python
"""
Algoritmo de Remoção de Orelhas para Triangulação de Polígonos
Pedro Gigeck Freire - nUSP 10737136
"""

from geocomp.common.segment import Segment
from geocomp.common.abbb import Abbb
from geocomp.common.prim import left, right_on, left_on
from geocomp.common import control
from .monotono import Monotono
    
# todo: fazer a dcel
# Debugar a inserção na abbb

class Trapezio:
    # Recebe o vértice de superte v e as duas arestas da esquerda e direita
    def __init__ (self, sup, e = None, d = None):
        self.sup = sup
        if e != None and d != None:
            if e.init.y < e.to.y:
                e.init, e.to = e.to, e.init
            if d.init.y < d.to.y:
                d.init, d.to = d.to, d.init
            self.a_esq = e
            self.a_dir = d
    
    def __eq__ (self, other):
        return (other != None and other.sup.y <= self.sup.y and
                right_on (self.a_esq.init, self.a_esq.to, other.sup) and
                left_on (self.a_dir.init, self.a_dir.to, other.sup))
    
    def __gt__ (self, other):
        return left (self.a_esq.init, self.a_dir.to, other.sup)
        
def ponta_pra_baixo (p):
    return p.next.y > p.y and p.prev.y > p.y

def trata_caso_meio (p, viz_baixo, L, diags):
    # Remove da linha o trapésio que tem o p
    t = Trapezio (p)
    removido = (L.busca (t)).elemento
    L.deleta (t)
    
    # Insere um novo trapésio com o p
    # Se o removido estava a direita
    if (p == removido.a_esq.to):
        t.a_dir = Segment (p, viz_baixo)
        t.a_esq = removido.a_esq        
    # Se estava a esquerda
    else:
        t.a_esq = Segment (p, viz_baixo)
        t.a_dir = removido.a_dir
    L.insere (t)
    
    if ponta_pra_baixo (removido.sup):
        d = Segment (removido.sup, p)
        d.plot()
        control.sleep()
        diags.append (d)
    
def trata_ponta_pra_cima (p, L, diags):
    viz_esq = p.next
    viz_dir = p.prev
    if viz_esq.x > viz_dir.x:
        viz_esq, viz_dir = viz_dir, viz_esq
    
    t = Trapezio (p)
    removido = (L.busca (t)).elemento
    L.deleta (t)
    
    if removido == None:
        t.a_esq = Segment (p, viz_esq)
        t.a_dir = Segment (p, viz_dir)
        L.insere (t)
    
    else:
        t1 = Trapezio (p, removido.a_esq, Segment (p. viz_dir))
        t2 = Trapezio (p, Segment (p, viz_esq), removido.a_dir)
        L.insere (t1)
        L.insere (t2)
        
        d = Segment (p, removido.sup)
        d.plot()
        control.sleep()
        diags.append (d)
    
def trata_ponta_pra_baixo (p, L, diags):
    t = Trapezio (p)
    removido1 = (L.busca (t)).elemento
    L.deleta (t)
    
    if ponta_pra_baixo (removido1.sup):
        d = Segment (removido1.sup, p)
        d.plot()
        control.sleep()
        diags.append (d)
    
    # Se tem outro polígono
    removido2 = (L.busca (t)).elemento
    if removido2 != None:
        L.deleta (t)
        
        if ponta_pra_baixo (removido2.sup):
            d = Segment (removido2.sup, p)
            d.plot()
            control.sleep()
            diags.append (d)
        
        if removido2.a_esq.to == p:
            L.insere (p, removido1.a_esq, removido2.a_dir)
        else:
            L.insere (p, removido2.a_esq, removido1.a_dir)

def monotonos (P):
    """ Função que recebe um polígono P e particiona P em vários polígonos monótonos
        Através da inserção de diagonais
        Retorna a lista de polígonos monótonos e a lista de diagonais adicionadas
    """
    # Ordena os vértices pela Y-coordenada
    v = P.vertices()
    v = sorted(v, key = lambda x:(-x.y))
    
    diags = [] # lista de diagonais que acrescentamos
    L = Abbb()
    
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
            trata_caso_meio (p, viz_baixo, L, diags)
        elif viz_cima.y < p.y:
            trata_ponta_pra_cima (p, L, diags)
        else:
            trata_ponta_pra_baixo (viz_cima, p, viz_baixo, L, diags) 
    
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