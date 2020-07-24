from estruturas.point import Point
from estruturas.abbb import Abbb
import desenhos

# Precisão pro ponto flutuante
eps = 1e-7

class Node_Point_Circle:
    " Classe que será nosso nó na ABBB de pontos-eventos "  
    " guarda um ponto e os circulos que ele pertence "
    def __init__ (self, ponto, ini, fim, inter, inter_unico):
        self.ponto = ponto
        self.ini = ini # lista dos circulos que esse ponto é o ponto da esquerda
        self.fim = fim # lista dos circulos que esse ponto é o ponto da direita
        self.inter = inter # lista dos circulos que esse ponto é de um ponto de interseção
        self.inter_unico = inter_unico # Lista dos circulos que esse ponto é o unico ponto de interseção
    
    def __eq__ (self, other):
        return other != None and self.ponto.approx_equals (other.ponto)
    
    # Ordem que usaremos na ABBB, da esquerda pra direita, de baixo pra cima    
    def __gt__ (self, other):
        return (self.ponto.x - other.ponto.x > eps or
                (abs(self.ponto.x - other.ponto.x) < eps and self.ponto.y - other.ponto.y > eps))
    
    def __str__ (self):
        i = [str(x) for x in self.ini]
        inter = [str(x) for x in self.inter]
        interu = [str(x) for x in self.inter_unico]
        f = [str(x) for x in self.fim]
        return str(self.ponto)
        #return (str(self.ponto) + '\nini: ' + str(i) + '\ninter: ' + 
        #       str(inter) + '\ninter_uico: ' + str(interu) +
        #       '\nfim: ' + str(f))
    
class Node_Semi_Circle:
    " Classe que será o nó na nossa ABBB da linha de varredura "
    " Guarda um arco que é a metade de cima ou de baixo de um circulo"
    def __init__(self, circ, baixo, ref):
        self.circ = circ
        self.baixo = baixo # Booleano, representa qual metade do circulo é
        self.ref = ref # Ponto de referência para percorrer a abbb
    
    def desenha (self, cor = "green"):
        " Desenha o arco na tela "
        self.circ.hilight_semi_circle (not self.baixo, cor = cor, grossura = 3)
        
    def apaga (self):
        " Apaga o arco da tela "
        self.circ.unhilight_semi_circle (not self.baixo)
        
    def esquerda (self, p, baixo):
        " Retorna se o ponto p está a esquerda do arco"
        " baixo é o criterio de desempate, diz se o ponto 'está indo' pra baixo ou pra cima"
        # caso onde o ponto está dentro do circulo
        if  (p.x - self.circ.center.x)**2 + (p.y - self.circ.center.y)**2 - self.circ.r**2 <= eps:
            #só esta a esquerda se eu for o arco de baixo
            return self.baixo
        # caso onde o ponto está fora do circulo
        else:
            # Caso particular: o ponto está bem na linha do equador do semi circulo,
            # desempoatamos pelo contexto do ponto
            if abs (p.y - self.circ.center.y) < eps:
                return self.baixo 
                #return not baixo
            return p.y > self.circ.center.y
    
    def __str__ (self):
        " Para debugar "
        return str(self.circ) + ' -- ' + str(self.baixo) + ' -- ' + str(self.ref)
            
    def __eq__ (self, other):
        return other != None and self.circ == other.circ and self.baixo == other.baixo
    
    # Ordem que usaremos na linha de varredura    
    def __gt__ (self, other):
        if self.circ == other.circ:
            return self.baixo and not other.baixo
        ref = other.ref
        x = self.circ.center.x
        y = self.circ.center.y
        
        # Se o ponto de referencia é uma interseção, 
        if abs((ref.x - x)**2 + (ref.y - y)**2 - self.circ.r**2) < eps:
            # então eu pego um ponto um pouco posterior pra ser o ponto de refencia, 
            # aplicando a formula do circulo pra 2*epsilon pra frente
            if other.baixo:
                sinal = -1
            else:
                sinal = 1
            # Formula do circulo
            x_novo = ref.x + 2*eps
            x_novo = min (x_novo, other.circ.center.x + other.circ.r)
            y_novo = other.circ.center.y
            y_novo += sinal*(other.circ.r**2 - (x_novo - other.circ.center.x)**2)**0.5
         
            ref = Point (x_novo, y_novo)
            
        # Self > other <=> other está a esquerda do self
        return self.esquerda (ref, other.baixo)
    
def eventos (circulos):
    "Função que retorna uma ABBB de pontos-eventos, que são os extremos horizontais dos circulos"
    Q = Abbb () # Abbb dos pontos eventos
    for c in circulos:
        p_esq = c.center - Point (c.r, 0)
        p_dir = c.center + Point (c.r, 0)
        baixo = Node_Semi_Circle (c, True, p_esq)
        cima = Node_Semi_Circle (c, False, p_esq)
        p1 = Node_Point_Circle (p_esq, ini = [baixo, cima], fim = [], inter = [], inter_unico = [])
        p2 = Node_Point_Circle (p_dir, ini = [], fim = [baixo, cima], inter = [], inter_unico = [])
        no1 = Q.busca (p1)
        no2 = Q.busca (p2)
        # Se os pontos já estão inseridos, só atualiza, se não, insere
        if no1.elemento != None:  
            no1.elemento.ini.append (baixo)
            no1.elemento.ini.append (cima)
        else:
            Q.insere (p1)
            p_esq.plot ('red')
            no1 = Q.busca (p1)
        if no2.elemento != None:
            no2.elemento.fim.append (baixo)
            no2.elemento.fim.append (cima)
        else:
            Q.insere (p2)
            p_dir.plot ('red')
        
    return Q

