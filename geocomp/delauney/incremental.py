# -*- coding: utf-8 -*-
from geocomp.common.point import Point
from geocomp.common.segment import Segment
from geocomp.common.prim import left
from geocomp.common.dcel import Dcel
from geocomp.common.control import sleep

class Node_Triang:
    " Classe que será o nó do DAG, guarda os triângulos que fazem parte da triangulação "
    def __init__ (self, p1, p2, p3):
        if left (p1, p2, p3):
            self.p1 = p1
            self.p2 = p2
        else:
            self.p1 = p2
            self.p2 = p1
        self.p3 = p3

        # Node_Triangs que são filhos do self no DAG
        self.filhos = []
        # arestas
        self.a1 = Segment (self.p1, self.p2)
        self.a2 = Segment (self.p2, self.p3)
        self.a3 = Segment (self.p3, self.p1)

    def busca (self, ponto):
        " Retorna o nó folha em que o ponto está "
        for f in self.filhos:
            if (left (f.p1, f.p2, ponto) and 
                left (f.p2, f.p3, ponto) and
                left (f.p3, f.p1, ponto)):
                return f.busca (ponto)
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

def add_triangs_dcel (d, p, triang):
    " Adiciona os três triangulos formados por p e as arestas do triang na dcel d"
    " E retorna as 3 meia arestas de p para os vértices do triang"
    d.add_vertex (p)
    e1 = d.add_edge (p, triang.p1)
    e2 = d.add_edge (p, triang.p2)
    e3 = d.add_edge (p, triang.p3)
    e1.draw()
    e2.draw()
    e3.draw()
    return e1, e2, e3

def ilegal (e):
    " Devolve se a aresta dada pela meia aresta 'e' é ilegal "
    # O quadrilatero precisa ser convexo
    seg1 = Segment (e.init, e.to)
    seg2 = Segment (e.prox.to, e.twin.prox.to)
    if not seg1.intersects (seg2): return False

    # Precisamos achar o menor angulo de um triangulo
    def angulo (p1, p2, p3):
        # Devolve o angulo em p2 do triangulo p1-p2-p3
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
    min_ang1 = min ([angulo (e.prev.init, e.init, e.to),
                     angulo (e.init, e.to, e.prev.init),
                     angulo (e.to, e.prev.init, e.init)])
    # Acha o menor angulo do triangulo com a aresta e.twin
    min_ang2 = min ([angulo (e.twin.prev.init, e.init, e.to),
                     angulo (e.init, e.to, e.twin.prev.init),
                     angulo (e.init, e.twin.prev.init, e.to)])
    min_ang_legal = min(min_ang1, min_ang2)

    # Acha o menor angulo dos triangulos com a outra diagonal
    min_ang1 = min ([angulo (e.prev.init, e.init, e.twin.prev.init),
                     angulo (e.init, e.prev.init, e.twin.prev.init),
                     angulo (e.prev.init, e.twin.prev.init, e.init)])
    min_ang2 = min ([angulo (e.prev.init, e.to, e.twin.prev.init),
                     angulo (e.to, e.prev.init, e.twin.prev.init),
                     angulo (e.prev.init, e.twin.prev.init, e.to)])
    min_ang_ilegal = min(min_ang1, min_ang2)
    return min_ang_legal < min_ang_ilegal


def Incremental (pontos):
    d = Dcel()
    if len(pontos) <= 3: return []
        
    inf1, inf2, inf3 = pontos_infinitos (pontos)
    
    # Cria o triangulo auxiliar que contém toda a coleção
    raiz = Node_Triang (inf1, inf2, inf3)
    d.add_vertex (inf1)
    d.add_vertex (inf2)
    d.add_vertex (inf3)
    e1 = d.add_edge (inf1, inf2)
    e2 = d.add_edge (inf2, inf3)
    e3 = d.add_edge (inf3, inf1)
    e1.draw ("gray")
    e2.draw ("gray")
    e3.draw ("gray")
    # Toda vez que criarmos uma face vamos ter que associar a folha do dag a essa face
    d.extra_info[e1.f] = raiz

    # Processamento principal
    for p in pontos:
        triang = raiz.busca (p)
        p.hilight()
        sleep()
        # Adiciona as três arestas na dcel
        e1, e2, e3 = add_triangs_dcel (d, p, triang)
        sleep()
        # Adiciona as novas faces/triangulos no dag e dcel
        novos_triangs = [(Node_Triang (triang.p1, triang.p2, p), e2),
                         (Node_Triang (triang.p2, triang.p3, p), e3),
                         (Node_Triang (triang.p3, triang.p1, p), e1)]
        for t in novos_triangs:
            triang.filhos.append (t[0])
            d.extra_info[t[1].f] = t[0]

        # Legaliza arestas
        # Vamos fazer uma fila de meia-arestas que precisam ser verificadas
        verificadas = [e1.prox, e2.prox, e3.prox]
        # Quem está nessa fila de aresta vou pintar de amarelo
        e1.prox.hide()
        e2.prox.hide()
        e3.prox.hide()
        e1.prox.draw("yellow green")
        e2.prox.draw("yellow green")
        e3.prox.draw("yellow green")
        sleep()

        while len (verificadas) > 0:
            e = verificadas.pop()

            e.hide()
            e.draw("yellow")
            sleep()
            e.hide()

            if not ilegal (e):
                e.draw()  
            else:
                e.draw("red")
                sleep()
                e.hide()
                # Guarda os triangulos que serão removidos do dag
                pai1 = d.extra_info[e.f]
                pai2 = d.extra_info[e.twin.f]
                # Revome a diagonal ilegal e adiciona a legal
                d.remove_edge (e)
                e_nova = d.add_edge (e.prox.to, e.twin.prox.to, e.prox.f)
                e_nova.draw()
                # Adiciona os novos triangulos no dag
                t1 = Node_Triang (e.to, e.prox.to, e.twin.prox.to)
                t2 = Node_Triang (e.init, e.prox.to, e.twin.prox.to)
                pai1.filhos = pai2.filhos = [t1, t2]
                # referencia as novas folhas para suas faces na dcel
                d.extra_info[e_nova.f] = t1
                d.extra_info[e_nova.twin.f] = t2

        p.unhilight()