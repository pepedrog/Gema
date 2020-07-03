#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

"""Primitivas geometricas usadas nos algoritmos

Use o modulo geocomp.common.guiprim para que essas primitivas sejam
desenhadas na tela  medida que elas so usadas. Tambm  possvel
desenh-las de um jeito especfico para um determinado algoritmo.
Veja geocomp.convexhull.quickhull para um exemplo.
"""

def area2 (a, b, c):
    "Retorna duas vezes a area do tringulo determinado por a, b, c"
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

def area_sign(a, b, c):
    area = area2(a, b, c)
    if area > 0:
        return 1
    if area < 0:
        return -1
    return 0

def left (a, b, c):
    "Verdadeiro se c est  esquerda do segmento orientado ab"
    return area2 (a, b, c) > 0

def left_on (a, b, c):
    "Verdadeiro se c est  esquerda ou sobre o segmento orientado ab"
    return area2 (a, b, c) >= 0

def collinear (a, b, c):
    "Verdadeiro se a, b, c sao colineares"
    return area2 (a, b, c) == 0

def right (a, b, c):
    "Verdadeiro se c est  direita do segmento orientado ab"
    return not (left_on (a, b, c))

def right_on (a, b, c):
    "Verdadeiro se c est  direita ou sobre o segmento orientado ab"
    return not (left (a, b, c))

def dist2 (a, b):
    "Retorna o quadrado da distancia entre os pontos a e b"
    dy = b.y - a.y
    dx = b.x - a.x

    return dy*dy + dx*dx

# epsilon do erro
ERR = 1.0e-5

def cmpFloat(a, b):
	"Comparacao de float com margem de erro com preferencia para a igualdade"
	if (abs(a-b) < ERR):
		return 0
	elif (a + ERR > b):
		return 1
	return -1

def float_left (a, b, c):
	"Verdadeiro se c est  esquerda do segmento orientado ab utilizando comparacao de float"
	if(cmpFloat(area2 (a, b, c), 0) == 1):
		return True
	return False

def float_left_on (a, b, c):
	"Verdadeiro se c est  esquerda ou sobre o segmento orientado ab utilizando comparacao de float"
	if(cmpFloat(area2 (a, b, c), 0) == 0):
		return True
	return False