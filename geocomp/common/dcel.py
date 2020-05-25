"""
    Implementação de uma DCEL (Double Connected Edge List)
    Uma lista de arestas duplamente ligadas para representar grafos planares
    
    Guarda, para cada vértice, uma meia aresta incidente a ele e para cada face,
    uma meia aresta da sua fronteira.
    
    Cada meia aresta guarda um ponteiro para a próxima e anterior, seus vértices,
    um ponteiro para sua aresta gêmea (ou outra meia aresta) e o índice da sua face
"""

from .prim import left, right

class half_edge:
    def init (self, init, to, f, prox, prev, twin):
        self.init = init # Point
        self.to = to     # Point
        self.f = f       # Int
        self.prox = prox # half_edge
        self.prev = prev # half_edge
        self.twin = twin # half_edge
    
    def __eq__ (self, other):
        return self.init == other.init and self.to == other.to

class Dcel:
    def init (self, v = []):
        self.v = dict()
        for p in v:
            self.v[p] = None
        self.f = [None]
    
    def add_vertex (self, p):
        self.v[p] = None
    
    def add_edge (self, v1, v2):
        prox1 = self.prox_edge (v1, v2)
        prox2 = self.prox_edge (v2, v1)
        e1 = half_edge (v1, v2, None, prox1, prox1.prev, None)
        e2 = half_edge (v2, v1, None, prox2, prox2.prev, e1)
        e1.twin = e2
        
        e1.prox.prev = e1
        e1.prev.prox = e1
        e2.prox.prev = e2
        e2.prev.prox = e2
        
        cc1 = close_circuit (e1)
        cc2 = close_circuit (e2)
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

    def create_face (self, e):
        new = len (self.f)
        e.f = new
        self.f.append (e)

        aux = e.prox
        while aux != e:
            aux.f = new
            aux = aux.prox

    def prox_edge (self, v1, v2):
        " Encontra a meia aresta que sai de v2 que deixa v1 a sua direita "
        aux = self.v[v2]
        while aux != None and right (v2, aux.to, v1):
            aux = aux.twin
            if aux != None:
                aux = aux.prox
        while aux != None and left (v2, aux.to, v1):
            aux = aux.prev
            if aux != None:
                aux = aux.twin
        return aux
    
    def close_circuit (e):
        " Indica se a inclusão se uma aresta e cria uma nova face"
        aux = e.prox
        while aux != None and aux != e:
            aux = aux.prox
        return aux == e