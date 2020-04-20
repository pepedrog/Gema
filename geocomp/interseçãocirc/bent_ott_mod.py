from geocomp.common.point import Point
from geocomp.common.segment import Segment
from geocomp.common.control import sleep

def equadores (circulos):
    "Função que retorna uma lista de segmentos l"
    "onde l[i] é um segmento que divide o circulos[i] no meio (linha do equador)"
    l = []
    for c in circulos:
        extremo1 = c.center - Point (c.r, 0)
        extremo2 = c.center + Point (c.r, 0)
        extremo1.plot (color = 'red')
        extremo2.plot (color = 'red')
        
        s = Segment (extremo1, extremo2)
        s.plot()
        sleep()
        
        l.append (s)
    return l    
        
def Bentley_Ottmann_Mod (l):
    
    # Pré-processamento - Transforma cada circulo em sua linha do equador
    eq = equadores (l)
    print(eq)
    