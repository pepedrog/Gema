# -*- coding: utf-8 -*-
""" Funções para desenhar no canvas 

Todas as funções retornam o id do desenho, que é necessário para apagar o desenho
As funções são basicamente as funções do canvas, um pouco mais amigaveis
Evite chamar essas funções diretamente, use as funções plot() de cada classe

Como o canvas é coordenado de cima pra baixo, sempre desenhamos com a coordenada
y = (canvas.height - y), pra ficarem coordenadas cartesianas
"""

from tkinter import ALL
import time

master = None
canvas = None
delay = None
passo_a_passo = None

# Definições padrão
cor_normal = 'white'
cor_destaque = 'orange'
# Pontos
raio_ponto = 3
raio_ponto_destaque = 4
grossura_segmento = 2
# Círculos
cor_preenchimento = None

def plot_point (x, y, cor, r):
    y = float(canvas['height']) - y
    return canvas.create_oval (x - r, y - r, x + r, y + r, fill = cor)

def plot_segment (x0, y0, x1, y1, cor, grossura):
    y0 = float(canvas['height']) - y0
    y1 = float(canvas['height']) - y1
    return canvas.create_line (x0, y0, x1, y1, fill = cor, width = grossura)

def plot_disc (x, y, r, cor_borda, cor_preenchimento, grossura):
    y = float(canvas['height']) - y
    return canvas.create_oval (x - r, y - r, x + r, y + r, outline = cor_borda,
                               width = grossura, fill = cor_preenchimento)

def plot_vert_line (x, cor = cor_normal, grossura = grossura_segmento):
    return canvas.create_line (x, 0, x, float(canvas['height']), fill = cor, width = grossura)

def plot_horiz_line (y, cor = cor_normal, grossura = grossura_segmento):
    y = float(canvas['height']) - y
    return canvas.create_line (0, y, float(canvas['width']), y, fill = cor, width = grossura)

def change_point_color (point_id, nova_cor):
    canvas.itemconfig (point_id, fill = nova_cor)
    
def plot_semi_circle (x0, y0, r, up, cor, grossura):
    "desenha um meio circulo de centro (x0, y0) e raio r, up indica se é a metade de cima"
    if up:
        sinal = 1
    else:
        sinal = -1    
    xy = []
    x = x0 - r
    step = r/100
    while x <= x0 + r:
        # Aplica a fórmula do círculo
        y = sinal * (r**2 - (x - x0)**2)**0.5 + y0
        xy.append(canvas.r2cx(x))
        xy.append(canvas.r2cy(y))
        x += step
    return canvas.create_line (xy, fill=cor, width=grossura)

def plot_delete (plot_id):
    canvas.delete (plot_id)

def sleep ():
    " Função para congelar a execução do algoritmo por um tempo "
    if master.passo_a_passo.get():
        master.tk.wait_variable (master.novo_passo)
    else:
        master.tk.after (master.delay.get(), master.tk.quit)
        master.tk.mainloop ()

def clear():
    canvas.delete(ALL)