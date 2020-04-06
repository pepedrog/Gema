#!/usr/bin/env python
"""Algoritmo de Divisão e Conquista (Shamos e Hoey)"""

from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.prim import *
import math

# distancia global para manter atualizada
d = float("inf")

def dist (par):
    d2 = dist2 (par.init, par.to)
    if d2 > 0:
        return  d2
    return float("inf")
def minPar (a, b):
    " Recebe dois segmentos e retorna aquele com menor distancia "
    if (dist (a) < dist (b)):
        return a
    return b

def candidatos (l, i, j):
    " Retorna uma lista dos pontos dentro da faixa [-d, +d] do ponto do leio da lista l[i:j] "
    global d
    meio = l[(i + j)//2]
    cand = []
    for p in l[i:j]:
        if abs(p.x - meio.x) < d:
            cand.append (p)
    
    return cand

def menorInter (l, i, j, par_min):
    " Retorna o par de pontos mais proximo dentro da faixa dada pelo ponto meio da lista "
    " e a distancia do min_par "
    print("entrei no inter")
    global d
    par_inter = par_min
    # desenha a faixa que eu estou procurando
    v1 = control.plot_vert_line (l[(i + j)//2].x - d, "blue")
    v2 = control.plot_vert_line (l[(i + j)//2].x + d, "blue")
    control.sleep()
    
    cand = candidatos (l, i, j)
    
    for k in range(len(cand)):
        for l in range(k + 1, len(cand)):
            
            # Se os pontos já estão distantes, posso parar de olhar
            if (cand[l].y - cand[k].y > d):
                break
            
            dcand = dist2 (cand[k], cand[l])
            if (dcand < d):
                d = dcand
                par_inter = Segment (cand[k], cand[l])
    
    control.plot_delete (v1)
    control.plot_delete (v2)
    control.sleep()
    return par_inter
                

def intercalaY (l, i, j):
    " Função que recebe uma lista l[i:j] dividida em metades ordenadas e intercala "
    " as duas metades, é o intercala do mergeSort "
    meio = i + j // 2
    ini1 = i
    ini2 = meio
    
    aux = []
    while (ini1 < meio and ini2 < j):
        if l[ini1].y < l[ini2].y:
            aux.append(l[ini1])
            ini1 += 1
        else:
            aux.append(l[ini2])
            ini2 += 1
            
    # Copia a metade que falta no vetor
    while ini1 < meio:
        aux.append(l[ini1])
        ini1 += 1
    while ini2 < j:
        aux.append(l[ini2])
        ini2 += 1
    
    l[i:j] = aux[:]
            

def ShamosRec (l, i, j):
    " Função que faz o serviço recursivo " 
    " recebe uma lista de pontos l[i:j] ordenados pela coordenada x "
    # Base da recursão, 2 ou 1 ponto
    print (str(i) + " " + str(j))
    if j - i < 3:
        # registra o par mais proximo
        par_min = Segment(l[i], l[j - 1])
        # Ordena pelo eixo y
        if (l[i].y > l[j - 1].y):
            l[i], l[j - 1] = l[j - 1], l[i]
    else:
        q = (i + j) // 2
        print (q)
        vert_id = control.plot_vert_line(l[q].x)
        l[q].hilight()
        control.sleep()
        
        # Calcula o menor das duas metades
        par_esq = ShamosRec (l, i, q)
        par_dir = ShamosRec (l, q, j)
        
        par_min = minPar (par_esq, par_dir)
        par_esq.hide()
        par_dir.hide()
        # Intercala do mergeSort escondido
        intercalaY (l, i, j)
        
        control.plot_delete (vert_id)
        l[q].unhilight()
        control.sleep()
        
        par_inter = menorInter (l, i, j, par_min)
        par_min = minPar (par_inter, par_min)
    
    global d
    d = min (d, dist (par_min))
    par_min.plot("yellow")
    control.sleep()
    return par_min
        
        

def Shamos (l):
    "Algoritmo de divisão e conquista para encontrar o par de pontos mais proximo"
    "Recebe uma lista de pontos l"         

    if len (l) < 2: return None
    
    l = sorted(l, key = lambda x:x.x)
    ShamosRec (l, 0, len(l))