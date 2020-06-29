#!/usr/bin/env python

from geocomp.common.vector import Vector
from geocomp.common.prim import dist2
import desenhos

class Point:
    "Um ponto representado por suas coordenadas cartesianas"

    def __init__ (self, x, y):
        "Para criar um ponto, passe suas coordenadas."
        self.x, self.y = x, y
        self.lineto_id = {}
        
        self.plot_id = None
        self.hi = None

    def __repr__ (self):
        "Retorna uma string da forma '( x y )'"
        return ("( " + str(self.x) + " " + str(self.y) + " )" )

    def __add__(self, other):
        if not isinstance(other, Point) and not isinstance(other, Vector):
            raise ValueError('Cannot add point with non point or vector')
        if other.dimension != self.dimension:
            raise ValueError("Cannot add {0}-d point with {1}-d point" \
                             .format(self.dimension, other.dimension))
        return Point(*[self[i] + other[i] for i in range(self.dimension)])

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 31 * hash(self.x) + hash(self.y)

    def plot (self, cor = desenhos.cor_normal, r = desenhos.raio_ponto):
        "Desenha o ponto na cor especificada"
        self.plot_id = desenhos.plot_point(self.x, self.y, cor, r)

    def unplot(self):
        if self.plot_id is not None: desenhos.plot_delete (self.plot_id)

    def hilight (self, cor = desenhos.cor_destaque):
        "Desenha o ponto com 'destaque' (raio maior e cor diferente)"
        if self.hi != None: desenhos.plot_delete (self.hi)
        self.hi = desenhos.plot_point(self.x, self.y, cor, r = desenhos.raio_ponto_destaque)
        return self.hi

    def unhilight (self):
        "Apaga o 'destaque' do ponto"
        if self.hi is not None: desenhos.plot_delete (self.hi)

    def lineto (self, p, color=desenhos.cor_normal, grossura=desenhos.grossura_segmento):
        "Desenha uma linha ate um ponto p na cor especificada"
        self.lineto_id[p] = desenhos.plot_segment (self.x, self.y, p.x, p.y, color, grossura)
        return self.lineto_id[p]

    def remove_lineto (self, p):
        "Apaga a linha ate o ponto p"
        if self.lineto_id[p] is not None: desenhos.plot_delete (self.lineto_id[p])

    def distance_to(self, other):
        return dist2(self, other) ** 0.5

    def is_inside(self, segment):
        ''' returns if point is inside the segment. '''
        return segment.has_inside(self)

    def approx_equals(self, other, precision=1e-7):
        return abs (self.x - other.x) < precision and abs (self.y - other.y)

    

    """
    Ordem dada por y, desempatando por x 
    PS: Usado no projeto do Lucas Moretto de Visibility Graph.
    """
    def __lt__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        if self.y < other.y:
            return True
        if self.y > other.y:
            return False
        if self.x < other.x:
            return True
        return False

    def __le__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        if self.y < other.y:
            return True
        if self.y > other.y:
            return False
        if self.x < other.x:
            return True
        if self.x > other.x:
            return False
        return True


#### Bruna & Renan ########

class Edge:

	def __init__(self, v1, v2):
		"Para criar uma aresta, passe suas coordenadas."
		self.point = v1
		self.twin = None
		self.prev = None
		self.next = None

	def __repr__ (self):
		return '( ' + repr(self.point) + ' )'
##########################
    
