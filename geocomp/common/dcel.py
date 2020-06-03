"""
    Implementação de uma DCEL (Double Connected Edge List)
    Uma lista de arestas duplamente ligadas para representar grafos planares
    
    A estrutura guarda, para cada vértice, uma meia aresta que tem ele como origem e para cada face,
    uma meia aresta da sua fronteira.
    
    Cada meia aresta guarda um ponteiro para a próxima e anterior, seus vértices e
    um ponteiro para sua aresta gêmea (ou outra meia aresta)
"""

from geocomp.common.prim import left, right
# Tem que tirar as faces
class half_edge:
    def __init__ (self, init, to, f, prox, prev, twin):
        self.init = init # Point
        self.to = to     # Point
        self.prox = prox # half_edge
        self.prev = prev # half_edge
        self.twin = twin # half_edge
    
    def __eq__ (self, other):
        return other != None and self.init == other.init and self.to == other.to
    
    def __str__ (self):
        return str(self.init) + "->" + str(self.to)

class Dcel:
    def __init__ (self):
        self.v = dict()
    
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
        
        self.v[v1] = e1
        self.v[v2] = e2

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
    
    def get_faces (self):
        " Retorna uma lista de meia arestas, cada uma representando uma face "
        # Vamos criar uma cópia dos vértices e ir removendo eles montando as faces
        v_cp = self.v.copy()
        # Deleta todos os vértices de grau 1
        for v in v_cp.keys():
            candidato = v
            while self.degree (v_cp, candidato) < 2:
                candidato = v_cp[v].to
                # deleta a resta que entra em v
                incidente = v_cp[v].twin
                incidente.prev.prox = v_cp[v].prox
                v_cp[v].prox.prev = incidente.prev
                # Deleta a aresta que sai de v
                del v_cp[v]
        
        # Agora que temos um grafo conexo, em que todo vértice tem grau > 2
        # Vamos fazer uma varredura no grafo, no esquema de uma busca em profundidade
        visitados = dict()
        for v in v_cp.keys():
            visitados[v] = False
        faces = []
        
        self.__get_faces_dfs (visitados, faces, self.v[0])
        return faces

    def __get_faces_dfs (self, visitados, faces, aresta_origem, f_max):
        """ Função recursiva para a dfs, se um dos vizinhos do aresta_origem.to 
        já foi visitado, adiciona a nova aresta representando uma nova face no vetor faces """
        # Adiciona as 
        atual = aresta_origem.to
        visitados[atual] = True
        v = aresta_origem.next
        while v != aresta_origem:
            if visitados[v.to]:
                faces.append (v)
                if (faces_restantes == 0): return
            else: self.__get_faces_dfs (visitados, faces, v, faces_restantes)
            v = v.twin.prox
            ## TALVEZ ISSO NÂO FUNCIONE AAA VAI MARCAR FACES REPETIDAS
            # PARA ENTENDER depois: https://www.geeksforgeeks.org/print-all-the-cycles-in-an-undirected-graph/
            # https://www.cs.tufts.edu/comp/150GA/homeworks/hw1/Johnson%2075.PDF
            # https://www.codeproject.com/Articles/1158232/Enumerating-All-Cycles-in-an-Undirected-Graph
            # https://mosaic.mpi-cbg.de/docs/Schneider2015.pdf
        
    def degree (v):
        " Retorna o número de arestas incidentes a v "
    
    def __str__ (self):
        " representação em string para testes "
        s = "Vértices\n"
        for p in self.v:
            s += str(p) + ":" + str(self.v[p])
        return s
    