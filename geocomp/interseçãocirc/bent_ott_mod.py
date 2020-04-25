from geocomp.common.point import Point
from geocomp.common.abbb import Abbb
from geocomp.common import control

eps = 1e-7

class Node_Point_Circle:
    " Classe que será nosso nó na ABBB de pontos-eventos "  
    " guarda um ponto e os circulos que ele pertence "
    def __init__ (self, ponto, ini = [], fim = [], inter = []):
        self.ponto = ponto
        self.ini = ini # lista dos circulos que esse ponto é o ponto da esquerda
        self.fim = fim # lista dos circulos que esse ponto é o ponto da direita
        self.inter = inter # lista dos circulos que esse ponto é de interseção
    
    def __eq__ (self, other):
        return other != None and self.ponto.approx_equals (other.ponto) # Para evitar erro numérico
    
    # Ordem que usaremos na ABBB, da esquerda pra direita, de baixo pra cima    
    def __gt__ (self, other):
        return (self.ponto.x - other.ponto.x > eps or
                (abs(self.ponto.x - other.ponto.x) < eps and self.ponto.y - other.ponto.y > eps))
    
    def __str__ (self):
        return str(self.ponto)# + "\nini = " + str(self.ini) + "\nfim: " + str(self.fim) + "\ninter: " + str(self.inter)
    
class Node_Circle_Half:
    " Classe que será o nó na nossa ABBB da linha de varredura "
    " Guarda um arco que é a metade de cima ou de baixo de um circulo"
    def __init__(self, circ, baixo, ref):
        self.circ = circ
        self.baixo = baixo # Booleano, representa qual metade do circulo é
        self.ref = ref # Ponto de referência para percorrer a abbb
    
    def desenha (self, color = "green"):
        " Desenha o arco na tela "
        self.circ.hilight_semi_circle (not self.baixo, color = color, width = 3)
        
    def apaga (self):
        " Apaga o arco da tela "
        self.circ.unhilight_semi_circle (not self.baixo)
        
    def esquerda (self, p, baixo):
        " Retorna se o ponto p está a esquerda do arco, baixo é o criterio de desempate"
        
        # caso onde o ponto está no dentro do circulo
        if  (p.x - self.circ.center.x)**2 + (p.y - self.circ.center.y)**2 - self.circ.r**2 <= eps:
            #só esta a esqerda se eu for o arco de baixo
            return self.baixo
        # caso onde o ponto está fora do circulo
        else:
            # Caso particular: o ponto está bem na linha do equador do semi circulo,
            # desempoatamos pelo contexto do ponto
            if abs (p.y - self.circ.center.y) < eps:
                return not baixo 
            return p.y > self.circ.center.y
            
    def __eq__ (self, other):
        return other != None and self.circ == other.circ and self.baixo == other.baixo
    
    # Ordem que usaremos na abbb    
    def __gt__ (self, other):
        
        ref = other.ref
        x = self.circ.center.x
        y = self.circ.center.y
        
        # Caso particular, os dois circulos estão horizontalmente lineares
        # Complica muito o teste de esquerda, então tratamos separados aqui
        if self.circ == other.circ:
            return self.baixo and not other.baixo
        
        
        # Se o ponto de referencia é uma interseção, uso o ponto da direita como referencia
        if abs((ref.x - x)**2 + (ref.y - y)**2 - self.circ.r**2) < eps:
            print("Estou reinserindo um ponto de interseção")
            ref = other.circ.center + Point (other.circ.r, 0)
            
        # Self > other <=> other está a esquerda do self
        return self.esquerda (ref, other.baixo)
            
    def __str__(self):
        return str(self.circ) + " " + str(self.baixo)

def eventos (circulos):
    "Função que retorna uma ABBB de pontos-eventos, que são os extremos horizontais dos circulos"
    
    Q = Abbb () # Abbb dos pontos eventos
    
    for c in circulos:
        extremo1 = c.center - Point (c.r, 0)
        extremo2 = c.center + Point (c.r, 0)
        
        baixo = Node_Circle_Half (c, True, extremo1)
        cima = Node_Circle_Half (c, False, extremo1)
        
        p1 = Node_Point_Circle (extremo1, ini = [baixo, cima], fim = [])
        p2 = Node_Point_Circle (extremo2, ini = [], fim = [baixo, cima])
        
        no1 = Q.busca (p1)
        no2 = Q.busca (p2)
        
        # Se os pontos já estão inseridos, só atualiza, se não, insere
        if no1.elemento != None:  
            no1.elemento.ini.append (baixo)
            no1.elemento.ini.append (cima)
        else:
            Q.insere (p1)
            extremo1.plot (color = 'red')
            
        if no2.elemento != None:
            no2.elemento.fim.append (baixo)
            no1.elemento.fim.append (cima)
            
        else:
            Q.insere (p2)
            extremo2.plot (color = 'red')
        
    return Q

