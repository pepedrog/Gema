"""
    Implementação de uma DCEL (Double Connected Edge List)
    Uma lista de arestas duplamente ligadas para representar grafos planares
    
    A estrutura guarda, para cada vértice, uma meia aresta que tem ele como origem e para cada face,
    uma meia aresta da sua fronteira.
    
    Cada meia aresta guarda um ponteiro para a próxima e anterior, seus vértices,
    um ponteiro para sua aresta gêmea (ou outra meia aresta) e o índice da sua face
"""

from geocomp.common.prim import left, right
from math import pi

class half_edge:
    def __init__ (self, init, to, f, prox, prev, twin):
        self.init = init # Point
        self.to = to     # Point
        self.f = f       # Int
        self.prox = prox # half_edge
        self.prev = prev # half_edge
        self.twin = twin # half_edge
    
    def __eq__ (self, other):
        return other != None and self.init == other.init and self.to == other.to
    
    def __str__ (self):
        return str(self.init) + "->" + str(self.to)
    
    def close_circuit (self):
        " Indica se a aresta e faz parte de um circuito fechado"
        aux = self.prox
        while aux != self:
            if aux.prox == aux.twin:
                return False
            aux = aux.prox
        return True

class Dcel:
    def __init__ (self):
        self.v = dict()
        self.f = [None]
    
    def add_vertex (self, p):
        self.v[p] = None
    
    def add_edge (self, v1, v2):
        # Adiciona as meias arestas
        e1 = half_edge (v1, v2, 0, None, None, None)
        e2 = half_edge (v2, v1, 0, None, None, e1)
        e1.twin = e2
        
        # Ajeita os ponteiros de prev e prox
        prox1 = self.prox_edge (v1, v2)
        prox2 = self.prox_edge (v2, v1)
        
        if prox1 == None:
            prox1 = e2
            prev2 = e1
        else:
            prev2 = prox1.prev
        if prox2 == None:
            prox2 = e1
            prev1 = e2
        else:
            prev1 = prox2.prev
        e1.prox = prox1
        e1.prev = prev1
        e2.prox = prox2
        e2.prev = prev2
        e1.prox.prev = e1
        e1.prev.prox = e1
        e2.prox.prev = e2
        e2.prev.prox = e2
        
        e1.f = e1.prox.f
        e2.f = e2.prox.f
        
        # Confere se criou uma nova face
        cc1 = e1.close_circuit()
        cc2 = e2.close_circuit()
        if cc1 and not cc2:
            self.f[e2.f] = e2
            self.create_face (e1)
        if cc2:
            self.f[e1.f] = e1
            self.create_face (e2)
            
        self.v[v1] = e1
        self.v[v2] = e2
        
        # Primeira Aresta adicionada
        if self.f[0] == None:
            self.f[0] = e1

    def create_face (self, e):
        " Cria uma face "
        new = len (self.f)
        e.f = new
        self.f.append (e)

        aux = e.prox
        while aux != e:
            aux.f = new
            aux = aux.prox

    def prox_edge (self, v1, v2):
        " Encontra a meia aresta que sai de v2 que deixa v1 a sua esquerda "
        if self.v[v2] == None:
            return None
        
        # Vou percorrer todas as arestas de v2 e achar a que forma angulo menor
        # com a aresta v1-v2, percorrendo no sentido antihorário
        def angulo (v3):
            # Vou achar, na verdade, o cosseno do angulo com a lei do cosseno
            a2 = (v3.x - v1.x)**2 + (v3.y - v1.y)**2
            b2 = (v3.x - v2.x)**2 + (v3.y - v2.y)**2
            c2 = (v1.x - v2.x)**2 + (v1.y - v2.y)**2
            ang = ((b2 + c2 - a2)/(2*((b2*c2)**0.5)))
            if right(v1, v2, v3):
                ang = - ang - 1000
            return -ang
            
        prox = self.v[v2]
        min_ang = angulo(prox.to)
        aux = prox.prev.twin
        # Vou rodando no sentido anti-horário pra achar a aresta certa
        while aux != self.v[v2]:
            ang_aux = angulo(aux.to)
            if ang_aux < min_ang:
                prox = aux
                ang_prox = ang_aux
            aux = aux.prev.twin
            
        return prox
    
    def initPolygon (self, P):
        " Transforma o self numa dcel para o polígono P "
        v = P.vertices()
        self.add_vertex (v[0])
        for i in range (1, len(v)):
            self.add_vertex (v[i])
            self.add_edge (v[i - 1], v[i])
        self.add_edge (v[-1], v[0])
    
    def __str__ (self):
        " representação em string para testes "
        s = "Vértices\n"
        for p in self.v:
            s += str(p) + ":" + str(self.v[p]) + "\n"
        s += "\nFaces:\n"
        for i in range(len(self.f)):
            s += str(i) + ":" + str(self.f[i]) + "\n"
        return s
        