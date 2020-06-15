# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import Grid
from tkinter import ttk

# Listas dos problemas e algoritmos para fazer os botões
from itens import problemas, algoritmos

# Classes dos objetos, para ler os arquivos
from estruturas.point import Point
from estruturas.polygon import Polygon
from estruturas.segment import Segment
from estruturas.disc import Disc
import os

import desenhos
#from PIL import ImageTk, Image

cor_botao = "snow"
cor_fundo = "orange"

class Home ():
    " Classe da aplicação principal, cuida de toda manipulação dos widgets "
    
    def __init__ (self):
        # Cria a tela
        self.tk = Tk()
        self.tk.title ("GEMA")
        
        # Lista do tipo de Arquivos
        self.tipos_input = [('Pontos', 'input/pontos'),
                            ('Polígonos', 'input/poligonos'),
                            ('Segmentos', 'input/segmentos'),
                            ('Círculos', 'input/circulos')]
        
        # Frame principal que contem todos os outros
        self.main_frame = Frame (self.tk, bg = cor_fundo)
        self.main_frame.pack(fill = BOTH, expand = True)
        Grid.columnconfigure(self.main_frame, 1, weight=1)
        Grid.rowconfigure(self.main_frame, 0, weight=1)
        
        # Frame com o logo e os botões pros problemas        
        self.frame_botoes = Frame (self.main_frame, bg = cor_fundo)
        #img = ImageTk.PhotoImage (Image.open('logo_teste.jpg'))
        img_lbl = Label (self.frame_botoes, # image = img, 
                         width = 25, height = 10)
        img_lbl.pack()
        self.cria_botoes()
        self.frame_botoes.grid (row = 0, column = 0, padx = 20, pady = 20, sticky = N)
        
        # Frame com o canvas do input
        self.frame_input = Frame (self.main_frame,pady = 20, bg = cor_fundo)
        self.canvas = Canvas (self.frame_input, width = 700, height = 700)
        self.canvas['bg'] = "black"
        self.canvas.pack (expand = True, fill = BOTH)
        self.frame_input.grid (row = 0, column = 1, sticky=N+S+E+W)
        desenhos.canvas = self.canvas
        p =desenhos.plot_point(250,250)
        desenhos.plot_segment(0,0,250,250)
        desenhos.plot_disc(300, 300, 100)
        desenhos.plot_vert_line(400)
        desenhos.plot_horiz_line(600, cor = "green")
        desenhos.change_point_color(p, "blue")
        
        
        # Frame com os arquivos
        self.frame_arquivos = Frame(self.main_frame,bg = cor_fundo)
        self.cria_abas ()
        self.frame_arquivos.grid (row = 0, column = 2, padx = 20, pady = 20, sticky = N)
        
    def cria_botoes (self):
        " Popula o self.frame_botoes com os botões dos problemas "
        for i in range(len(problemas)):
            # Cria o botão
            b = Button (self.frame_botoes, text = problemas[i][0])
            b['command'] = lambda arg = i: self.abre_tela (arg)
            b['relief'] = "ridge"
            b['bg'] = cor_botao
            b['activebackground'] = cor_botao
            b['width'] = 25
            b['height'] = 2
            b.pack (pady = (4, 0))
            
    def cria_abas (self):
        " Configura o self.frame_arquivos com as abas e os arquivos "
        # Configura o estilo das abas
        ttk.Style().configure ("TNotebook", background = cor_fundo);
        ttk.Style().configure("TNotebook.Tab", background=cor_botao, padding = (5, 10));
        self.abas = ttk.Notebook (self.frame_arquivos, height = 300)
        # Adiciona uma aba pra cada tipo de input
        for tipo in self.tipos_input:
            aba = Frame (self.abas)
            arquivos = Listbox (aba, height = 200)
            i = 0
            # Popula cada aba
            for arq in os.listdir(tipo[1]):
                arquivos.insert(i, arq)
                i += 1
            arquivos.bind('<<ListboxSelect>>', self.abre_arquivo)
            # Adiciona o scroll
            sb = Scrollbar (aba, orient = 'vertical')      
            sb.config (command = arquivos.yview)
            sb.pack(side = RIGHT, fill = Y)
            arquivos.config (yscrollcommand = sb.set)
            # Adiciona tudo na aba
            arquivos.pack (fill = BOTH)
            aba.pack(fill = BOTH)
            self.abas.add (aba, text = tipo[0], padding = 5)
        self.abas.pack()
    
            
    def abre_tela (self, i):
        " Recebe o índice do problema e transforma a tela inicial "
        " para mostrar os botões dos algoritmos correspondentes ao problema "
        self.frame_botoes.grid_forget()
        novos_botoes = Frame (self.main_frame, bg = cor_fundo)
        # Cria um botão pra cada algoritmo
        for alg in algoritmos[i]:
            # Cria o botão
            b = Button (novos_botoes, text = alg[1])
            #b['command'] = lambda arg = i, arg2 = b: self.abre_tela (arg, arg2)
            b['relief'] = "ridge"
            b['bg'] = cor_botao
            b['activebackground'] = cor_botao
            b['width'] = 25
            b['height'] = 2
            b.pack (pady = (4, 0))
        # Cria um botão de voltar
        b = Button (novos_botoes, text = "Voltar")
        b['command'] = lambda arg = novos_botoes: self.voltar (novos_botoes)
        b['relief'] = "ridge"
        b['bg'] = cor_botao
        b['activebackground'] = cor_botao
        b['width'] = 25
        b['height'] = 2
        b.pack (pady = (4, 0))
        
        self.abas.select(i)
        # Deixa o primeiro item pré selecionado
        self.abas.winfo_children()[i].winfo_children()[0].select_set(0)
        self.get_plot_input (i, self.abas.winfo_children()[i].winfo_children()[0].get(0))
        novos_botoes.grid (row = 0, column = 0, padx = 20, pady = 20, sticky = N)
        
    def voltar (self, frame_atual):
        " Função para o botão voltar, retorna o self.frame_botoes para o estado inicial "
        frame_atual.grid_forget()
        self.frame_botoes.grid (row = 0, column = 0, padx = 20, pady = 20, sticky = N)
    
    def abre_arquivo (self, evento):
        " Trata o evento de seleção do arquivo na listbox "
        try:
            lista = evento.widget
            index = int(lista.curselection()[0])
            arq = lista.get (index)
            tipo = self.abas.index(self.abas.select())
            self.get_plot_input(tipo, arq)
        except:
            # Erro quando troca de aba
            pass
    
    def get_plot_input (self, tipo, arq):
        " Salva o objeto correspondente ao arquivo arq no self.input "
        " E desenha ele no canvas "
        f = open(self.tipos_input[tipo][1] + "/" + arq, "r")
        self.input = []
        desenhos.clear()
        # Pontos
        if tipo == 0:
            for p in f:
                x, y = float(p.split()[0]), float(p.split()[1])
                p = Point(x, y)
                p.plot()
                self.input.append (p)
        # Poligono
        elif tipo == 1:
            vertices = []
            for p in f:
                x, y = float(p.split()[0]), float(p.split()[1])
                vertices.append (Point(x, y))
            self.input = Polygon (vertices)
        # Segmentos
        elif tipo == 2:
            for p in f:
                x1, y1 = float(p.split()[0]), float(p.split()[1])
                x2, y2 = float(p.split()[2]), float(p.split()[3])
                self.input.append (Segment(Point(x1, y1), Point(x2, y2)))
        # Círculos
        elif tipo == 3:
            for p in f:
                x, y, r = float(p.split()[0]), float(p.split()[1]), float(p.split()[2])
                self.input.append (Disc(x, y, r))
        
Home = Home()
Home.tk.mainloop()

#desenhos.plot_point(250,250)