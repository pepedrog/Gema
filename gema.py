# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import Grid
from tkinter import ttk

# Listas dos problemas e algoritmos para fazer os botões
from itens import problemas, algoritmos, tipos_input

# Classes dos objetos, para ler os arquivos
from estruturas.point import Point
from estruturas.polygon import Polygon
from estruturas.segment import Segment
from estruturas.disc import Disc

import os
import sys
import desenhos
import aleatorios
from PIL import ImageTk, Image

from gema_animacao import anima_gema, pula_gema

cor_botao = "snow"
cor_fundo = "orange"

class Gema ():
    " Classe da aplicação principal, cuida de toda manipulação dos widgets "
    
    def __init__ (self):
        # Cria a tela
        self.tk = Tk()
        self.tk.title ("GEMA")
        self.tk.resizable (0, 0)
        self.tk.geometry('+%d+%d' %(0, 0))

        self.delay = IntVar()
        self.passo_a_passo = IntVar()
        self.passo_a_passo.set(0)
        self.novo_passo = IntVar()
        self.novo_passo.set(1)
        self.esta_rodando = False
        self.tk.bind('<space>', (lambda x=1: self.novo_passo.set(x)))
        
        # Cria todos os widgets da parte gráfica
        self.cria_frames()
        self.popula_frames()
    
        # Sincroniza o canvas com as funções gráficas
        desenhos.canvas = self.canvas
        desenhos.master = self
        
        self.roda_logo(None)
        self.delay.set (200)
        self.tk.protocol("WM_DELETE_WINDOW", self.sair)       

    def roda_logo (self, event):
        # Bloqueia os botoes
        desenhos.clear ()
        self.b_sair['text'] = 'Pular'
        self.b_sair['command'] = pula_gema
        
        for w in self.frame_botoes.winfo_children():
            if type (w) == Button: w.configure (state = DISABLED)
        anima_gema(self.delay)
        for w in self.frame_botoes.winfo_children():
            w.configure (state = NORMAL)
        self.rodei_logo = True
        self.delay.set (200)
        self.b_sair['text'] = 'Sair'
        self.b_sair['command'] = self.sair
    
    def cria_frames (self):
        " Cria todos os objetos Frame e posiciona no Grid "
        # Frame principal que contem todos os outros
        self.main_frame = Frame (self.tk, bg = cor_fundo)
        self.main_frame.pack(fill = BOTH, expand = True)
        Grid.columnconfigure(self.main_frame, 1, weight=1)
        Grid.rowconfigure(self.main_frame, 0, weight=1)
        
        # Frame com os botoes do lado esquerdo
        self.frame_botoes_geral = Frame (self.main_frame, bg = cor_fundo)
        self.frame_botoes_geral.grid (row = 0, column = 0, padx = 20, pady = 20, sticky = NS)
        
        # Frame com o logo e os botões pros problemas        
        self.frame_botoes = Frame (self.frame_botoes_geral, bg = cor_fundo)
        self.frame_botoes.pack (side = TOP)
        
        # Frame com o canvas
        self.frame_canvas = Frame (self.main_frame,pady = 20, bg = cor_fundo)
        self.frame_canvas.grid (row = 0, column = 1, sticky=N+S+E+W)
        
        # Frame com os arquivos
        self.frame_arquivos = Frame(self.main_frame,bg = cor_fundo)
        self.frame_arquivos.grid (row = 0, column = 2, padx = 20, pady = 20, sticky = N)
        
    def popula_frames (self):
        " Coloca os widgets nos frames (Botões + Canvas + Lista de Arquivos)"
        # Botões
        self.img = Image.open('gema.png')
        self.img = self.img.resize ((100, 100),Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage (self.img)
        img_lbl = Label (self.frame_botoes, image = self.img, width = 100, height = 100,
                         relief="groove", borderwidth = 0)
        img_lbl.bind ("<Button-1>", self.roda_logo)
        img_lbl.pack (pady = 10)
        self.cria_botoes()
        self.b_sair = Button (self.frame_botoes_geral, text = 'Sair', command = self.sair)
        self.b_sair['relief'] = "ridge"
        self.b_sair['bg'] = cor_botao
        self.b_sair['height'] = 2
        self.b_sair.pack (side = BOTTOM, fill = X)
        delay = Scale (self.frame_botoes_geral, orient = HORIZONTAL, 
                       from_ = 1, to = 500, resolution = 1, showvalue = 0, 
                       bg = cor_fundo, highlightbackground = cor_fundo, 
                       troughcolor = cor_botao, label = 'Delay', variable = self.delay)
        delay.pack(side = BOTTOM, fill = X, pady = (0,4))
        cb = Checkbutton(self.frame_botoes_geral, 
                         text = 'passo a passo', variable = self.passo_a_passo)
        cb['bg'] = cor_botao
        cb['height'] = 2
        cb['relief'] = "ridge"
        cb.pack(side = BOTTOM, fill = X, pady = (0, 4))
        
        # Canvas
        self.canvas = Canvas (self.frame_canvas, width = 600, height = 600)
        self.canvas['bg'] = "black"
        self.canvas.pack (expand = False)
        
        # Arquivos
        self.cria_abas ()
        frame_aleatorio = Frame (self.frame_arquivos, bg = cor_fundo)
        b_novo_input = Button (frame_aleatorio, text = "Input Aleatório")
        b_novo_input['command'] = self.input_aleatorio
        b_novo_input['relief'] = "ridge"
        b_novo_input['bg'] = cor_botao
        b_novo_input['height'] = 2
        b_novo_input['width'] = 24
        b_novo_input.pack (pady = (10, 0), side = LEFT)
        self.n_rand = Entry (frame_aleatorio, width = 7, justify = 'center')
        self.n_rand.insert(END, '16')
        self.n_rand.pack(ipady = 5, pady = (10, 0), side = RIGHT)
        frame_aleatorio.pack(fill = X)
        
        frame_grava = Frame (self.frame_arquivos, bg = cor_fundo)
        b_grava_input = Button (frame_grava, text = "Gravar Input")
        b_grava_input['command'] = self.grava_input
        b_grava_input['relief'] = "ridge"
        b_grava_input['bg'] = cor_botao
        b_grava_input['height'] = 2
        b_grava_input['width'] = 11
        b_grava_input.pack (pady = (10, 0), side = LEFT)
        self.novo_input = Entry (frame_grava, width = 20, justify = 'center')
        self.novo_input.insert(0, 'nome do arquivo')
        self.novo_input.pack(ipady = 5, pady = (10, 0), side = RIGHT)
        frame_grava.pack(fill = X)
        
    def cria_botoes (self):
        " Popula o self.frame_botoes com os botões dos problemas "
        for i in range(len(problemas)):
            # Cria o botão
            b = Button (self.frame_botoes, text = problemas[i][0])
            b['command'] = lambda arg = i: self.abre_tela (arg)
            b['relief'] = "ridge"
            b['bg'] = cor_botao
            b['width'] = 25
            b['height'] = 2
            b.pack (pady = (2, 0))
            
    def cria_abas (self):
        " Configura o self.frame_arquivos com as abas e os arquivos "
        # Configura o estilo das abas
        ttk.Style().configure ("TNotebook", background = cor_fundo)
        ttk.Style().configure ("TNotebook.Tab", background=cor_botao, padding = (5, 10))
        self.abas = ttk.Notebook (self.frame_arquivos, height = 300)
        # Adiciona uma aba pra cada tipo de input
        for tipo in tipos_input:
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
        " para mostrar os botões dos algoritmos correspondentes ao problema i "
        self.frame_botoes.pack_forget()
        self.novos_botoes = Frame (self.frame_botoes_geral, bg = cor_fundo)
        j = 0
        # Cria um botão pra cada algoritmo
        for alg in algoritmos[i]:
            # Cria o label pro botao
            l = Label (self.novos_botoes, text = "0", width = 3)
            # Cria o botão
            b = Button (self.novos_botoes, text = alg[1])
            b['command'] = lambda a1 = alg, a2 = i, a3 = l: self.roda_algoritmo (a1, a2, a3)
            b['relief'] = "ridge"
            b['bg'] = cor_botao
            b['width'] = 20
            b['height'] = 2
            b.grid (row = j, column = 0)
            l.grid (row = j, column = 1, padx = (5, 0))
            j += 1
            
        self.b_sair['text'] = "Voltar"
        self.b_sair['command'] = self.voltar
        
        tipo = problemas[i][2]
        # Coloca na aba de input certa
        if self.abas.index('current') != tipo or self.rodei_logo: 
            self.abas.select(tipo)
            # Deixa o primeiro item pré selecionado
            self.abas.winfo_children()[tipo].winfo_children()[0].select_set(2)
            self.get_plot_input (tipo, self.abas.winfo_children()[tipo].winfo_children()[0].get(2))
        self.novos_botoes.pack (side = TOP)
        
    def voltar (self):
        " Função para o botão voltar, retorna o self.frame_botoes para o estado inicial "
        self.novos_botoes.pack_forget()
        self.frame_botoes.pack (side = TOP)
        self.b_sair['text'] = "Sair"
        self.b_sair['command'] = self.sair
    
    def sair (self):
        " Função para o botão sair "
        self.novo_passo.set (1)
        self.tk.destroy()
    
    def abre_arquivo (self, evento):
        " Trata o evento de seleção do arquivo na listbox "
        try:
            if not self.esta_rodando:
                lista = evento.widget
                index = int(lista.curselection()[0])
                arq = lista.get (index)
                tipo = self.abas.index('current')
                self.get_plot_input(tipo, arq)
        except:
            pass # Quando troca de aba
    
    def get_plot_input (self, tipo, arq):
        " Salva o objeto correspondente ao arquivo arq no self.input "
        " E desenha ele no canvas "
        self.rodei_logo = False
        f = open(tipos_input[tipo][1] + "/" + arq, "r")
        self.input = []
        self.novo_input.delete(0, END)
        self.novo_input.insert(0, arq)
        desenhos.clear()
        # Pontos
        if tipo == 0:
            for p in f:
                x, y = float(p.split()[0]), float(p.split()[1])
                self.input.append (Point(x, y))
        # Poligono
        elif tipo == 1:
            vertices = []
            for p in f:
                x, y = float(p.split()[0]), float(p.split()[1])
                vertices.append (Point(x, y))
            p =  Polygon (vertices)
            self.input = p
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
        self.plot_input()
        
    def input_aleatorio (self):
        " Função que trata o clique do botão 'Input Aleatorio' "
        self.rodei_logo = False
        desenhos.clear()
        self.main_frame.update()
        tipo = self.abas.index('current')
        try:
            n = int(self.n_rand.get())
        except:
            n = 50
            self.n_rand.delete (0, END)
            self.n_rand.insert (0, '16')
        self.input = aleatorios.input_aleatorio (tipo, n, self.canvas.winfo_width(),
                                                 self.canvas.winfo_height())
        self.plot_input()
        self.novo_input.delete (0, END)
        self.novo_input.insert (0, "aleatorio_%04d" % n)
    
    def grava_input (self):
        " Função que trata o clique do botão 'Gravar Input' "
        " Escrevendo o self.input num arquivo de nome "
        arq = self.novo_input.get()
        tipo = self.abas.index('current')
        try:
            f = open(tipos_input[tipo][1] + "/" + arq, "x")
            novo = True
        except:
            f = open(tipos_input[tipo][1] + "/" + arq, "w")
            novo = False
        if tipo == 0:
            for p in self.input:
                f.write ('%f %f\n' % (p.x, p.y))
        elif tipo == 1:
            for p in self.input.vertices():
                f.write ('%f %f\n' % (p.x, p.y))
        elif tipo == 2:
            for s in self.input:
                f.write ('%f %f %f %f\n' % (s.init.x, s.init.y, s.to.x, s.to.y))
        elif tipo == 3:
            for c in self.input:
                f.write ('%f %f %f\n' % (c.center.x, c.center.y, c.r))
                
        f.close()
        if novo:
            self.abas.winfo_children()[tipo].winfo_children()[0].insert (10000, arq)  
    
    def plot_input(self):
        desenhos.clear()
        try: 
            self.input.plot()
        except: 
            for p in self.input: p.plot()
    
    def roda_algoritmo (self, alg, prob, lbl):
        # Desabilita os frames enquanto roda o algoritmo
        self.esta_rodando = True
        for w in self.frame_botoes_geral.winfo_children ():
            if w.winfo_children:
                for b in w.winfo_children ():
                    b.configure (state = DISABLED)
        self.b_sair['text'] = 'Cancelar'
        self.b_sair['command'] = desenhos.cancela

        desenhos.num_sleeps = 0
        self.plot_input()
        
        cmd = ("__import__('algoritmos." + problemas[prob][1] + '.' + alg[0] +
               "', fromlist=['object'])." + alg[2] + "(self.input)")
        try: exec(cmd)
        except desenhos.InterruptAlg: # Cancela a execução 
            self.plot_input()
            desenhos.cancel = False
        except Exception as e:
            print("ERRO: " + str(e))
            self.plot_input()
        
        
        # Retorna os frames para o estado original
        self.esta_rodando = False
        for w in self.frame_botoes_geral.winfo_children():
            if w.winfo_children:
                for b in w.winfo_children():
                    b.configure (state = NORMAL)
        self.b_sair.configure (state = NORMAL)
        
        lbl['text'] = str (desenhos.num_sleeps)
        self.b_sair['text'] = "Voltar"
        self.b_sair['command'] = self.voltar

if len(sys.argv) > 2:
    pula_gema()
Home = Gema()
Home.tk.mainloop()
