# -*- coding: utf-8 -*-
from geocomp.common.point import Point
from geocomp.common.segment import Segment
from geocomp.common.prim import left, left_on
from geocomp.common.control import sleep
from random import shuffle

desenha_busca = False

color_triang = "orange"
color_novo = "firebrick"
color_legalizaveis = "green"
color_ilegal = "red"

# Os tres pontos no infinito
global infs

class Node_Triang:
    " Classe que será o nó do DAG, guarda os triângulos que fazem parte da triangulação "
    def __init__ (self, p1, p2, p3, viz12 = None, viz23 = None, viz31 = None):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.viz1 = viz12 # Node_triang vizinho da aresta p1-p2
        self.viz2 = viz23 # vizinho da p2-p3
        self.viz3 = viz31 # vizinho da p3-p1
        # Node_Triangs que são filhos do self no DAG
        self.filhos = []
        # arestas
        self.a1 = Segment (self.p1, self.p2)
        self.a2 = Segment (self.p2, self.p3)
        self.a3 = Segment (self.p3, self.p1)
    
    def draw (self, color):
        self.a1.plot(color)
        self.a2.plot(color)
        self.a3.plot(color)
        sleep()
    
    def hide (self):
        self.a1.hide()
        self.a2.hide()
        self.a3.hide()
        
    def busca (self, ponto):
        " Retorna o nó folha em que o ponto está "
        if desenha_busca: self.draw("gray")
        for f in self.filhos:
            if (left_on (f.p1, f.p2, ponto) and 
                left_on (f.p2, f.p3, ponto) and
                left_on (f.p3, f.p1, ponto)):
                if desenha_busca: self.hide()
                return f.busca (ponto)
        if desenha_busca: 
            self.hide()
            self.draw(color_triang)
        return self 

def pontos_infinitos (p):
    " Devolve três pontos fictícios tais que o triangulo formado por eles "
    " contém todos os pontos de p "
    
    # Vou montar um quadradão que contém todos os pontos
    cima = baixo = direito = esquerdo = p[0]
    for i in range(1, len(p)):
        if p[i].y > cima.y: cima = p[i]
        if p[i].y < baixo.y: baixo = p[i]
        if p[i].x < esquerdo.x: esquerdo = p[i]
        if p[i].x > direito.x: direito = p[i]
        
    # Agora monto um triângulão que contém esse quadrado
    p1 = Point (esquerdo.x - 10*(direito.x - esquerdo.x), baixo.y - 10*(cima.y - baixo.y))
    p2 = Point (esquerdo.x + (direito.x - esquerdo.x)/2, cima.y + 10*(cima.y - baixo.y))
    p3 = Point (esquerdo.x + 10*(direito.x - esquerdo.x), baixo.y - 10*(cima.y - baixo.y))
    return p1, p2, p3

def vertice_oposto (t):
    " Devolve o vértice de t.viz1 que é não está em t, junto dos outros 2 numa lista "
    oposto = t.viz1.p1
    adj1 = t.viz1.p2
    adj2 = t.viz1.p3
    if oposto in t.a1.endpoints():
        oposto = t.viz1.p2
        adj1 = t.viz1.p1
        adj2 = t.viz1.p3
    if oposto in t.a1.endpoints():
        oposto = t.viz1.p3
        adj1 = t.viz1.p2
        adj2 = t.viz1.p1
    return oposto, adj1, adj2

