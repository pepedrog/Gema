# -*- coding: utf-8 -*-

from random import randint
from estruturas.point import Point 

def input_aleatorio (tipo, n, max_x, max_y):
    " Retorna n objetos na área dada por (0, max_x, 0, max_y) "
    ret = []
    if tipo == 0:
        for i in range(n):
            ret.append(Point (randint(25, max_x - 25), randint(25, max_y - 25)))
    return ret