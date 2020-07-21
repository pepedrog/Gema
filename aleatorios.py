# -*- coding: utf-8 -*-

from random import randint, uniform, gauss, random
import math
from estruturas.disc import Disc 
from estruturas.point import Point 
from estruturas.polygon import Polygon 
from estruturas.segment import Segment 

def input_aleatorio (tipo, n, max_x, max_y):
    " Retorna n objetos na área dada por (0, max_x, 0, max_y) "
    ret = []
    if tipo == 0:
        for i in range(n):
            ret.append(Point (randint(25, max_x - 25), randint(25, max_y - 25)))
    elif tipo == 2:
        for i in range(n):
            ret.append(Segment(Point (randint(25, max_x - 25),
                                      randint(25, max_y - 25)),
                               Point (randint(25, max_x - 25),
                                      randint(25, max_y - 25))))
    elif tipo == 3:
        for i in range(n):
            x = randint(50, max_x - 50)
            y = randint(50, max_y - 50)
            ret.append(Disc(x, y, randint(5, min([x, y, 
                                                  max_x - x, max_y - y]) - 10)))
    elif tipo == 1:
        x = max_x / 2
        y = max_y / 2
        v = randomPolygon (x, y, min(x, y)/2, uniform(0, 1), uniform(.1, .4), n)
        ret = Polygon (v)
    return ret

# Eu genuinamente copiei esse código de 
# https://stackoverflow.com/questions/8997099/algorithm-to-generate-random-2d-polygon
def randomPolygon( ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts ) :
    ''' Start with the centre of the polygon at ctrX, ctrY, 
        then creates the polygon by sampling points on a circle around the centre. 
        Randon noise is added by varying the angular spacing between sequential points,
        and by varying the radial distance of each point from the centre.
    
        Params:
        ctrX, ctrY - coordinates of the "centre" of the polygon
        aveRadius - in px, the average radius of this polygon, this roughly controls how large the polygon is, really only useful for order of magnitude.
        irregularity - [0,1] indicating how much variance there is in the angular spacing of vertices. [0,1] will map to [0, 2pi/numberOfVerts]
        spikeyness - [0,1] indicating how much variance there is in each vertex from the circle of radius aveRadius. [0,1] will map to [0, aveRadius]
        numVerts - self-explanatory
    
        Returns a list of vertices, in CCW order.
    '''

    irregularity = clip( irregularity, 0,1 ) * 2*math.pi / numVerts
    spikeyness = clip( spikeyness, 0,1 ) * aveRadius

    # generate n angle steps
    angleSteps = []
    lower = (2*math.pi / numVerts) - irregularity
    upper = (2*math.pi / numVerts) + irregularity
    sum = 0
    for i in range(numVerts) :
        tmp = uniform(lower, upper)
        angleSteps.append( tmp )
        sum = sum + tmp

    # normalize the steps so that point 0 and point n+1 are the same
    k = sum / (2*math.pi)
    for i in range(numVerts) :
        angleSteps[i] = angleSteps[i] / k

    # now generate the points
    points = []
    angle = uniform(0, 2*math.pi)
    for i in range(numVerts) :
        r_i = clip( gauss(aveRadius, spikeyness), 0, 2*aveRadius )
        x = ctrX + r_i*math.cos(angle)
        y = ctrY + r_i*math.sin(angle)
        points.append( Point(int(x),int(y)) )

        angle = angle + angleSteps[i]

    return points

def clip(x, min, max):
    if( min > max ):  return x    
    elif( x < min ):  return min
    elif( x > max ):  return max
    else:             return x