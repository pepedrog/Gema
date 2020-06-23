#!/usr/bin/env python

from geocomp.common.guiprim import *

from geocomp.common.segment import Segment
import desenhos

class Polygon:
    """Um Poligono. Implementado como uma lista ligada de pontos"""
    def __init__ (self, pontos):
        "Para criar o poligono, passe uma lista (de python) de pontos"
        self.cid = {}
        self.hid = {}
        self.hidp = {}

        p = self.pts = pontos[0]

        for i in range(1, len(pontos)):
            p.next = pontos[i]
            pontos[i].prev = p
            p = p.next
        p.next = self.pts
        self.pts.prev = p

    def __repr__ (self):
        "Retorna uma string da forma [ ( x0 y0 ) ( x1 y1 ) ... ]"
        ret = '[ '
        p = self.pts
        while p.next != self.pts:
            ret = ret + repr(p) + ' '
            p = p.next
        ret = ret + repr(p)
        ret = ret + ' ]'
        return ret

    def plot (self, cor = desenhos.cor_segmento, grossura = desenhos.grossura_segmento):
        "Desenha o poligono na tela"
        p = self.pts
        while p.next != self.pts:
            self.cid[p] = p.lineto (p.next, cor, grossura)
            p = p.next
        self.cid[p] = p.lineto (p.next, cor, grossura)

    def hide (self):
        "Apaga o poligono na tela"
        p = self.pts
        while p.next != self.pts:
            if p in self.cid:
                desenhos.plot_delete (self.cid[p])
                del (self.cid[p])
            p = p.next

        if p in self.cid:
            desenhos.plot_delete (self.cid[p])
            del (self.cid[p])

    def to_list (self):
        """      
        Retorna uma lista (de python) com todos os pontos 
        
        Mantido só por questões de compatibilidade. Prefira usar
        vertices()
        
        """
        return self.vertices()
        
    def vertices(self):
        vertices = []
        p = self.pts
        while p.next != self.pts:
            vertices.append(p)
            p = p.next
        vertices.append(p)
        return vertices
    
    # Retorna lista de arestas, cada uma um Segment
    def edges(self):
        edges = []
        p = self.pts
        while p.next != self.pts:
            edges.append(Segment(p, p.next))
            p = p.next
        edges.append(Segment(p, p.next))
        return edges
    
    # Retorna o par (p, n) que vem antes e depois de v no polígono
    def adj(self, v):
        vertices = self.vertices()
        for i in range(len(vertices)):
            if vertices[i] == v:
                if i == 0:
                    return vertices[-1], vertices[1]
                if i == len(vertices) - 1:
                    return vertices[i - 1], vertices[0]
                return vertices[i - 1], vertices[i + 1]
        return None

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        edges1 = self.edges()
        edges2 = other.edges()
        for e in edges1:
            if e not in edges2:
                return False
        for e in edges2:
            if e not in edges1:
                return False
        return True