def marca_intersec (no1, no2, pontos):
    "Testa se há interseções entre o nó 1 e o nó 2 e adiciona em pontos, se houver"
    
    # Despinta de verde e pinta de amarelo
    no1.apaga()
    no2.apaga()
    no1.desenha ("yellow")
    no2.desenha ("yellow")
    control.sleep()
    # despinta os meio circulos de amarelo e pinta de verde denovo
    no1.apaga()
    no2.apaga()
    no1.desenha()
    no2.desenha()
    
    inter = no1.circ.intersection (no2.circ)
    for p in inter:
        # Só marco se o o ponto faz parte das metades correspondentes
        if (((no1.baixo and p.y <= no1.circ.center.y) or (not no1.baixo and p.y >= no1.circ.center.y)) and 
            ((no2.baixo and p.y <= no2.circ.center.y) or (not no2.baixo and p.y >= no2.circ.center.y))):
            
            # insere o nó na ABBB de pontos ou só atualiza se ele já existir na ABBB
            p_no = Node_Point_Circle (p, ini = [], fim = [], inter = [no1, no2])
            p_no_abb = pontos.busca (p_no)
            
            if p_no_abb.elemento != None:
                p_no_abb.elemento.inter.append (no1)
                p_no_abb.elemento.inter.append (no2)
            else:
                pontos.insere (p_no)
                p_no.ponto.plot('red')    

    control.sleep()
    
def insere_na_linha (L, no, pontos):
    "Insere o nó na linha de varredura L e testa as interseções com consecutivos "
    
    L.insere (no)
    no.desenha()
    control.sleep()
            
    pred = L.predecessor (no)
    suc = L.sucessor (no)

    if pred != None:
        marca_intersec (no, pred, pontos)
    if suc != None:
        marca_intersec (no, suc, pontos)
    
    
    print("depois de inserir " + str(no))
    L.printa_arvore()

def deleta_da_linha (L, no, pontos):
    "deleta o nó da linha de varredura L e testa a interseção entre os que ficaram consecutivos"
    
    pred = L.predecessor (no)
    suc = L.sucessor (no)
    L.deleta (no)
    no.apaga()
    control.sleep()
    
    if pred != None and suc != None:
        marca_intersec (pred, suc, pontos)
    
    print("depois de deletar " + str(no))
    L.printa_arvore()

def Bentley_Ottmann_Mod (l):
    
    L = Abbb () # Linha de varredura
    
    # Pré-processamento - Transforma cada circulo em pontos-eventos
    # pontos é a ABBB de pontos eventos
    pontos = eventos (l)
    control.sleep()
    
    # Se precisar conferir a redblack
    pontos.printa_arvore()
    
    # Aqui de fato começa o Bentley e Ottman
    while not pontos.vazia():
        p = pontos.deleta_min()
        
        # desenha a linha
        id_linha = control.plot_vert_line (p.ponto.x)
        id_evento = p.ponto.hilight()
        control.sleep()
        
        print("-------------")
        "------------------------- Pontos da esquerda --------------------------------"
        # Insere as metade dos circulos
        for arco in p.ini:
            insere_na_linha (L, arco, pontos)
         
        "------------------------- Pontos de interseção ------------------------------"
        # Processando as interseções
        if len (p.inter) > 0:
            p.ponto.hilight('yellow')
        
            print("Arvore antes de trocar")
            L.printa_arvore()
        
        # Vamos trocar a ordem dos que intersectam em p
        trocados = []
        # Remove todos
        for arco in p.inter:
            trocados.append (arco)
            L.deleta (trocados[-1])
            print("depois de remover o " + str(trocados[-1]))
            L.printa_arvore()

        # Insere denovo com o novo ponto de referencia
        for arco in trocados:
            arco.ref = p.ponto
            print("vou reinserir o " + str(arco) + " com ref = " + str(arco.ref))
            L.insere (arco)
            
        if len (p.inter) > 0:
            print("depois de trocar")
            L.printa_arvore()
        
        "------------------------- Pontos da direita --------------------------------"
        # Deleta as metade dos circulos
        for arco in p.fim:
            deleta_da_linha (L, arco, pontos)
        
        # apaga a linha
        control.plot_delete (id_linha)    
        control.plot_delete (id_evento)
        p.ponto.unplot()
        