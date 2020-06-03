# -*- coding: utf-8 -*-
from geocomp.common.point import Point
from geocomp.common.segment import Segment

class Node_Triang:
    " Classe que será o nó do DAG, guarda os triângulos que fazem parte da triangulação "
    def __init__ (self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        
        self.filhos = []
        # Node_Triangs que são filhos do self no DAG
    
    def draw (self):
        " Desenha o triângulo do nó "
        # arestas
        self.a1 = Segment (self.p1, self.p2)
        self.a2 = Segment (self.p2, self.p3)
        self.a3 = Segment (self.p3, self.p1)
        
        self.a1.plot("orange")
        self.a2.plot("orange")
        self.a3.plot("orange")
    
    def hide (self):
        " Apaga o desenho do triângulo"
        self.a1.hide()
        self.a2.hide()
        self.a3.hide()
    
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
        
    cima.hilight()
    baixo.hilight()
    esquerdo.hilight()
    direito.hilight()
        
    # Dou uma alargada no quadrado pros pontos não cairem na borda
    cima.y += 20
    baixo.y -= 20
    esquerdo.x -= 20
    direito.x += 20
    
    # Agora monto um triângulo retângulo que contém esse quadrado
    p1 = Point (esquerdo.x, baixo.y)
    p2 = Point (esquerdo.x, baixo.y + 2*(cima.y - baixo.y))
    p3 = Point (esquerdo.x + 2*(direito.x - esquerdo.x), baixo.y)
    
    return p1, p2, p3

def Incremental(p):
    
    if len(p) <= 3:
        Node_Triang(p[0], p[1], p[2]).draw()
        
    inf1, inf2, inf3 = pontos_infinitos (p)
    
    raiz = Node_Triang (inf1, inf2, inf3)
    raiz.draw()
    