# -*- coding: utf-8 -*-
from estruturas.point import Point
from estruturas.segment import Segment
from estruturas.prim import left, left_on
from estruturas.dcel import Dcel
import desenhos
desenha_busca = False

color_triang = "orange"
color_legalizaveis = "green"

# Os tres pontos no infinito
global infs

from math import *
import random
RADIUS = 240

my_delay = (10, 50, 5)
pula = False

def pula_gema():
    global pula
    pula = True
    
def sleep():
    global pula
    if not pula:
        desenhos.sleep()

def uniform_circ (num_pts, radius):
    l = []
    for i in range (num_pts):
        theta = (2*pi*i)/num_pts

        x = float (radius * cos (theta))
        y = float (radius * sin (theta))

        l.append ( (x, y) )

    return l

def randdisc (num_pts, radius):
    if radius < 0: radius = -radius
    if radius == 0: radius = 10000
    l = []
    for i in range (0, num_pts):
        r2 = random.uniform (0, radius*radius)
        r = sqrt (r2)
        theta = random.uniform (0, 2 * pi)

        x = float (r * cos (theta))
        y = float (r * sin (theta))

        l.append ( (x,y) )

    return l

def grid (linhas, colunas):
    l = []
    for i in range(3, linhas - 3):
        for j in [5, 6, colunas - 1, colunas - 2]:
            l.append ([(i+1)* 600/(linhas+1), (j+1) * 600/(colunas+1)])
    for i in [2, 3, linhas - 4, linhas - 3]:
        for j in range(7, colunas - 2):
            l.append ([(i+1)* 600/(linhas+1), (j+1) * 600/(colunas+1)])
    return l

def main ():
    novo = []
    clara = []
    for i in randdisc(150, 60):
        novo.append(Point(i[0] + 300, i[1] + 392))
    for i in uniform_circ(25, 90):
        novo.append(Point(i[0] + 300, i[1] + 392))
    for i in uniform_circ(50, 110):
        novo.append(Point(i[0] + 300, i[1] + 392))
    for i in grid(15, 15):
        novo.append(Point(i[0], i[1]))
        clara.append(Point(i[0], i[1]))
        
    f = open('input/pontos/gema', "w")
    for p in novo:
        f.write ('%f %f\n' % (p.x, p.y - 92))
    f.close()
    return clara, novo
    # Poligono
    
main()

class Node_Triang:
    " Classe que será o nó do DAG, guarda os triângulos que fazem parte da triangulação "
    def __init__ (self, p1, p2, p3, a):
        if left (p1, p2, p3):
            self.p1 = p1
            self.p2 = p2
        else:
            self.p1 = p2
            self.p2 = p1
        self.p3 = p3
        self.a = a # Alguma aresta da DCEL que faz parte desse triangulo
        self.filhos = [] # Node_Triangs que são filhos do self no DAG
        # arestas
        self.a1 = Segment (self.p1, self.p2)
        self.a2 = Segment (self.p2, self.p3)
        self.a3 = Segment (self.p3, self.p1)
        
    def busca (self, ponto):
        " Retorna o nó folha em que o ponto está "
        for f in self.filhos:
            if (left_on (f.p1, f.p2, ponto) and 
                left_on (f.p2, f.p3, ponto) and
                left_on (f.p3, f.p1, ponto)):
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
    " Adiciona o P na dcel d e uma aresta de p pra cada ponta do triang "
    d.add_vertex (p)
    e1 = d.add_edge (p, triang.p1, triang.a.f)
    e2 = d.add_edge (p, triang.p2, triang.a.f)
    e3 = d.add_edge (p, triang.p3, e2.f)
    return e1, e2, e3

def ilegal (e):
    " Devolve se a aresta dada pela meia aresta 'e' é ilegal "
    # As arestas do triangulão infinito não podem ser ilegais
    global infs
    if e.init in infs and e.to in infs:
        return False
    
    # O quadrilatero precisa ser convexo
    if left (e.twin.prox.to, e.to, e.prox.to) == left (e.twin.prox.to, e.init, e.prox.to):
        return False

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