def marca_intersec (no1, no2, pontos, x = None):
    "Testa se há interseções entre o nó 1 e o nó 2 e adiciona em pontos, se houver"
    "E só marca as interseções que ocorrem do x pra direita"
    # Despinta de verde e pinta de amarelo
    no1.apaga()
    no2.apaga()
    no1.desenha ("yellow")
    no2.desenha ("yellow")
    desenhos.sleep()
    # despinta de amarelo e pinta de verde denovo
    no1.apaga()
    no2.apaga()
    no1.desenha()
    no2.desenha()
    
    inter = no1.circ.intersection (no2.circ)
    for p in inter:
        # Só marco se o o ponto esta pra frente do x especificado
        # e se faz parte das metades correspondentes 
        #(se intersecta a metade de cima e eu sou a de baixo eu não marco)
        if ((x == None or p.x > x) and
            ((no1.baixo and p.y <= no1.circ.center.y) or (not no1.baixo and p.y >= no1.circ.center.y)) and 
            ((no2.baixo and p.y <= no2.circ.center.y) or (not no2.baixo and p.y >= no2.circ.center.y))):
            # Crio o nó
            # Caso degenerado onde os arcos se intersectam em 1 só ponto, que eu guardo no inter_unico[]
            if len (inter) == 1:
                p_no = Node_Point_Circle (p, ini = [], fim = [], inter = [], inter_unico = [no1, no2])
            # caso geral onde os arcos se intersectam em 2 pontos
            else:
                p_no = Node_Point_Circle (p, ini = [], fim = [], inter = [no1, no2], inter_unico = [])
                
            # insere o nó na linha, ou só atualiza se ele já existir
            p_no_abb = pontos.busca (p_no)
            if p_no_abb.elemento == None:
                pontos.insere (p_no)
                p_no.ponto.plot('red') 
            else:
                if len (inter) == 1:
                    p_no_abb.elemento.inter_unico.append (no1)
                    p_no_abb.elemento.inter_unico.append (no2)
                else:
                    p_no_abb.elemento.inter.append (no1)
                    p_no_abb.elemento.inter.append (no2)
    desenhos.sleep()
    
def insere_na_linha (L, no, pontos, x = None, trocados = []):
    "Insere o nó na linha de varredura L e testa as interseções com consecutivos "
    "Mas só marca as interseções que ocorrem do x pra frente e que não se repetem nos trocados"
    print("vou inserir o "+str(no))
    L.insere (no)
    L.printa_arvore()
    if x == None:
        no.desenha()
        desenhos.sleep()
    pred = L.predecessor (no)
    suc = L.sucessor (no)

    if pred != None and (trocados == [] or pred not in trocados):
        marca_intersec (no, pred, pontos, x)
    if suc != None and (trocados == [] or suc not in trocados):
        marca_intersec (no, suc, pontos, x)
    
def deleta_da_linha (L, no, pontos, x = None):
    "Deleta o nó da linha de varredura L e testa a interseção entre os que ficaram consecutivos"
    "Mas só marca as interseções que ocorrem do x pra frente"
    print("vou deletar o "+str(no))
    pred = L.predecessor (no)
    suc = L.sucessor (no)
    L.deleta (no)
    L.printa_arvore()
    no.apaga()
    desenhos.sleep()
    if pred != None and suc != None:
        marca_intersec (pred, suc, pontos, x)

def bentley_ottmann_mod (l):
    L = Abbb () # Linha de varredura
    resp = [] # Os nós com os pontos de interseção que retornaremos
    # Pré-processamento - Transforma cada circulo em pontos-eventos
    # pontos é a ABBB de pontos eventos
    pontos = eventos (l)
    desenhos.sleep()
    
    while not pontos.vazia():
        p = pontos.deleta_min()
        print("---------------------------------- P = " + str(p))
        # desenha a linha
        id_linha = desenhos.plot_vert_line (p.ponto.x, 'green')
        id_evento = p.ponto.hilight('green')
        desenhos.sleep()
        "------------------------- Pontos da esquerda --------------------------------"
        for arco in p.ini:
            insere_na_linha (L, arco, pontos)
            
        "------------------------- Pontos de interseção ------------------------------"
        if len (p.inter) > 0 or len (p.inter_unico) > 0:
            p.ponto.hilight('yellow')
            resp.append (p)
            
        # Troca a ordem dos arcos (do p.inter[])
        # (Não troco a ordem do p.inter_unico[] porque os circulos não se "penetram")
        trocados = []
        # Remove todos
        for arco in p.inter:
            if p.ponto.x < arco.circ.center.x + arco.circ.r - eps and arco not in trocados:
                trocados.append (arco)
                L.deleta (arco)
        # Insere denovo com o novo ponto de referencia
        for arco in trocados:
            arco.ref = p.ponto
            insere_na_linha (L, arco, pontos, p.ponto.x, trocados)
        
        "------------------------- Pontos da direita --------------------------------"
        for arco in p.fim:
            deleta_da_linha (L, arco, pontos, p.ponto.x)
            
        # apaga a linha
        desenhos.plot_delete (id_linha)    
        desenhos.plot_delete (id_evento)
        p.ponto.unplot()

    return resp
