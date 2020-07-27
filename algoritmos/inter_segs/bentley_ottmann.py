from estruturas.point import Point
from estruturas.abbb import Abbb
from estruturas.prim import left, area2
import desenhos

# Precisão pro ponto flutuante
eps = 1e-7

class Node_Point:
    " Classe que será nosso nó na ABBB de pontos-eventos "  
    " guarda um ponto e os segmentos que ele pertence "
    def __init__ (self, ponto, ini, fim, inter):
        self.ponto = ponto
        self.ini = ini # lista dos segmentos que esse ponto é o ponto da esquerda
        self.fim = fim # lista dos segmentos que esse ponto é o ponto da direita
        self.inter = inter # lista dos segmentos que esse ponto é de um ponto de interseção
        
    def __eq__ (self, other):
        return other is not None and self.ponto.approx_equals (other.ponto)
    
    # Ordem que usaremos na ABBB, da esquerda pra direita, de baixo pra cima    
    def __gt__ (self, other):
        return (self.ponto.x - other.ponto.x > eps or
                (abs(self.ponto.x - other.ponto.x) < eps and self.ponto.y - other.ponto.y > eps))
    
    def __str__(self):
        return str(self.ponto)
    
class Node_Seg:
    " Classe que será o nó na nossa ABBB da linha de varredura "
    " Guarda um segmento e seu ponto de referencia"
    def __init__(self, seg, ref):
        self.seg = seg
        self.ref = ref # Ponto de referência para percorrer a abbb
            
    def __eq__ (self, other):
        return other != None and self.seg == other.seg
    
    # Ordem que usaremos na linha de varredura    
    def __gt__ (self, other):
        ref = other.ref
        # Se o ponto de referencia é uma interseção, 
        if abs(area2 (self.seg.init, self.seg.to, ref)) < eps:
            # O ponto de referência vai ser o ponto da direita
            ref = other.seg.to
        # Self > other <=> other está a esquerda do self
        return left (self.seg.init, self.seg.to, ref)
    
    def __str__ (self):
        return str(self.seg) + " " + str (self.ref)

def eventos (segmentos):
    "Função que retorna uma ABBB de pontos-eventos, que são os extremos horizontais dos circulos"
    Q = Abbb () # Abbb dos pontos eventos
    for s in segmentos:
        if s.init.x > s.to.x or (s.init.x == s.to.x and s.init.y > s.to.y):
           s.init, s.to = s.to, s.init
        no_seg = Node_Seg (s, s.init)
        p1 = Node_Point (s.init, ini = [no_seg], fim = [], inter = [])
        p2 = Node_Point (s.to, ini = [], fim = [no_seg], inter = [])
        no1 = Q.busca (p1)
        no2 = Q.busca (p2)
        # Se os pontos já estão inseridos, só atualiza, se não, insere
        if no1.elemento != None:  
            no1.elemento.ini.append (no_seg)
        else:
            Q.insere (p1)
            p1.ponto.plot ('red')
        if no2.elemento != None:
            no2.elemento.fim.append (no_seg)
        else:
            Q.insere (p2)
            p2.ponto.plot ('red')
        
    return Q

def marca_intersec (no1, no2, pontos, p_x = None):
    "Testa se há interseção entre o nó1 e o nó2 e adiciona em pontos, se houver"
    "E só marca as interseções que ocorrem do p_x pra direita"
    # Despinta de verde e pinta de amarelo
    no1.seg.hide()
    no2.seg.hide()
    no1.seg.plot ('yellow')
    no2.seg.plot ('yellow')
    desenhos.sleep()
    # despinta de amarelo e pinta de verde denovo
    no1.seg.hide()
    no2.seg.hide()
    no1.seg.plot ('green')
    no2.seg.plot ('green')
    
    p = no1.seg.intersection (no2.seg)
    # Só marco se o o ponto esta pra frente do x especificado
    if (p != None and (p_x == None or p.x > p_x.x or (p.x == p_x.x and p.y > p_x.y))):
        # Crio o nó
        p_no = Node_Point (p, ini = [], fim = [], inter = [no1, no2])
        # insere o ponto na arvore, ou só atualiza se ele já existir
        p_no_abb = pontos.busca (p_no)
        if p_no_abb.elemento == None:
            pontos.insere (p_no)
            p_no.ponto.plot('red') 
        else:
            if no1 not in p_no_abb.elemento.inter:
                p_no_abb.elemento.inter.append (no1)
            if no2 not in p_no_abb.elemento.inter:
                p_no_abb.elemento.inter.append (no2)
    desenhos.sleep()
    
