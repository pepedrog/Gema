"""
    Implementação de uma DCEL (Double Connected Edge List)
    Uma lista de arestas duplamente ligadas para representar grafos planares
    
    A estrutura guarda, para cada vértice, uma meia aresta que tem ele como origem e para cada face,
    uma meia aresta da sua fronteira.
    
    Cada meia aresta guarda um ponteiro para a próxima e anterior, seus vértices,
    um ponteiro para sua aresta gêmea (ou outra meia aresta) e o índice da sua face
"""

from geocomp.common.prim import left, right

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
        
        e1 = half_edge (v1, v2, 0, None, None, None)
        e2 = half_edge (v2, v1, 0, None, None, e1)
        e1.twin = e2
        
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
        
        cc1 = e1.close_circuit()
        cc2 = e2.close_circuit()
        if cc1 and not cc2:
            e2.f = e2.prox.f
            self.f[e2.f] = e2
            self.create_face (e1)
        if cc2:
            e1.f = e1.prox.f
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
        " Encontra a meia aresta que sai de v2 que deixa v1 a sua direita "
        if self.v[v2] == None:
            return None
        
        aux = self.v[v2]
        # Vai rodando no sentido horário até passar do v1 ou voltar
        while right (v2, aux.to, v1) and right (v2, aux.to, aux.twin.prox.to):
            aux = aux.twin.prox
        # Vai rodando no sentido anti-horário até passar do v1 ou voltar
        while left (v2, aux.to, v1) and left (v2, aux.to, aux.prev.twin.to):
            aux = aux.prev.twin
        return aux
    
    def __str__ (self):
        " representação em string para testes "
        s = "Vértices\n"
        for p in self.v:
            s += str(p) + ":" + str(self.v[p])
        s += "\nFaces:\n"
        for i in range(len(self.f)):
            s += str(i) + ":" + str(self.f[i])
        return s
        