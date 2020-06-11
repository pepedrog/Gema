# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
import os
#from PIL import ImageTk, Image

cor_botao = "snow"
cor_fundo = "orange"

class Home ():
    def __init__ (self):
        # Cria a tela
        self.tk = Tk()
        self.tk.title = "GEMA"
        # Lista de algoritmos
        self.algoritmos = [('Par mais Próximo', 'geocomp/par_proximo'),
                           ('Fecho Covexo', 'geocomp/fecho'),
                           ('Triangulação de Delauney', 'geocomp/delauney'),
                           ('Triangulação de Polígonos', 'geocomp/delauney'),
                           ('Interseção de Segmentos', 'geocomp/inter_segs'),
                           ('Interseção de Círculos', 'geocomp/inter_circs')]
        
        # Lista do tipo de Arquivos
        self.tipos_input = [('Pontos', 'input/pontos'),
                            ('Polígonos', 'input/poligonos'),
                            ('Segmentos', 'input/segmentos'),
                            ('Círculos', 'input/circulos')]
        
        # Frame principal que contem todos os outros
        self.main_frame = Frame (self.tk, bg = cor_fundo)
        self.main_frame.pack(fill = BOTH, expand = True)
        
        # Frame com o logo e os botões pros algoritmos        
        self.frame_botoes = Frame (self.main_frame, bg = cor_fundo)
        #img = ImageTk.PhotoImage (Image.open('logo_teste.jpg'))
        img_lbl = Label (self.frame_botoes, # image = img, 
                         width = 25, height = 10)
        img_lbl.pack()
        self.cria_botoes()
        self.frame_botoes.pack(side=LEFT, anchor = N, padx = 20, pady = 20)
        
        # Frame com o canvas do input
        self.frame_input = Frame (self.main_frame,pady = 20, bg = cor_fundo)
        self.canvas = Canvas (self.frame_input, width = 500, height = 500)
        self.canvas['bg'] = "black"
        self.canvas.pack(fill = BOTH, expand = True)
        self.frame_input.pack(side=LEFT, fill = BOTH, expand = True)
        
        # Frame com os arquivos
        self.frame_arquivos = Frame(self.main_frame,bg = cor_fundo)
        self.cria_abas ()
        self.frame_arquivos.pack(side=LEFT, padx = 20, pady = 20, anchor = N)
    
    def cria_botoes (self):   
        for a in self.algoritmos:
            # Cria o botão
            b = Button (self.frame_botoes, text = a[0])
            b['command'] = lambda arg = a[1]: self.abre_tela (arg)
            b['relief'] = "ridge"
            b['bg'] = cor_botao
            b['activebackground'] = cor_botao
            b['width'] = 25
            b['height'] = 2
            b.pack(pady = (4, 0))
    
    def cria_abas (self):
        # Configura o estilo das abas
        ttk.Style().configure ("TNotebook", background = cor_fundo);
        ttk.Style().configure("TNotebook.Tab", background=cor_botao, padding = (5, 10));
        abas = ttk.Notebook (self.frame_arquivos, height = 300)
        # Adiciona uma aba pra cada tipo de input
        for tipo in self.tipos_input:
            aba = Frame (abas)
            arquivos = Listbox (aba, height = 200)
            i = 0
            # Popula cada aba
            for arq in os.listdir(tipo[1]):
                arquivos.insert(i, arq)
                i += 1
            # Adiciona o scroll
            sb = Scrollbar (aba, orient = 'vertical')      
            sb.config (command = arquivos.yview)
            sb.pack(side = RIGHT, fill = Y)
            arquivos.config (yscrollcommand = sb.set)
            # Adiciona tudo na aba
            arquivos.pack (fill = BOTH)
            aba.pack(fill = BOTH)
            abas.add (aba, text = tipo[0], padding = 5)
        abas.pack()
            
    def abre_tela (self, tela):
        print(tela)

Home = Home()
Home.tk.mainloop()