def insere_na_linha (L, no, pontos, p_x = None, trocados = []):
    "Insere o nó na linha de varredura L e testa as interseções com consecutivos "
    "Mas só marca as interseções que ocorrem do x pra frente e que não se repetem nos trocados"
    L.insere (no)
    pred = L.predecessor (no)
    suc = L.sucessor (no)
    if pred != None and (trocados == [] or pred not in trocados):
        marca_intersec (no, pred, pontos, p_x)
    if suc != None and (trocados == [] or suc not in trocados):
        marca_intersec (no, suc, pontos, p_x)
    
def deleta_da_linha (L, no, pontos, p_x = None):
    "Deleta o nó da linha de varredura L e testa a interseção entre os que ficaram consecutivos"
    "Mas só marca as interseções que ocorrem do x pra frente"
    pred = L.predecessor (no)
    suc = L.sucessor (no)
    L.deleta (no)
    no.seg.hide()
    desenhos.sleep()
    if pred != None and suc != None and pred != suc:
        marca_intersec (pred, suc, pontos, p_x)

def bentley_ottmann (l):
    L = Abbb () # Linha de varredura
    resp = [] # Os nós com os pontos de interseção que retornaremos
    # Pré-processamento - Transforma cada circulo em pontos-eventos
    # pontos é a ABBB de pontos eventos
    pontos = eventos (l)
    desenhos.sleep()
    
    while not pontos.vazia():
        p = pontos.deleta_min()
        # desenha a linha
        id_linha = desenhos.plot_vert_line (p.ponto.x, 'green')
        id_evento = p.ponto.hilight('green')
        desenhos.sleep()
        
        "------------------------- Pontos da direita --------------------------------"
        for seg in p.fim:
            seg.ref = seg.seg.to
            deleta_da_linha (L, seg, pontos, p.ponto)
            
        "------------------------- Pontos da esquerda --------------------------------"
        for seg in p.ini:
            seg.seg.plot ('green')
            desenhos.sleep()
            insere_na_linha (L, seg, pontos)
         
        "------------------------- Pontos de interseção ------------------------------"
        if len (p.inter) > 0 or (len (p.ini) + len (p.fim)) > 1:
            p.ponto.hilight('yellow')
            resp.append (p)
            
        # Troca a ordem dos segmentos (do p.inter[])
        trocados = []
        # Remove todos
        for seg in p.inter:
            if seg not in p.fim:
                if seg.seg.to.x != seg.seg.init.x:
                    y_ref = (((seg.seg.to.x*seg.seg.init.y) - (seg.seg.init.x*seg.seg.to.y) -
                              (p.ponto.x - 10*eps)*(seg.seg.init.y - seg.seg.to.y)) / 
                              (seg.seg.to.x - seg.seg.init.x))
                    seg.ref = Point (p.ponto.x - 10*eps, y_ref)
                else:
                    seg.ref = Point (p.ponto.x, p.ponto.y + 10*eps)
                trocados.append (seg)
                L.deleta (seg)
        # Insere denovo com o novo ponto de referencia
        for seg in trocados:
            seg.ref = p.ponto
            #print("reinserindo " + str(seg))
            insere_na_linha (L, seg, pontos, p.ponto, trocados)
            
        # apaga a linha
        desenhos.plot_delete (id_linha)
        desenhos.plot_delete (id_evento)
        p.ponto.unplot()

    return resp