def escreve_gema():
    g = [Point (210, 190), Point (140, 190), Point (140, 110), Point (210, 110),
         Point (210, 150), Point (190, 150)]
    for i in range(len(g)):
        g[i].hilight()
        if (i > 0):
            g[i].lineto(g[i - 1], 'orange')
        sleep()
    e = [Point (290, 110), Point (230, 110), Point (230, 150), Point (290, 150), 
         Point (230, 150), Point (230, 180), Point (290, 180)]
    for i in range(len(e)):
        e[i].hilight()
        if (i > 0):
            e[i].lineto(e[i - 1], 'orange')
        sleep()
        
    m = [Point (310, 110), Point (310, 180), Point (340, 150), Point (370, 180), Point(370, 110)]
    for i in range(len(m)):
        m[i].hilight()
        if (i > 0):
            m[i].lineto(m[i - 1], 'orange')
        sleep()
        
    a = [Point (390, 110), Point (405, 150), Point (445, 150), Point (405, 150), 
         Point (420, 190), Point (430, 190), Point (460, 110)]
    for i in range(len(a)):
        a[i].hilight()
        if (i > 0):
            a[i].lineto(a[i - 1], 'orange')
        sleep()

def escreve_geometric():
    g = [Point (130, 70), Point (110, 70), Point (110, 50), Point (130, 50),
         Point (130, 60), Point (120, 60)]
    for i in range(1, len(g)):
        g[i].lineto(g[i - 1], 'orange')
        sleep()
    e = [Point (151, 50), Point (135, 50), Point (135, 58), Point (151, 58), 
         Point (135, 58), Point (135, 66), Point (151, 66)]
    for i in range(1, len(e)):
        e[i].lineto(e[i - 1], 'orange')
        sleep()
    o = [Point (156, 50), Point (156, 66), Point (172, 66), Point (172, 50)]
    for i in range(len(o)):
        o[i].lineto(o[i - 1], 'orange')
        sleep()
    m = [Point (177, 50), Point (177, 66), Point (185, 58), Point (193, 66), Point(193, 50)]
    for i in range(1, len(m)):
        m[i].lineto(m[i - 1], 'orange')
        sleep()
    e = [Point (214, 50), Point (198, 50), Point (198, 58), Point (214, 58), 
         Point (198, 58), Point (198, 66), Point (214, 66)]
    for i in range(1, len(e)):
        e[i].lineto(e[i - 1], 'orange')
        sleep()
    t = [Point (224, 50), Point (224, 66), Point (216, 66), Point (231, 66)]
    for i in range(1, len(t)):
        t[i].lineto(t[i - 1], 'orange')
        sleep()
    r = [Point (233, 50), Point (233, 66), Point (247, 66), Point (247, 58), 
         Point (237, 58), Point (247, 50)]
    for i in range(1, len(r)):
        r[i].lineto(r[i - 1], 'orange')
        sleep()
    i = [Point (252, 50), Point (264, 50), Point (258, 50), 
         Point (258, 66), Point (252, 66), Point (264, 66)]
    for j in range(1, len(i)):
        i[j].lineto(i[j - 1], 'orange')
        sleep()
    c = [Point (285, 50), Point (269, 50), Point (269, 66), Point (285, 66)]
    for i in range(1, len(c)):
        c[i].lineto(c[i - 1], 'orange')
        sleep()

def escreve_algorithms():
    a = [Point (315, 50), Point (319, 60), Point (331, 60), Point (319, 60), 
         Point (323, 70), Point (327, 70), Point (335, 50)]
    for i in range(1, len(a)):
        a[i].lineto(a[i - 1], 'orange')
        sleep()
    l = [Point (339, 66), Point (339, 50), Point (352, 50)]
    for i in range(1, len(l)):
        l[i].lineto(l[i - 1], 'orange')
        sleep()
    g = [Point (370, 66), Point (356, 66), Point (356, 50), Point (370, 50),
         Point (370, 58), Point (364, 58)]
    for i in range(1, len(g)):
        g[i].lineto(g[i - 1], 'orange')
        sleep()
    o = [Point (374, 50), Point (374, 66), Point (387, 66), Point (387, 50)]
    for i in range(len(o)):
        o[i].lineto(o[i - 1], 'orange')
        sleep()
    r = [Point (392, 50), Point (392, 66), Point (408, 66), Point (408, 58), 
         Point (398, 58), Point (408, 50)]
    for i in range(1, len(r)):
        r[i].lineto(r[i - 1], 'orange')
        sleep()
    i = [Point (413, 50), Point (426, 50), Point (419, 50), 
         Point (419, 66), Point (426, 66), Point (413, 66)]
    for j in range(1, len(i)):
        i[j].lineto(i[j - 1], 'orange')
        sleep()
    t = [Point (438, 50), Point (438, 66), Point (430, 66), Point (446, 66)]
    for i in range(1, len(t)):
        t[i].lineto(t[i - 1], 'orange')
        sleep()
    h = [Point (451, 50), Point (451, 66), Point(451, 58), 
         Point (465, 58), Point (465, 50), Point (465, 66)]
    for i in range(1, len(h)):
        h[i].lineto(h[i - 1], 'orange')
        sleep()
    m = [Point (470, 50), Point (470, 66), Point (478, 58), Point (486, 66), Point(486, 50)]
    for i in range(1, len(m)):
        m[i].lineto(m[i - 1], 'orange')
        sleep()
    s = [Point (507, 66), Point (491, 66), Point (491, 58),
         Point (507, 58), Point (507, 50), Point (491, 50)]
    for i in range(1, len(s)):
        s[i].lineto(s[i - 1], 'orange')
        sleep()
        