def ilegal (t):
    " Devolve se a aresta dada pela meia aresta 'e' é ilegal "
    # As arestas do triangulão infinito não podem ser ilegais
    global infs
    if t.a1.init in infs and t.a1.to in infs:
        return False
    
    t.a1.hide()
    t.a1.plot(color_legalizaveis)
    sleep()
    # O quadrilatero precisa ser convexo
    seg1 = Segment (t.a1.init, t.a1.to)
    seg2 = Segment (t.a1.prox.to, t.a1.twin.prox.to)
    if not seg1.intersects (seg2): return False

    def angulo (p1, p2, p3):
        " Devolve algo proporcional ao angulo em p2 de p1-p2-p3 "
        # Na verdade, devolve o -2*cosseno do angulo com a lei do cosseno
        a2 = (p3.x - p1.x)**2 + (p3.y - p1.y)**2
        b2 = (p3.x - p2.x)**2 + (p3.y - p2.y)**2
        c2 = (p1.x - p2.x)**2 + (p1.y - p2.y)**2
        ang = ((b2 + c2 - a2)/(2*((b2*c2)**0.5)))
        return -ang
        # Como cosseno é descrescente para angulos menores que pi,
        # Então posso comparar dois angulos a e b pelos seus cossenos
        # a > b <=> cos(a) < cos(b)
    
    # Acha o menor angulo do triangulo com a aresta e
    min_ang1 = min ([angulo (t.p1, t.p2, t.p3),
                     angulo (t.p2, t.p3, t.p1),
                     angulo (t.p3, t.p1, t.p2)])
    # Acha o menor angulo do triangulo com a aresta e.twin
    min_ang2 = min ([angulo (t.viz1.p1, t.viz1.p2, t.viz1.p3),
                     angulo (t.viz1.p2, t.viz1.p3, t.viz1.p1),
                     angulo (t.viz1.p3, t.viz1.p1, t.viz1.p2)])
    min_ang_legal = min(min_ang1, min_ang2)

    # Acha o menor angulo dos triangulos com a outra diagonal
    oposto, adj1, adj2 = vertice_oposto (t)
    min_ang1 = min ([angulo (oposto, adj1, t.p3),
                     angulo (oposto, t.p3, adj1),
                     angulo (adj1, oposto, t.p3)])
    min_ang2 = min ([angulo (oposto, adj2, t.p3),
                     angulo (oposto, t.p3, adj2),
                     angulo (adj2, oposto, t.p3)])
    min_ang_ilegal = min(min_ang1, min_ang2)
    t.a1.hide()
    return min_ang_legal < min_ang_ilegal


def Incremental (pontos):
    " Função principal: Recebe uma coleção de pontos e retorna uma DCEL da triangulão "
    " de Delauney desses pontos, desenhando os passos do algoritmo na tela "
    if len(pontos) < 3: return []
    
    global infs
    global desenha_busca
    shuffle (pontos)
    
    inf1, inf2, inf3 = pontos_infinitos (pontos)
    infs = [inf1, inf2, inf3]
    
    # Cria o triangulo auxiliar grandão que contém toda a coleção
    raiz = Node_Triang (inf1, inf2, inf3)
    
    # Processamento principal
    for p in pontos:
        p.hilight(color_novo)
        triang = raiz.busca (p)
        sleep()
        
        # Adiciona as novas faces/triangulos no dag
        t1 = Node_Triang (triang.p1, triang.p2, p, triang.viz1)
        t2 = Node_Triang (triang.p2, triang.p3, p, triang.viz3, viz31 = t1)
        t3 = Node_Triang (triang.p3, triang.p1, p, triang.viz2, t1, t2)
        t1.viz2 = t2
        t1.viz3 = t3
        t2.viz2 = t3

        # triangulos que precisam ser legalizados 
        # Vamos convencionar que a aresta que precisa ser conferida é a a1
        legalizaveis = [t1, t2, t3]

        while len (legalizaveis) > 0:
            t = legalizaveis.pop()
            
            if not ilegal (t):
                t.a1.plot (color_triang)  
            else:
                t.a1.plot (color_ilegal)
                sleep()
                t.hide()
                
                # Só precisa tomar cuidado com a organização dos pontos no vizinho
                
                # Adiciona os novos triangulos no dag
                nova_ponta, adj1, adj2 = vertice_oposto (t)
                t1 = Node_Triang (nova_ponta, adj1, p)
                t2 = Node_Triang (nova_ponta, adj2, p)
                t.filhos = t.viz1.filhos = [t1, t2]
                legalizaveis.extend (t1, t2)
                t1.draw(color_triang)
                t2.draw(color_triang)
                sleep()
        p.unhilight()
    """
    # Depois de processar todos os pontos, removo os pontos do infinito
    for i in infs:
        rem = d.v[i].twin.prox
        while rem != d.v[i]:
            d.remove_edge(rem)
            rem = rem.twin.prox
        d.remove_edge(rem)
        d.v.pop(i)
        sleep()
    # Por algum motivo quando eu retorno a DCEL buga a tela :(
    return [d]
        """