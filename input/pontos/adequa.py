# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 08:49:46 2020

@author: gigec
"""
from math import *
import random
RADIUS = 210

def rand_n_vertices (num_pts, num_vertices, radius):
    if radius < 0: radius = -radius
    if radius == 0: radius = 10000

    if num_vertices < 4: num_vertices = 4

    if num_vertices > num_pts:
        num_vertices, num_pts = num_pts, num_vertices
    
    l1 = randdisc (num_pts - num_vertices, 0.7*radius)
    l2 = uniform_circ (num_vertices, radius)

    l1.extend (l2)

    return l1

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
    for i in range(linhas):
        for j in range(colunas):
            l.append ([(i+1)* 600/(linhas+1), (j+1) * 600/(colunas+1)])
    return l
            
def main ():
    " Função que trata o clique do botão 'Gravar Input' "
    " Escrevendo o self.input num arquivo de nome "
    #f = open('spiral_03')
    #input = []
    #for p in f:
    #    x, y = float(p.split()[0]), float(p.split()[1])
    #    x, y = x + 50, y + 50
    #    input.append ([x, y])
    f = open('regular_500', "w")
    for i in uniform_circ(500, RADIUS):
        f.write ('%f %f\n' % (i[0] + 300, i[1] + 300))
    f.close()
    # Poligono
main()