def anima_gema (delay):
    " Função principal: Recebe uma coleção de pontos e retorna uma DCEL da triangulão "
    " de Delauney desses pontos, desenhando os passos do algoritmo na tela "
    d = Dcel()
    clara, pontos = main()
    random.shuffle (pontos)
    #pontos = sorted(pontos, key = lambda x:-x.y)
    
    global infs
    global desenha_busca
    global pula
    delay.set(10)
    inf1, inf2, inf3 = pontos_infinitos (pontos)
    infs = [inf1, inf2, inf3]
    
    # Cria o triangulo auxiliar grandão que contém toda a coleção
    raiz = Node_Triang (inf1, inf2, inf3, None)
    d.add_vertex (inf1)
    d.add_vertex (inf2)
    d.add_vertex (inf3)
    e1 = d.add_edge (inf1, inf2)
    e2 = d.add_edge (inf2, inf3)
    e3 = d.add_edge (inf3, inf1)
    raiz.a = e1.twin
    
    # Toda vez que criarmos uma face vamos ter que associar a folha do dag a essa face
    d.extra_info[e1.f] = raiz

    # Processamento principal
    for p in pontos:
        triang = raiz.busca (p)
        
        # Caso degenerado
        # 1. Pontos Coincidentes -> Apenas ignoro
        if p == triang.p1 or p == triang.p2 or p== triang.p3:
            p.unhilight()
            continue
        
        # Adiciona as três arestas na dcel
        e1, e2, e3 = add_triangs_dcel (d, p, triang)
        novas = [e1, e2, e3]
        # Adiciona as novas faces/triangulos no dag e dcel
        novos_triangs = [Node_Triang (triang.p1, triang.p2, p, e1),
                         Node_Triang (triang.p2, triang.p3, p, e2),
                         Node_Triang (triang.p3, triang.p1, p, e3)]
        for t in novos_triangs:
            triang.filhos.append (t)
            d.extra_info[t.a.f] = t
            
        # Legaliza arestas
        legalizaveis = [e1.prox, e2.prox, e3.prox]

        while len (legalizaveis) > 0:
            e = legalizaveis.pop()
            
            if ilegal (e):
                # Guarda os triangulos que serão 'removidos' das folhas do dag
                pai1 = d.extra_info[e.f]
                pai2 = d.extra_info[e.twin.f]
                
                # Revome a diagonal ilegal e adiciona a legal
                d.remove_edge (e)
                e_nova = d.add_edge (e.prox.to, e.twin.prox.to, e.prox.f)
                novas.append(e_nova)
                
                # Adiciona os novos triangulos no dag
                t1 = Node_Triang (e.to, e.prox.to, e.twin.prox.to, e_nova)
                t2 = Node_Triang (e.init, e.prox.to, e.twin.prox.to, e_nova.twin)
                pai1.filhos = pai2.filhos = [t1, t2]
                # referencia as novas folhas do dag para suas faces na dcel
                d.extra_info[e_nova.f] = t1
                d.extra_info[e_nova.twin.f] = t2
                # Adiciona as arestas dos novos triangs na fila de legalizáveis
                for l in [e_nova.prox, e_nova.prev, e_nova.twin.prox, e_nova.twin.prev]:
                    if l.init != p and l.to != p:
                        legalizaveis.append(l)
        # Recolore as arestas que estavam com a outra cor
        for e in novas:
            if e.init in clara or e.to in clara:
                if e.init in clara and e.to in clara:
                    color_triang = "white"
                else:
                    color_triang = 'black'
            else:
                color_triang = "orange"
            if e.init not in infs and e.to not in infs:
                e.draw(color_triang)
        sleep()
    
    # Depois de processar todos os pontos, removo os pontos do infinito
    for i in infs:
        rem = d.v[i].twin.prox
        while rem != d.v[i]:
            d.remove_edge(rem)
            rem = rem.twin.prox
        d.remove_edge(rem)
        d.v.pop(i)
        sleep()
        
    delay.set(50)
    escreve_gema()
    delay.set(5)
    escreve_geometric()
    escreve_algorithms()
    pula = False
        