# -*- coding:utf-8 -*-
'''
Created on 1/12/2018

@author: valves
'''

from copy import deepcopy
import random
from numpy.random import uniform, choice, normal


class Stack: #classe Stack para o historico
    def __init__(self):
        self.items = []
    def is_empty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def top(self):
        return self.items[len(self.items)-1]
    def size(self):
        return len(self.items)

class GandaGaloEngine:
    
    def __init__(self):
        self.linhas = 0 #nº linhas do tabuleiro 
        self.colunas = 0 #nº colunas do tabuleiro
        self.tabuleiro = [] #matriz que representa o puzzle
        self.ancora=Stack() # Stack que guarda os nº das jogadas em que se fez ancora
        self.historico=Stack() # Stack do histórico dos movimentos ao longo do jogo
        self.jogada_n=0 # nº da jogada (irá diminuir caso se use o undoancora ou undo, por se retornar no jogo)
        self.tab_backup=[] #backup do self.tabuleiro, a usar se mostrar um tabuleiro, enquanto outro já esta aberto
        self.lin_backup=0 #backup do self.linhas, a usar se mostrar um tabuleiro, enquanto outro já esta aberto
        self.col_backup=0 #backup do self.colunas, a usar se mostrar um tabuleiro, enquanto outro já esta aberto
        self.resolve_auto_bifurc=Stack() #usado no resolver: quando no resolver, numa dada casa se pode jogar tanto X como O,
        #guarda a posição da jogada; é útil se mais à frente no jogo o tabuleiro bloqueia, podendo voltar-se atrás;
        # não é necessário para jogadas em casas que numa casa qualquer uma das jogadas levam a que o tabuleiro deixe de ser válido 
        self.conta_bifurc_gerar=0 # variável que vai contar o nº de jogadas em que se pode ser tanto X como O;
        #se este exceder um fator, o tabuleiro é considerado díficil
    
    def ler_tabuleiro_ficheiro(self, filename, abrir=0, aberto=0): 
        #abrir=0: metodo usado no comando mostrar; se não for 0, usado no abrir
        #aberto=0: quando ainda não foi aberto nenhum tabuleiro; se for o contrário, ter-se de guardar do tabuleiro original
        '''
        Cria nova instancia do jogo numa matriz
        :param filename: nome do ficheiro a ler
        '''        
        if aberto!=0: # se há tabuleiro aberto,tem-se de guardar das informações do tabuleiro original
            print("AVISO: jogo aberto.")
            self.tab_backup=self.tabuleiro
            self.lin_backup=self.linhas
            self.col_backup=self.colunas
        ficheiro_valido=1 # se ficheiro valido, ficheiro_valido=1 
        try:
            ficheiro = open(filename, "r") #abrir ficheiro filename
            lines = ficheiro.readlines() #ler as linhas do ficheiro para a lista lines
            dim = lines[0].strip('\n').split(' ')  # obter os dois numeros da dimensao do puzzle, retirando o '\n'  
            try:
                self.linhas = int(dim[0])  # retirar o numero de linhas
                self.colunas = int(dim[1])  # retirar o numero de colunas
                if len(dim)==2 and self.linhas>2 and self.colunas>2: # verifica se a primeira linha tem 2 nº
                    # e se esses valores são maiores que 2, de modo a ser um tabuleiro no mínimo de 3*3
                    if len(lines)-1!=self.linhas:ficheiro_valido=0 
                    #verifica o nº de linhas, que terá de ser igual a self.linhas, ou senão, ficheiro inváildo
                    else:
                        for i in range(1,len(lines)):
                            line=lines[i].split() #separa carateres por linha
                            if line.count('.')+line.count('#')+line.count('X')+line.count('O')!=self.colunas: 
                             #conta se o nº de carateres válido que tem de ser igual ao nº colunas
                                 ficheiro_valido=0 #ficheiro invalido
                else: ficheiro_valido=0 #ficheiro invalido
            except ValueError: ficheiro_valido=0 #ficheiro invalido, por não ter valores numéricos na 1ª linha  
            if ficheiro_valido==1: # se ficheiro válido, escreve os carateres no self.tabuleiros
                self.tabuleiro=[]
                for i in range(1,len(lines)):
                    self.tabuleiro.append(lines[i].split())      
            else: print("Erro: ficheiro com formato inválido.")  
            return self.tabuleiro
        except:
            print("Erro: na leitura do tabuleiro")
        else:
            ficheiro.close()
        return self.tabuleiro
    
    def backup(self): 
        #quando se mostra um tabuleiro, com outro aberto
        #retorna os dados originais; limpa-se backups
        self.linhas = self.lin_backup
        self.colunas = self.col_backup
        self.tabuleiro = self.tab_backup
        self.lin_backup=-1
        self.col_backup=-1
        self.tab_backup=[]
        
    def tabuleiro_valido(self):
        valido=1 #se valido=1, tabuleiro válido
        for i in range(self.linhas):
            if valido==1: #De modo a não fazer nada caso já tenha determinado que não e valido
                for j in range(self.colunas):
                    if valido==1: #De modo a não fazer nada caso já tenha determinado que não e valido
                        if self.tabuleiro[i][j]=='X' or self.tabuleiro[i][j]=='O': #se o carater a analisar é um X ou O
                            try:  #para não bloquear se ultrapassar os limites da matriz     
                                if (self.tabuleiro[i][j]==self.tabuleiro[i-1][j] and self.tabuleiro[i][j]==self.tabuleiro[i+1][j]) and i-1>-1: 
                                    # verficar se os pontos na mesma coluna são iguais, i-1>-1 de modo a não comparar com o tabuleiro[-1], que seria o tabuleiro[len(tabuleiro)-1] 
                                    valido=0 #tabuleiro não válido
                            except IndexError: pass #indices fora da matriz não se podem comparar
                            try:
                                if(self.tabuleiro[i][j]==self.tabuleiro[i-1][j-1] and self.tabuleiro[i][j]==self.tabuleiro[i+1][j+1]) and i-1>-1 and j-1>-1: 
                                    # verficar se os pontos na mesma diagonal são iguais i-1>-1 de modo a não comparar com o tabuleiro[-1], que seria o tabuleiro[len(tabuleiro)-1] 
                                    valido=0 #tabuleiro não válido
                            except IndexError: pass #indices fora da matriz não se podem comparar
                            try:    
                                if (self.tabuleiro[i][j]==self.tabuleiro[i][j-1] and self.tabuleiro[i][j]==self.tabuleiro[i][j+1]) and j-1>-1: 
                                    # verficar se os pontos na mesma linha são iguais
                                    valido=0 #tabuleiro não válido
                            except IndexError: pass #indices fora da matriz não se podem comparar
                            try:
                                if (self.tabuleiro[i][j]==self.tabuleiro[i-1][j+1] and self.tabuleiro[i][j]==self.tabuleiro[i+1][j-1]) and i-1>-1 and j-1>-1: 
                                    # verficar se os pontos na mesma diagonal são iguais
                                    valido=0 #tabuleiro não válido
                            except IndexError: pass #indices fora da matriz não se podem comparar
        if self.tabuleiro==[]: # tabuleiro vazio
            print("Erro: nenhum tabuleiro aberto.")
            return False 
        elif valido==1: return True
        else:return False
        
    def jogada(self,caract,lin,col):
        try:
            if caract=="X" or caract=="O": #verifica caratares válidos
                if self.tabuleiro[lin][col]==".": #verifica se posição não está bloqueada
                    if lin>=0 and lin<self.linhas and col>=0 and col<self.linhas:#verifica se posição existe na matriz
                        self.tabuleiro[lin][col]=caract #completa a jogada
                        self.historico.push([lin,col,caract]) #guarda a jogada no histórico
                        self.jogada_n+=1 #incrementa-se o nº da jogada
                        contador,resolvido=0,0# contador espaços libertos para jogadas e resolvido guardará se o jogo acabou 
                        for line in self.tabuleiro: 
                            contador+=line.count(".")# conta espaços libertos para jogadas
                        if contador==0: # se não há espeços libertos para jogadas
                            resolvido=1 # jogo completo
                        if resolvido==1 and self.tabuleiro_valido(): #tabuleiro preenchido e válido
                            print("Completou o jogo!")
                    else: print("Erro: coordenadas não válidas. O tabuleiro mantém-se inalterado.")
                else: print("Erro: posição bloqueada. O tabuleiro mantém-se inalterado.")
            else: print("Erro: caracter não válido. O tabuleiro mantém-se inalterado.")
        except: print("Erro: na jogada.")
      
    def ajuda_jogada(self,resolver_auto=0):    #se resolver_auto==0, este método é para o comando ajuda; caso contrário, é usado para o comando resolver
        sugestoes_2=[]#posições em que em pelo menos uma das direções tem 2 X's ou O´s
        for i in range(self.linhas):
                for j in range(self.colunas):
                    if self.tabuleiro[i][j]==".": #posições em que se pode jogar
                        #todas as possibilidades(todas as direcoes a analisar)
                        #se os 2 pontos adjacentes na mesma direção foram iguais e carateres de jogo X ou O
                        #o ciclo guarda o carater oposto para não bloquear o jogo
                        #2 pontos "anteriores" ou "posteriores":
                        #[(i-2),(j-2)],[(i-1),(j-1)]: diagonal p/ cima esq
                        #[[(i),(j-2)],[(i),(j-1)]]: linha p/ esq
                        #[(i+1),(j-1)],[(i+2),(j-2)]: diagonal p/ baixo esq
                        #[[(i-2),(j)],[(i-1),(j)]]:coluna p/cima
                        #[[(i+1),(j)],[(i+2),(j)]]:coluna p/baixo
                        #[[(i-2),(j+2)],[(i-1),(j+1)]]: diagonal p/ cima dir
                        #[[(i),(j+1)],[(i),(j+2)]]:linha p/ dir
                        #[[(i+1),(j+1)],[(i+2),(j+2)]]: diagonal p/ baixo dir
                        #ponto a analisar entre 2 pontos:
                        #[[(i-1),(j-1)],[(i+1),(j+1)]]: diag esq -> dir
                        #[[(i),(j-1)],[(i),(j+1)]]:linha
                        #[[(i-1),(j)],[(i+1),(j)]]:coluna
                        #[[(i-1),(j+1)],[(i+1),(j-1)]]: diag dir -> esq
                        todas_direcoes=  [[[(i-2),(j-2)],[(i-1),(j-1)]],[[(i),(j-2)],[(i),(j-1)]],
                                          [[(i+1),(j-1)],[(i+2),(j-2)]],[[(i-2),(j)],[(i-1),(j)]],
                                          [[(i+1),(j)],[(i+2),(j)]],[[(i-2),(j+2)],[(i-1),(j+1)]],
                                          [[(i),(j+1)],[(i),(j+2)]],[[(i+1),(j+1)],[(i+2),(j+2)]],
                                          [[(i-1),(j-1)],[(i+1),(j+1)]],[[(i),(j-1)],[(i),(j+1)]],
                                          [[(i-1),(j)],[(i+1),(j)]],[[(i-1),(j+1)],[(i+1),(j-1)]]] 
                        sug=0 #para guardar se alguma sugestão já foi definida para o ponto (i,j)
                        for direc in todas_direcoes:
                            if sug==0: #caso já se saiba que é uma possível sugestão, isto limita o código a correr       
                                try:
                                    if (self.tabuleiro[direc[0][0]][direc[0][1]]==self.tabuleiro[direc[1][0]][direc[1][1]] 
                                        and (self.tabuleiro[direc[0][0]][direc[0][1]]=="X" or 
                                        self.tabuleiro[direc[0][0]][direc[0][1]]=="O") and 
                                        direc[0][0]>-1 and direc[0][1]>-1 and direc[1][0]>-1 and direc[1][1]>-1):
                                        # Verifica se em alguma das opções de todas_direcoes ocorre
                                        # que os 2 elementos são iguais e iguais a X ou O, e garantir que os indices
                                        # não são negativos
                                        if self.tabuleiro[direc[0][0]][direc[0][1]]=="O": cel='X' #sugere o carater oposto para não bloquear o jogo
                                        else: cel='O'#sugere o carater oposto para não bloquear o jogo
                                        sugestoes_2.append([i,j,cel])#guarda linha, coluna e sugestao de carater
                                        sug=1#sugestão já definida
                                except IndexError: pass #caso os indices ultrapassem os limites da matriz
                            #de modo a não colocar mais condições que limitam os índices a valores menores que os limites da matriz 
        sugestao = [-1,-1] #variável para o return
        if sugestoes_2 != []: #se houver alguma situação em que 2 carateres adjacentes iguais
            sugestao=random.choice(sugestoes_2) #escolha aleatória da lista de sugestão, porque todas as sugestões são de jogadas prioritárias e importantes a resolver
        else: # se nao houver nenhuma sequencia de 2 elementos iguais na lista, procura-se a primeira casa disponível 
            sug=0 #para guardar se alguma sugestão já foi definida
            lin=0
            col=0
            try:
                while sug==0 and lin<self.linhas: 
                #enquanto não for encontrado local disponível e enquanto está dentro dos limites da matriz
                    if self.tabuleiro[col][lin]==".": #local disponível
                        sug=1 #sugestão encontrada: para o ciclo while
                        sugestao=[col,lin,["O","X"]] #guarda posicao e um carater aleatório
                    else: #caso não seja local disponível
                        if col==self.colunas-1: #se o ciclo está no final de uma linha
                            #passa-se para a próxima linha, para a primeira coluna
                            col=0 
                            lin+=1
                        else: #se o ciclo não está no final de uma linha
                            #passa-se para a próxima coluna
                            col+=1
            except: pass
        if resolver_auto==0: return sugestao[:2] #se for utilizado o comando ajuda, so se pretende retornar posição, não o carater sugerido
        else: return sugestao  #se usado no comando resolver          
    
    def def_resolver_auto(self, gerar=0, dific=0): 
        # se gerar != 0, conta o nº de bifurcações encontradas até encontrar a solução
        resolvido=0 #variável que indica se o tabuleiro está resolvido
        while self.tabuleiro_valido() and resolvido==0:
            tab_cheio_val=True # verifica se o tabuleiro está cheio e válido
            #enquanto o tabuleiro estiver válido e não resolvido
            pos=self.ajuda_jogada(1) #vê a sugestão do metodo ajuda_jogada, retornando também o carater a jogar
            if type(pos[2])==list: # se houver mais que uma sugestão de jogada (jogadas não críticas)
                #jogadas críticas são irrelevantes: jogar uma ou outra fazer perder o jogo a mesma
                global jog
                jog = deepcopy(self.jogada_n)
                self.resolve_auto_bifurc.push(jog) #guarda a jogada da dupla sugestão
                del jog
                pos[2]='X' #seleciona um elemento, por defeito fica o X
                if gerar!=0: self.conta_bifurc_gerar+=1
            self.jogada(pos[2],pos[0],pos[1]) #implementa a sugestão
            contador=0 #contador de espaços disponíveis ("."): se 0: tabuleiro resolvido
            for line in self.tabuleiro: contador+=line.count(".")# conta espaços libertos para jogadas
            if contador==0: # se não há espeços libertos para jogadas
                resolvido=1 # jogo completo
            if resolvido==1:tab_cheio_val=self.tabuleiro_valido() # verifica se o tabuleiro está cheio e válido
            if gerar == 0: self.printpuzzle() #imprime cada iteração da resolução (exceto no gerar)
            print()
            if ((not tab_cheio_val or (contador > 0 and not self.tabuleiro_valido()))
            and not self.resolve_auto_bifurc.is_empty()): #se tabuleiro não resolvido e não válido, com bifurcações em memória
                print("Erro: tabuleiro inválido. Irá se retornar à última posição em que se podia ser ambas as jogadas.")
                resolvido=0 #caso o tabuleiro estivesse preenchido, mas a última jogada tornava o tabuleiro inválido
                ult_pos=self.resolve_auto_bifurc.pop()
                pos_ult_jog=[]#irá guardar a linha e coluna aonde jogar O quando ocorre bifurcação
                while self.jogada_n > ult_pos: #enquanto não se faz os undo's até à bifurcação
                    if self.jogada_n> ult_pos+1: self.return_undo(1) #se for antes da última jogada, não é preciso o retorno das posições
                    else: pos_ult_jog=self.return_undo(1,1)#última jogada antes da bifurcação, retorna os posições da jogada anterior
                    if gerar == 0: self.printpuzzle() #imprime cada iteração da resolução (exceto no gerar)
                    print()
                self.jogada('O',pos_ult_jog[0],pos_ult_jog[1]) #no local da jogada da bifurcação joga O, que é o opsto do default X
                if gerar == 0: self.printpuzzle() #imprime cada iteração da resolução (exceto no gerar)
                print()
                
        if resolvido==1 and self.tabuleiro_valido():print("Tabuleiro Preenchido. Acabou o jogo.") # o tabuleiro cheio e válido o jogo acabou
        elif gerar==0: print("Erro: tabuleiro sem solução.")
        if gerar!=0 and dific==0:
            if resolvido==1 and self.tabuleiro_valido(): return True
            else: return False 
            del self.resolve_auto_bifurc #elimina a stack de bifurcações
            self.resolve_auto_bifurc=Stack() #cria uma stack de bifurcações vazia
        
    def return_undo(self, anc=0, volta_atras_res_aut=0): 
        #volta a jogada anterior; se anc diferente de 0, é usado no volta_unancora
        #volta_atras_res_aut!=0: usando no resolver para quando o resolver nao consegue
        #acabar um tabuleiro, mas teve pelo menos um jogada em que pode escolher entre X e O
        try:
            if not self.historico.is_empty(): #se o histórico não está vazio
                volta=[]
                if volta_atras_res_aut!=0: volta=self.historico.top()#guarda a alteração de linha para o resolver automático
                ult_altera=self.historico.pop() #define o tabuleiro como a jogada anterior
                self.tabuleiro[ult_altera[0]][ult_altera[1]]='.' # altera o tableiro as últimas posições alteradas para '.': célula vazia
                self.jogada_n-=1 #decrementa-se-se o nº da jogada
                if volta_atras_res_aut!=0: return volta #retornar a alteração de linha para o resolver automático
            else:#se o histórico está vazio (só tem uma jogada no histórico): retorna à jogada original
                if anc==0: print("Erro: não há jogadas anteriores em memória.") # esta mensagem nao é imprimida se utilizada no undo ancora
        except: print("Erro: no undo")
            
    def nova_ancora(self, new_var=0): 
        #define guarda posição de jogada numa stack
        #new_var!=0: chamado em self.ver_mais_1_sol
        try:
            global pos
            pos=deepcopy(self.jogada_n) #duplica-se a instância self.jogada_n
            self.ancora.push(pos) #adiciona-se uma posição de jogadas no self.ancora
            del pos # elimina-se a instÂncia com o destruidor __del__
            if new_var==0: print("Âncora atual:") #ancora atual é igual ao tabuleiro atual, a ser imprimido pelo código da Shell
        except: print("Erro: no ancora.")
        
    def volta_unancora(self): #volta a ancora anterior        
        try:
            if self.ancora.is_empty(): 
                print("Erro: não há âncoras em memória.") # se a stack do self.ancora está vazia
            elif self.ancora.top()>self.jogada_n: # se a jogada atual procede a última ancora
                print("Erro: última jogada procede última âncora; esta âncora será eliminada.") # se, com o undo, o jogador já passou para posições anteriores
                self.ancora.pop() #última âncora eliminada
            else:
                pos= self.ancora.pop() #retira a última âncora
                while self.jogada_n > pos: #enquanto há jogadas posteriores à última ancora
                    self.return_undo(1) #retorna a jogada anterior
        except: print("Erro: no undo.")


    def gerar_tabuleiro(self,dific,linha,coluna):
        try:
            if (dific==1 or dific==2) and linha > 2 and coluna > 2: 
                # se o nível de dificuldade é 1 (fácil)
                # ou 2 (díficil), e se o tamanho do tabuleiro é pelo menos 3*3
                # back-up (recorrendo a deepcopy nos Stacks) das variáveis que são usadas no jogada, undo, resolver,...
                # e limpeza (recorrendo ao __del__ em Stacks), de modo a ter "variáveis vazias", de modo a puder-se
                # usar os métodos já criados
                self.tab_backup=self.tabuleiro 
                self.lin_backup=self.linhas
                self.col_backup=self.colunas
                self.linhas=linha
                self.colunas=coluna
                self.settabuleiro([]) #define o tabuleiro como vazio
                global jogadas_pos_gerar, historico_bk, ancora_bk
                jogadas_pos_gerar=deepcopy(self.jogada_n)
                historico_bk=deepcopy(self.historico)
                ancora_bk=deepcopy(self.ancora)
                novo_tab=[] # irá ter um tabuleiro vazio de tamanho linha*coluna
                for i in range(linha):
                    novo_tab.append([])
                    for j in range(coluna):
                        novo_tab[i].append('.')
                poss_linha=[] #irá ter todos os valores 0:linha
                #usado para o random de jogadas bloquedas no tabuleiro
                for i in range(linha):poss_linha.append(i) #[0,1,2....,linha]
                poss_col=[] #irá ter todos os valores 0:coluna
                #usado para o random de jogadas bloquedas no tabuleiro
                for i in range(coluna):poss_col.append(i) #[0,1,2....,coluna]
                tab_valido = False #vai verificar se o tabulero criado é válido    
                while not tab_valido: #enquanto não encontrar um tabuleiro com as caraterísticas que se pretende
                    self.gerar_novas_variaveis()#limpa histórico, ancora e nº de jogadas; guarda em ancora a jogada inicial
                    tab_gerar=novo_tab #igual a tabuleiro vazio
                    tab_gerado_valido=False
                    n_casas_bloq=int(uniform(0.03,0.10)*self.linhas*self.colunas) # 3% a 10% de casas bloqueadas ("#")
                    for i in range(n_casas_bloq): #coloca o nº de casas bloqueadas definidas atrás
                        linha_aleat=random.choice(poss_linha) #escolhe uma linha aleatoriamente
                        col_aleat=random.choice(poss_col) #escolhe uma coluna aleatoriamente
                        tab_gerar[linha_aleat][col_aleat]="#" #coloca "#" na posição aleatória
                    self.settabuleiro(tab_gerar) #guarda este novo tabuleiro
                    tab_gerado_valido=False
                    try: 
                        self.def_resolver_auto(1) #resolve o tabuleiro
                        print("OK")
                        tab_gerado_valido=self.tabuleiro_valido() #verifica a validade
                    except: pass
                    if tab_gerado_valido:
                        n_casas_bloq_jogadas=int(uniform(0.10,0.25)*linha*coluna) #bloqueia jogadas em 15% a 30% do tabuleiro
                        for i in range(self.linhas*self.colunas, n_casas_bloq_jogadas-1, -1):
                            colocado=False #verifica se foi colocada uma casa bloqueada no tabuleiro
                            while not colocado: #enquanto não for colocada uma casa bloqueada no tabuleiro
                                linha_aleat=random.choice(poss_linha) #escolhe uma linha aleatoriamente
                                col_aleat=random.choice(poss_col) #escolhe uma coluna aleatoriamente
                                if self.tabuleiro[linha_aleat][col_aleat]=='O' or self.tabuleiro[linha_aleat][col_aleat]=='X': # se a acasa aleatoriamente escolhida estiver preenchida
                                    self.tabuleiro[linha_aleat][col_aleat]='.' #coloca a casa vazia
                                    colocado=True
                        self.gerar_novas_variaveis() #limpa histórico, ancora e nº de jogadas; guarda em ancora a jogada inicial
                        self.conta_bifurc_gerar=0 #retorna a contagem de bifurcações a 0
                        try:self.def_resolver_auto(1,1) #resolve o tabuleiro 
                        except: pass
                        fator=float(self.conta_bifurc_gerar/(self.linhas*self.colunas - n_casas_bloq_jogadas)) 
                        #calcula a fracao de casas jogadas se poderiam
                        # jogar tanto X ou O sobre o nº de casas total - as casas já bloquedas
                        fator_facil_dificil=0.15 # se menos que 15% bifurcações: fácil, se mais: díficil
                        if not self.ver_mais_1_sol(): # se não tem outra solução
                            if ((dific == 1 and fator < fator_facil_dificil) or
                                (dific == 2 or fator > fator_facil_dificil)):
                                tab_valido=True #tabuleiro válido
                                self.volta_unancora()  #retorna ao tabuleiro inicial
                            else: self.settabuleiro([]) #limpa tabuleiro
                        else: self.settabuleiro([]) #limpa tabuleiro
        
                filename='Tab_dific_'+str(dific)+'_linhas_'+str(self.linhas)+'_colunas'+str(self.colunas)+'_auto.txt' #nome do ficheiro
                self.guardar_tabuleiro(filename) # guarda o ficheiro
                #retorna às variáveis originais
                self.backup()
                del self.historico
                del self.ancora
                self.historico=deepcopy(historico_bk)
                self.ancora=deepcopy(ancora_bk)
                self.conta_bifurc_gerar=0
                self.jogada_n=jogadas_pos_gerar
                del historico_bk
                del ancora_bk
                del jogadas_pos_gerar
            else:
                print("Erro: parâmetros inválidos.")        
        except: print("Erro: no gerar")
                
    def ver_mais_1_sol(self):
        #vai verificar se o tabuleiro do gerar tem mais que uma solução
        outra_sol=False
        if self.resolve_auto_bifurc.size() != 0:
            ult_pos=self.resolve_auto_bifurc.pop() #última bifurcação
            pos_ult_jog=[]#irá guardar a linha e coluna aonde jogar O quando ocorre bifurcação
            while self.jogada_n > ult_pos: #enquanto não se faz os undo's até à bifurcação
                if self.jogada_n> ult_pos+1: self.return_undo(1) #se for antes da última jogada, não é preciso o retorno das posições
                else: pos_ult_jog=self.return_undo(1,1) #última jogada antes da bifurcação, retorna os posições da jogada anterior
            self.jogada('O',pos_ult_jog[0],pos_ult_jog[1]) #no local da jogada da bifurcação joga O, que é o opsto do default X
            print("Verificando outras soluções")
            outra_sol=self.def_resolver_auto() #resolve o tabuleiro, à procura de uma 2ª solução
            print("Verificado")
        return outra_sol
                
    def gerar_novas_variaveis(self):
        #limpa histórico e ancoras para o gerar
        del self.historico
        del self.ancora
        self.jogada_n=0               
        self.historico=Stack()
        self.ancora=Stack()
        self.nova_ancora(1) #ancora do tabuleiro vazio
    
    def getlinhas(self): #retorna o nº de linhas
        return self.linhas
    
    def getcolunas(self): #retorna o nº de colunas
        return self.colunas
    
    def gettabuleiro(self): #retorna tabuleiro
        return self.tabuleiro
    
    def settabuleiro(self, t): # iguala tabuleiro a t
        self.tabuleiro = t
        
    def printpuzzle(self): #imprime o tabuleiro
        for linha in self.tabuleiro:
            for simbolo in linha:
                print(simbolo,end=" ")
            print()
        
    def guardar_tabuleiro(self, filename):
        try:
            jogo=self.gettabuleiro()#devolve o tabuleiro
            lin,col=self.getlinhas(),self.getcolunas()
            guardar_puzzle=open(filename,'w') #abre o ficheiro arg
            guardar_puzzle.write(str(lin)+' '+str(col)+'\n') #escreve 1ª linha com nº linhas e colunas
            for i in range(lin): #imprimir linha a linha os carateres separados por espaços
                for j in range(col): #imprimir coluna a coluna os carateres
                    if j != col-1: #se o ciclo não está no fim de uma linha
                        guardar_puzzle.write(jogo[i][j]+' ') #imprimir carater e espaço
                    elif i != lin-1: #se o ciclo está no fim de uma linha, mas não na última linha
                        guardar_puzzle.write(jogo[i][j]+'\n') #imprimir carater e mudança de linha
                    else: #ciclo na última linha e coluna
                        guardar_puzzle.write(jogo[i][j])#imprime só carater
        except: print("Erro: no guardar.")
        else: guardar_puzzle.close() #fecha o ficheiro

