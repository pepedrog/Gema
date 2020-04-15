import sys

# O insere foi feito
# Para fazer: deleção e busca

class Node:
    def __init__ (self, elemento, pai = None, no_esq = None, no_dir = None, vermelho = True):
        self.elemento = elemento
        self.pai = pai
        self.no_esq = no_esq
        self.no_dir = no_dir
        self.vermelho = vermelho

class Abbb:
    def __init__(self, compara):
        self.compara = compara
        
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
            if self.compara (atual.elemento, elemento) >= 0: # atual >= elemento
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
                        self.rotaciona_dir (novo)
                    
                    # caso 3 -> novo é o filho direito
                    novo.pai.vermelho = False
                    novo.pai.pai.vermelho = True
                    self.rotaciona_esq (novo.pai.pai)
            
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
                        self.rotaciona_esq (novo)
                    novo.pai.vermelho = False
                    novo.pai.pai.vermelho = True
                    self.rotaciona_dir (novo.pai.pai)

            if novo == self.raiz:
                break
        
        self.raiz.vermelho = False
    
    # busca o elemento na árvore e retorna o nó correspondente
    def busca (self, elemento):
        atual = self.raiz
        buscado = self.nulo
        while atual != self.nulo:
            if atual.elemento == elemento:
                buscado = atual
                break
            if self.compara (atual.elemento, elemento) > 0: # atual >= elemento
                atual = atual.no_esq
            else:
                atual = atual.no_dir
        return buscado
        
    # deleta o elemento da árvore
    def deleta (self, elemento):
        
        buscado = self.busca (elemento)
        if buscado == self.nulo:
            return

        removido = buscado
        removido_vermelho = removido.vermelho
        
        # casos simples: um dos filhos é nulo -> troca o removido pelo outro filho
        if buscado.no_esq == self.nulo:
            substituto = buscado.no_dir
            self.__transplanta (buscado, buscado.no_dir)
        elif (buscado.no_dir == self.nulo):
            substituto = buscado.no_esq
            self.__transplanta (buscado, buscado.no_esq)
        
        # caso complexo: dois filhos não nulos
        # vamos buscar alguém que só tem um filho
        else:
            um_filho = self.minimo (buscado.no_dir)
            removido_vermelho = um_filho.vermelho
            substituto = um_filho.no_dir
            if um_filho.pai == buscado:
                substituto.pai = um_filho
            else:
                self.__transplanta (removido, removido.no_dir)
                removido.no_dir = buscado.no_dir
                removido.no_dir.pai = removido

            self.__transplanta(buscado, um_filho)
            um_filho.no_esq = buscado.left
            um_filho.no_esq.pai = um_filho
            um_filho.vermelho = buscado.color
        if removido_vermelho:
            self.__conserta_deleta (substituto)

    # # Conserta a árvore modificada pela deleção
    def conserta_deleta (self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    # case 3.2
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        # case 3.3
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    # case 3.4
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 0 and s.right.color == 0:
                    # case 3.2
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        # case 3.3
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left 

                    # case 3.4
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0
        
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

    # find the node with the minimum key
    def minimo (self, node):
        while node.no_dir != self.nulo:
            node = node.no_esq
        return node

    # find the node with the maximum key
    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    # find the successor of a given node
    def successor(self, x):
        # if the right subtree is not None,
        # the successor is the leftmost node in the
        # right subtree
        if x.no_dir != self.nulo:
            return self.minimo (x.no_dir)

        # else it is the lowest ancestor of x whose
        # left child is also an ancestor of x.
        pai = x.pai
        while pai != self.nulo and x == pai.no_dir:
            x = pai
            pai = pai.pai
        return pai

    # find the predecessor of a given node
    def predecessor(self,  x):
        # if the left subtree is not None,
        # the predecessor is the rightmost node in the 
        # left subtree
        if (x.left != self.TNULL):
            return self.maximum(x.left)

        y = x.parent
        while y != self.TNULL and x == y.left:
            x = y
            y = y.parent

        return y

    # Rotaciona o nó raiz para a esquerda 
    def rotaciona_esq(self, raiz):
        filho = raiz.no_dir
        
        # Coloca o neto no lugar do filho
        raiz.no_dir = filho.no_esq
        if raiz.no_esq != self.nulo:
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
    def rotaciona_dir(self, raiz):
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
            raiz.pai.right = filho
        else:
            raiz.pai.no_esq = filho
            
        # Coloca a raiz no filho
        filho.no_dir = raiz
        raiz.pai = filho    
    
def compara( x, y):
    return x - y

if __name__ == "__main__":
    bst = Abbb(compara)
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
    #bst.delete_node(25)
    bst.printa_arvore()
