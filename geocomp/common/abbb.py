import sys

class Node:
    def __init__ (self, elemento, pai = None, no_esq = None, no_dir = None, vermelho = True):
        self.elemento = elemento
        self.pai = pai
        self.no_esq = no_esq
        self.no_dir = no_dir
        self.vermelho = vermelho

class Abbb:
    def __init__(self):
        
        # Vamos criar um nó nulo dummy
        # Isso facilitará para checar a cor dos nós
        self.nulo = Node (None, vermelho = False)
        
        self.raiz = self.nulo
        
    # Insere o elemento na árvore, mantendo balanceada
    def insere(self, elemento):
        
        # Busca onde inserir o elemento na árvore
        pai = None
        atual = self.raiz
        esq = True # Flag para saber se será o filho esquerdo ou direito

        while atual != self.nulo:
            pai = atual
            # Não permitimos nós repetidos
            if atual.elemento == elemento:
                return
            if atual.elemento > elemento:
                atual = atual.no_esq
                esq = True
            else:
                atual = atual.no_dir
                esq = False
            
        # insere o novo nó
        novo = Node (elemento, pai, no_esq = self.nulo, no_dir = self.nulo)
        if pai == None:
            novo.vermelho = False
            self.raiz = novo
        elif esq:
            pai.no_esq = novo
        else:
            pai.no_dir = novo

        # casos sem necessidade de rebalanceamento
        if novo.pai == None or novo.pai.pai == None:
            return

        # Rebalanceia a árvore
        self.__conserta_insere (novo)
        
    # Faz as operações necessárias para manter as propriedades da árvore rubro-negra
    # após a insersão do nó novo
    def  __conserta_insere(self, novo):
        # Vamos retirar todos os nós vermelhos consecutivos, 
        # o nó novo é sempre vermelho
        while novo.pai.vermelho:
            # pai é o filho direito
            if novo.pai == novo.pai.pai.no_dir:
                tio = novo.pai.pai.no_esq # irmao do pai = tio 
                # caso 1 
                if tio.vermelho:
                    tio.vermelho = False
                    novo.pai.vermelho = False
                    novo.pai.pai.vermelho = True
                    novo = novo.pai.pai
                else:
                    # caso 2 -> transforma no caso 3
                    # novo é o filho esquerdo -> novo vira o filho direito
                    if novo == novo.pai.no_esq:
                        novo = novo.pai
                        self.__rotaciona_dir (novo)
                    
                    # caso 3 -> novo é o filho direito
                    novo.pai.vermelho = False
                    novo.pai.pai.vermelho = True
                    self.__rotaciona_esq (novo.pai.pai)
            
            # espelhos dos casos anteriores
            else:
                tio = novo.pai.pai.no_dir
                if tio.vermelho:
                    tio.vermelho = False
                    novo.pai.vermelho = False
                    novo.pai.pai.vermelho = True
                    novo = novo.pai.pai
                else:
                    if novo == novo.pai.no_dir:
                        novo = novo.pai
                        self.__rotaciona_esq (novo)
                    novo.pai.vermelho = False
                    novo.pai.pai.vermelho = True
                    self.__rotaciona_dir (novo.pai.pai)

            if novo == self.raiz:
                break
        
        self.raiz.vermelho = False
    
    # busca o elemento na árvore e retorna o nó correspondente
    def busca (self, elemento):
        atual = self.raiz
        while atual != self.nulo:
            if atual.elemento == elemento:
                return atual
            if atual.elemento > elemento:
                atual = atual.no_esq
            else:
                atual = atual.no_dir
        return atual
        
    # deleta o elemento da árvore
    def deleta (self, elemento):
        
        buscado = self.busca (elemento)
        if buscado == self.nulo:
            return

        print("antes de deletar o " + str(elemento))
        self.printa_arvore()
        substituto_original_vermelho = buscado.vermelho
        
        # casos simples: um dos filhos é nulo -> troca o removido pelo outro filho
        if buscado.no_esq == self.nulo:
            substituto = buscado.no_dir
            substituto_original_vermelho = substituto.vermelho
            substituto.vermelho = buscado.vermelho
            self.__transplanta (buscado, buscado.no_dir)
            
        elif (buscado.no_dir == self.nulo):
            substituto = buscado.no_esq
            substituto_original_vermelho = substituto.vermelho
            substituto.vermelho = buscado.vermelho
            self.__transplanta (buscado, buscado.no_esq)
            
        # caso complexo: dois filhos não nulos
        # vamos buscar alguém que só tem um filho (o sucessor)
        else:
            substituto = self.__sucessor (buscado)
            substituto_original_vermelho = substituto.vermelho
            pai_substituto = substituto.pai
            
            # coloca o substituto no lugar do buscado
            if (pai_substituto != buscado):
                # tira o substituto lá de baixo
                pai_substituto.no_esq = substituto.no_dir
                #transfere os filhos
                substituto.no_esq = buscado.no_esq
                substituto.no_dir = buscado.no_dir
                substituto.no_esq.pai = substituto
                substituto.no_dir.pai = substituto
                self.__transplanta (buscado, substituto)
                
                # o nó que precisaremos consertar é o que deletamos lá de baixo
                if pai_substituto.no_esq != self.nulo:
                    substituto_original_vermelho = pai_substituto.no_esq.vermelho
                    pai_substituto.no_esq.vermelho = substituto.vermelho
                substituto.vermelho = buscado.vermelho
                
                substituto = pai_substituto.no_esq
                # as vezes o substituto é o none, então precisamos sinalizar o pai dele denovo
                substituto.pai = pai_substituto
            else:
                # O buscado é o pai do substituto

                # coloca o antigo irmão como filho
                substituto.no_esq = buscado.no_esq
                substituto.no_esq.pai = substituto
                
                # Coloca o antigo avô como pai
                substituto.pai = buscado.pai
                if buscado.pai != None:
                    if buscado.pai.no_dir == buscado:
                        buscado.pai.no_dir = substituto
                    else:
                        buscado.pai.no_esq = substituto
                else:
                    self.raiz = substituto
                
                # Ajeita as cores dos substitutos
                substituto_original_vermelho = substituto.no_dir.vermelho
                
                substituto.no_dir.vermelho = substituto.vermelho
                
                substituto.no_dir.pai = substituto
                    
                substituto.vermelho = buscado.vermelho
                substituto = substituto.no_dir
        
        print("antes de consertar")
        self.printa_arvore()
        if not substituto_original_vermelho:
            self.__conserta_deleta (substituto)
        print("depois de consertar")
        self.printa_arvore()

    # # Conserta a árvore modificada pela deleção
    def __conserta_deleta (self, x):
        # Nosso problema é que deletamos um nó preto,
        # Então o ramo da árvore que o x está tem um nó preto a menos
        # Precisamos fazer com que o lado do irmão do x também perca um nó preto
        while x != self.raiz and not x.vermelho:
            if x == x.pai.no_esq:
                irmao = x.pai.no_dir
                if irmao.vermelho:
                    # caso 1 - irmão vermelho
                    # Rotaciona pra esquerda - o irmão vermelho vai virar o avô (preto)
                    #                        - o pai vai ficar vermelho
                    #                        - o x vai ficar irmão de um nó preto
                    # E a quantidade de nós pretos em cada sub arvore vai permanecer igual
        
                    irmao.vermelho = False
                    x.pai.vermelho = True
                    self.__rotaciona_esq(x.pai)
                    irmao = x.pai.no_dir
                # Aqui o irmão é sempre um nó preto
                if not irmao.no_esq.vermelho and not irmao.no_dir.vermelho:
                    # caso 2 - os sobrinhos são pretos
                    # simplesmente pintamos o irmão de vermelho
                    irmao.vermelho = True
                    x = x.pai
                else:
                    # caso 3 - algum dos sobrinhos é vermelho
                    if not irmao.no_dir.vermelho:
                        irmao.no_esq.vermelho = False
                        irmao.vermelho = True
                        self.__rotaciona_dir (irmao)
                        irmao = x.pai.no_dir

                    # o sobrinho vermelho é o direito
                    irmao.vermelho = x.pai.vermelho
                    x.pai.vermelho = False
                    irmao.no_dir.vermelho = False
                    self.__rotaciona_esq (x.pai)
                    x = self.raiz
                    
            # Casos espelhos pra quando o x é filho direito
            else:
                irmao = x.pai.no_esq
                if irmao.vermelho:
                    # caso 1
                    irmao.vermelho = False
                    x.pai.vermelho = True
                    self.__rotaciona_dir (x.pai)
                    irmao = x.pai.no_esq

                if not irmao.no_esq.vermelho and not irmao.no_dir.vermelho:
                    # caso 2
                    irmao.vermelho = True
                    x = x.pai
                else:
                    if not irmao.no_esq.vermelho:
                        # caso 3
                        irmao.no_dir.vermelho = False
                        irmao.vermelho = True
                        self.__rotaciona_esq (irmao)
                        irmao = x.pai.no_esq 

                    irmao.vermelho = x.pai.vermelho
                    x.pai.vermelho = False
                    irmao.no_esq.vermelho = False
                    self.__rotaciona_dir (x.pai)
                    x = self.raiz
                    
        x.vermelho = False
        
    # Função que coloca o nó v no lugar do nó u
    def __transplanta(self, u, v):
        if u.pai == None:
            self.raiz = v
        elif u == u.pai.no_dir:
            u.pai.no_dir = v
        else:
            u.pai.no_esq = v
        v.pai = u.pai

    def __printa_arvore(self, node, indent, last):
        # printa a estrutura da subarvore com a raiz node
        if node != self.nulo:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.vermelho else "BLACK"
            print (str(node.elemento) + "(" + s_color + ")")
            self.__printa_arvore(node.no_esq, indent, False)
            self.__printa_arvore(node.no_dir, indent, True)
            
    # Printa a árvore na tela
    def printa_arvore(self):
        self.__printa_arvore(self.raiz, "", True)

    # Encontra o nó com menor valor a partir do node
    def __minimo (self, node):
        while node.no_esq != self.nulo:
            node = node.no_esq
        return node

    # Encontra o nó com maior valor a partir do node
    def __maximo (self, node):
        while node.no_dir != self.nulo:
            node = node.no_dir
        return node
 
    # Encontra o elemento sucessor do e
    def sucessor (self, e):
        x = self.busca (e)
        if x == self.nulo:
            return None
        x = self.__sucessor (x)
        return x.elemento
    
    # Encontra o elemento predecessor do e
    def predecessor (self, e):
        x = self.busca (e)
        if x == self.nulo:
            return None
        x = self.__predecessor (x)
        return x.elemento
    
    # Encontra o nó sucessor do nó não nulo x
    def __sucessor (self, x):
        # o sucessor é o filho mais a esquerda do filho da direita
        if x.no_dir != self.nulo:
            return self.__minimo (x.no_dir)
        
        # ou é o ancestral de x que é o filho esquerdo
        pai = x.pai        
        while pai != None and x == pai.no_dir:
            x = pai
            pai = pai.pai
            
        if pai == None:
            pai = self.nulo
        return pai

    # Encontra o nó predecessor do nó não nulo x
    def __predecessor(self,  x):
        #espelho do sucessor
        if (x.no_esq != self.nulo):
            return self.__maximo(x.no_esq)

        pai = x.pai        
        while pai != None and x == pai.no_esq:
            x = pai
            pai = pai.pai
        
        if pai == None:
            pai = self.nulo
        return pai

    # Rotaciona o nó raiz para a esquerda 
    def __rotaciona_esq(self, raiz):
                        
        filho = raiz.no_dir
        # Coloca o neto no lugar do filho
        raiz.no_dir = filho.no_esq
        if filho.no_esq != self.nulo:
            filho.no_esq.pai = raiz
        
        # Coloca o filho no lugar da raiz
        filho.pai = raiz.pai
        if raiz.pai == None:
            self.raiz = filho
        elif raiz == raiz.pai.no_esq:
            raiz.pai.no_esq = filho
        else:
            raiz.pai.no_dir = filho
            
        
        # Coloca a raiz no filho
        filho.no_esq = raiz
        raiz.pai = filho
        
        
    # Rotaciona o nó para a direita 
    def __rotaciona_dir(self, raiz):
        filho = raiz.no_esq
        
        # Coloca o neto no lugar do filho
        raiz.no_esq = filho.no_dir
        if filho.no_dir != self.nulo:
            filho.no_dir.pai = raiz

        # Coloca o filho no lugar da raiz
        filho.pai = raiz.pai
        if raiz.pai == None:
            self.raiz = filho
        elif raiz == raiz.pai.no_dir:
            raiz.pai.no_dir = filho
        else:
            raiz.pai.no_esq = filho
            
        # Coloca a raiz no filho
        filho.no_dir = raiz
        raiz.pai = filho
    
    def deleta_min (self):
        minimo = self.__minimo (self.raiz)
        e = minimo.elemento
        self.deleta (e)
        return e
    
    def vazia (self):
        return self.raiz == self.nulo

