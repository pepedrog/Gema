# -*- coding: utf-8 -*-
""" Funções para desenhar no canvas 

Todas as funções retornam o id do desenho, que é necessário para apagar o desenho
As funções são basicamente as funções do canvas, um pouco mais amigaveis

Como o canvas é coordenado de cima pra baixo, sempre desenhamos com a coordenada
y = (canvas.height - y), pra ficarem coordenadas cartesianas

"""
from tkinter import ALL

canvas = None

# Definições padrão
cor_ponto = "white"
cor_segmento = "orange"
cor_destaque = "yellow"
cor_circulo = "white"
cor_preenchimento = "black"
raio_ponto = 3
raio_ponto_destaque = 4
cor_ponto_destaque = "orange"
grossura_segmento = 2

def plot_point (x, y, cor = cor_ponto, r = raio_ponto):
    y = float(canvas['height']) - y
    return canvas.create_oval (x - r, y - r, x + r, y + r, fill = cor)

def plot_segment (x0, y0, x1, y1, cor = cor_segmento, grossura = grossura_segmento):
    y0 = float(canvas['height']) - y0
    y1 = float(canvas['height']) - y1
    return canvas.create_line (x0, y0, x1, y1, fill = cor, width = grossura)

def plot_disc (x, y, r, cor_borda = cor_circulo,
               cor_preenchimento = None, grossura = grossura_segmento):
    y = float(canvas['height']) - y
    return canvas.create_oval (x - r, y - r, x + r, y + r, outline = cor_borda,
                               width = grossura, fill = cor_preenchimento)

def plot_vert_line (x, cor = cor_segmento, grossura = grossura_segmento):
    return canvas.create_line (x, 0, x, float(canvas['height']), fill = cor, width = grossura)

def plot_horiz_line (y, cor = cor_segmento, grossura = grossura_segmento):
    y = float(canvas['height']) - y
    return canvas.create_line (0, y, float(canvas['width']), y, fill = cor, width = grossura)

def change_point_color (point_id, new_color):
    canvas.itemconfig (point_id, fill = new_color)
    
def plot_delete (plot_id):
    canvas.delete (plot_id)

def clear():
    canvas.delete(ALL)