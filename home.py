# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font
class App ():
    def __init__ (self):
        # Cria a tela
        self.tk = Tk()
        self.tk.title = "GEMA"
        
        # Lista de algoritmos
        self.algoritmos = [('Par mais Próximo', 'geocomp/par_proximo'),
                           ('Interseção de Segmentos', 'geocomp/inter_segs'),
                           ('Triangulação de Delauney', 'geocomp/delauney'),
                           ('Triangulação de Polígonos', 'geocomp/delauney'),
                           ('Interseção de Círculos', 'geocomp/inter_circs'),
                           ('Fecho Covexo', 'geocomp/fecho')]
        
        # Frame principal
        self.main_frame = Frame (self.tk)
        self.main_frame.pack()
        
        # Frame com os botões
        self.frame_botoes = Frame (self.main_frame)
        self.cria_botoes()
        self.frame_botoes.pack(side=LEFT)
        
        # Frame com o canvas do input
        self.frame_input = Frame (self.main_frame, padx = 20, pady = 20)
        self.canvas = Canvas (self.frame_input, width = 500, height = 500)
        self.canvas['bg'] = "black"
        self.canvas.pack()
        self.frame_input.pack(side=RIGHT)
    
    def cria_botoes (self):   
        for a in self.algoritmos:
            # Cria o botão
            b = Button (self.frame_botoes, text = a[0])
            b['command'] = lambda arg = a[1]: self.abre_tela (arg)
            b['relief'] = "ridge"
            b['bg'] = "orange"
            b['activebackground'] = "orange"
            b['width'] = 25
            b['height'] = 2
            #b['font'] = "Courier"
            b.pack(pady = 2, padx = (20, 0))
        
    def abre_tela (self, tela):
        print(tela)

Home = App()
Home.tk.mainloop()
        
        