if __name__ == "__main__":
    bst = Abbb()
    bst.insere(8)
    bst.printa_arvore()
    print("-------------------")
    bst.insere(18)
    bst.printa_arvore()
    print("-------------------")
    bst.insere(5)
    bst.printa_arvore()
    print("-------------------")
    bst.insere(15)
    bst.printa_arvore()
    print("-------------------")
#    bst.insere(17)
#    bst.printa_arvore()
#    print("-------------------")
    bst.insere(25)
    bst.printa_arvore()
    print("-------------------")
    bst.insere(40)
    bst.printa_arvore()
    print("-------------------")
    bst.insere(80)
    bst.printa_arvore()
    print("-------------------")
    bst.deleta(8)
    bst.printa_arvore()
    
    print('--------------\n\n')
    bst2 = Abbb()
    
    
    bst2.insere(-6)
    bst2.printa_arvore()
    print("-------------------")
    bst2.insere(10)
    bst2.printa_arvore()
    print("-------------------")
    bst2.insere(11)
    bst2.printa_arvore()
    print("-------------------")
    bst2.insere(19)
    bst2.printa_arvore()
    print("-------------------")
    bst2.insere(17)
    bst2.printa_arvore()
    print("-------------------")
    bst2.insere(27)
    bst2.printa_arvore()
    print("-------------------")
    bst2.insere(41)
    bst2.printa_arvore()
    print("-------------------")
