# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import Grid
from tkinter import ttk
import os
from itens import problemas, algoritmos
#from PIL import ImageTk, Image

cor_botao = "snow"
cor_fundo = "orange"

class Home ():
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
        self.canvas = Canvas (self.frame_input, width = 500, height = 500)
        self.canvas['bg'] = "black"
        self.canvas.pack (expand = True, fill = BOTH)
        self.frame_input.grid (row = 0, column = 1, sticky=N+S+E+W)
        
        # Frame com os arquivos
        self.frame_arquivos = Frame(self.main_frame,bg = cor_fundo)
        self.cria_abas ()
        self.frame_arquivos.grid (row = 0, column = 2, padx = 20, pady = 20, sticky = N)
    
    def cria_botoes (self):   
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
        # Recebe um botão b e o índice do problema e transforma a 
        # tela inicial para rodar os algoritmos correspondentes ao problema
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
        
        self.abas.select(problemas[i][2])
        # Deixa o primeiro item pré selecionado
        self.abas.winfo_children()[index].winfo_children()[0].select_set(0)
        self.desenha_arquivo (problemas[i][2] + "/" +
                              self.abas.winfo_children()[index].winfo_children()[0].get(0))
        novos_botoes.grid (row = 0, column = 0, padx = 20, pady = 20, sticky = N)
        
    def voltar (self, frame_atual):
        # Função que retorna para a tela inicial
        frame_atual.grid_forget()
        self.frame_botoes.grid (row = 0, column = 0, padx = 20, pady = 20, sticky = N)
    
    def abre_arquivo (self, evento):
        # Trata o evento de seleção do arquivo na listbox
        try:
            lista = evento.widget
            index = int(lista.curselection()[0])
            arq = lista.get (index)
            pasta = self.tipos_input[self.abas.index(self.abas.select())][1]
            self.desenha_arquivo (pasta + "/" + arq)
        except:
            # Erro quando troca de aba
            pass
    
    def desenha_arquivo (self, arq):
        print(arq)

Home = Home()
Home.tk.mainloop()