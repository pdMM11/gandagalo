# -*- coding:utf-8 -*-
'''
Created on 1/12/2018

@author: valves
'''
from cmd import *
from GandaGaloWindow import GandaGaloWindow
from GandaGaloEngine import GandaGaloEngine


class GandaGaloShell(Cmd):
    
    intro = 'Interpretador de comandos para o GandaGalo. Escrever help ou ? para listar os comandos disponíveis.\n'
    prompt = 'GandaGalo> '
                               
    def do_mostrar(self, arg):
        " -  comando mostrar que leva como parâmetro o nome de um ficheiro..: mostrar <nome_ficheiro> \n" 
        try:
            lista_arg = arg.split() #separa os argumentos pelos espaços
            num_args = len(lista_arg) #nº argumentos
            if num_args == 1:
                aberto=0 #esta variável vai averiguar se já há tabuleiros abertos
                if eng.gettabuleiro() != []: aberto=1 #tabuleiro aberto
                eng.ler_tabuleiro_ficheiro(lista_arg[0],0,aberto) #lê o ficheiro
                eng.printpuzzle() #imprime o puzzle
                self.do_ver(' ') # mostra graficamente o tabuleiro
                if aberto==0: # se não há tabuleiro aberto
                    eng.settabuleiro([]) #limpa o tabuleiro
                    #porque este comando é só para ver, apagando então este tabuleiro
                    #se quiserem jogar, terá de ser com o abrir
                else: eng.backup()
                    #se já existir um tabuleiro aberto, mostra a mesma o tabuleiro pretendido, mas não o abre
            else: print("Número de argumentos inválido!")
        except: print("Erro: ao mostrar o puzzle")
    
    
    def do_abrir(self, arg):
        " - comando abrir que leva como parâmetro o nome de um ficheiro..: abrir <nome_ficheiro>  \n"
        if eng.gettabuleiro()==[]: # se não existir nenhum tabuleiro
            try:
                lista_arg = arg.split() #separa os argumentos pelos espaços
                num_args = len(lista_arg) #nº argumentos
                if num_args == 1:
                    eng.ler_tabuleiro_ficheiro(lista_arg[0],1) #lê o tabuleiro (útil depois para o comando gravar)
                    if eng.gettabuleiro() !=[]: # se tabuleiro não vazio imprime-o
                        eng.printpuzzle()
                        self.do_ver(' ') # mostra graficamente o tabuleiro
                    else: print("Erro: leitura de ficheiro.")
                else:
                    print("Número de argumentos inválido!")
            except:
                print("Erro: ao mostrar o puzzle")
        else:
            print("Erro: terá de fechar o jogo anterior.")
            
    
    def do_gravar(self, arg):
        " - comando gravar que leva como parâmetro o nome de um ficheiro..: gravar <nome_ficheiro>  \n"
        if eng.gettabuleiro()!=[]: # se existir tabuleiro
            try:
               lista_arg = arg.split() #separa os argumentos pelos espaços
               num_args = len(lista_arg) #nº argumentos
               if num_args == 1:
                   eng.guardar_tabuleiro(lista_arg[0]) # guarda tabuleiro
               else:
                    print("Número de argumentos inválido!")
            except:
                print("Erro: ao guardar o puzzle.")
        else: print("Erro: não existem dados para gravar")
    
    
    def do_jogar(self, arg):    
        " - comando jogar que leva como parâmetro o caractere referente à peça a ser jogada (‘X’ ou ‘O’) e dois inteiros que indicam o número da linha e o número da coluna, respetivamente, onde jogar \n"
        if eng.tabuleiro_valido(): #se tabuleiro existente e válido
            lista_arg = arg.split() #separa os argumentos pelos espaços
            num_args = len(lista_arg) #nº argumentos, que deverá ser o carater, linha e coluna a jogar
            if num_args == 3:
                try:
                    caract=lista_arg[0] # primeiro argumento é o catarer a jogar
                    linha=int(lista_arg[1])-1 # 2º argumento é a linha aonde jogar (-1 de modo aos indices começarem em 1)
                    coluna=int(lista_arg[2])-1 # 3º argumento é a coluna aonde jogar (-1 de modo aos indices começarem em 1)
                    eng.jogada(caract,linha,coluna) #jogar
                    self.do_ver(' ') # mostra graficamente o tabuleiro
                except ValueError: 
                    print("Erro: na jogada: argumento 1: X ou O; argumentos 2 e 3 têm de ser inteiros.")
            else: print("Número de argumentos inválido!")
            eng.printpuzzle() #imprime o tabuleiro
        else: #tabuleiro não válido
            print("Erro: Tabuleiro não válido.")
    
    
    def do_validar(self, arg):    
        " - comando validar que testa a consistência do puzzle e verifica se o tabuleiro está válido: validar \n"
        try:
            lista_arg = arg.split() #separa os argumentos pelos espaços
            num_args = len(lista_arg) #nº argumentos
            if num_args==0: # se não houver argumentos
                if eng.tabuleiro_valido(): #se tabuleiro existente e válido e nenhum argumento for definido
                    print("Tabuleiro válido; Solução possível.")
                else: #se tabuleiro não válido
                    print("Erro: Tabuleiro não válido; nenhuma solução possível")
                self.do_ver(' ') # mostra graficamente o tabuleiro
            else: print("Erro: o comando validar não requer argumentos.") # caso se tente colocar argumentos
        except: 
            print("Erro: no validar.")    
    
    
    def do_ajuda(self, arg):    
        " - comando ajuda que indica a próxima casa lógica a ser jogada (sem indicar a peça a ser colocada): ajuda  \n"   
        try:
            lista_arg = arg.split() #separa os argumentos pelos espaços
            num_args = len(lista_arg) #nº argumentos
            if num_args==0: # se não houver argumentos
                if eng.tabuleiro_valido(): #se tabuleiro existente e válido
                    sug=eng.ajuda_jogada() # retorna uma possível próxima jogada
                    if sug==[-1,-1]: #se o retorno for este, não há jogadas possíveis
                        print("Erro: Sugestão não encontrada.")
                        self.do_ver(' ') # mostra graficamente o tabuleiro
                    else:
                        print("Sugestão: ", (sug[0]+1), " ", (sug[1]+1))
                        global mostrar_ajuda, linha_ajuda, coluna_ajuda
                        mostrar_ajuda=1
                        linha_ajuda=sug[0]+1
                        coluna_ajuda=sug[1]+1
                        self.do_ver(' ') # mostra graficamente o tabuleiro                      
                else: #se tabuleiro não válido
                    print("Erro: Tabuleiro não válido; nenhuma solução possível")
                eng.printpuzzle() #imprime tabuleiro
            else: print("Erro: o comando ajuda não requer argumentos.") # caso se tente colocar argumentos
        except: print("Erro: no ajuda.")
            
    
    def do_undo(self, arg):    
        " - comando para anular movimentos (retroceder no jogo): undo \n"
        lista_arg = arg.split() #separa os argumentos pelos espaços
        num_args = len(lista_arg) #nº argumentos
        if num_args==0: # se não houver argumentos
            if eng.gettabuleiro!=[]: #se tabuleiro existente
                try: eng.return_undo() #volta à jogada anterior
                except: print("Erro: no undo.")
                else:
                    eng.printpuzzle() #imprime tabuleiro
                    self.do_ver(' ') # mostra graficamente o tabuleiro
            else: print("Erro: nenhum tabuleiro carregado.")
        else: print("Erro: o comando undo não requer argumentos.") # caso se tente colocar argumentos
    
    
    def do_resolver(self, arg):    
        " - comando para resolver o puzzle: resolver \n"
        lista_arg = arg.split() #separa os argumentos pelos espaços
        num_args = len(lista_arg) #nº argumentos
        if num_args==0: # se não houver argumentos
            try: 
                eng.def_resolver_auto() #resolução automática
                self.do_ver(' ') # mostra graficamente o tabuleiro
            except:print("Erro: no resolver.")
        else: print("Erro: o comando resolver não requer argumentos.") # caso se tente colocar argumentos
 
    
    def do_ancora(self, arg):    
        " - comando âncora que deve guardar o ponto em que está o jogo para permitir mais tarde voltar a este ponto: ancora \n" 
        lista_arg = arg.split() #separa os argumentos pelos espaços
        num_args = len(lista_arg) #nº argumentos
        if num_args==0: # se não houver argumentos
            try:eng.nova_ancora() #guarda uma ancora
            except:print("Erro: ao definir a ancora.")
            else:eng.printpuzzle() #imprime tabuleiro
        else: print("Erro: o comando ancora não requer argumentos.") # caso se tente colocar argumentos
    
    
    def do_undoancora(self, arg):    
        " - comando undo para voltar à última ancora registada: undoancora \n"  
        lista_arg = arg.split() #separa os argumentos pelos espaços
        num_args = len(lista_arg) #nº argumentos
        if num_args==0: # se não houver argumentos
            try: eng.volta_unancora() #retorna o tabuleiro à ancora anterior
            except: print("Erro: ao definir a ancora.")
            else: 
                eng.printpuzzle()
                self.do_ver(' ') # mostra graficamente o tabuleiro
        else: print("Erro: o comando undoancora não requer argumentos.") # caso se tente colocar argumentos
            
    
    def do_gerar(self, arg):    
        " - comando gerar que gera puzzles com solução única e leva três números inteiros como parâmetros: o nível de dificuldade (1 para ‘fácil’ e 2 para ‘difícil’), o número de linhas e o número de colunas do puzzle \n"
        try:
            lista_arg = arg.split() #separa os argumentos pelos espaços
            num_args = len(lista_arg) #nº argumentos, que deverá ser o nível de dificuldade (1 para ‘fácil’ e 2 para ‘difícil’), o número de linhas e o número de colunas do puzzle
            if num_args == 3:
                dific=int(lista_arg[0]) # primeiro argumento é a dificuldade do jogo
                linha=int(lista_arg[1]) # 2º argumento é o nº de linhas do novo tabuleiro
                coluna=int(lista_arg[2])  # 3º argumento é o nº de colunas do novo tabuleiro
                eng.gerar_tabuleiro(dific,linha,coluna) #gera o tabuleiro
            else: print("Erro: Nº de argumentos inválido.")
        except:print("Erro: no gerar.")

    def do_ver(self, arg):    #arg=0 porque a verificacao do nº de argumentos faz com que haja err
        " - Comando para visualizar graficamente o estado atual do GandaGalo caso seja válido: VER  \n"
        try:
            lista_arg = arg.split() #separa os argumentos pelos espaços
            num_args = len(lista_arg) #nº argumentos, que deverá ser o nível de dificuldade (1 para ‘fácil’ e 2 para ‘difícil’), o número de linhas e o número de colunas do puzzle
            if num_args == 0:
                global janela, ajuda  # pois pretendo atribuir um valor a um identificador global
                if janela is not None: del janela  # invoca o metodo destruidor de instancia __del__()
                if eng.gettabuleiro() !=[]: #existe tabuleiro aberto
                    janela = GandaGaloWindow(40, eng.getlinhas(), eng.getcolunas()) #cria instancia janela
                    janela.mostraJanela(eng.gettabuleiro()) #mostrar tabuleiro
                    try:
                        global mostrar_ajuda
                        if mostrar_ajuda == 1: # se for usado no comando ajuda
                            global linha_ajuda, coluna_ajuda #chama as variáveis globais que irão informar as coordenadas da ajuda
                            janela.desenhaCasaIluminada(coluna_ajuda,linha_ajuda) # por no local iluminado da jogada que é sugerida para a ajuda 
                            del linha_ajuda, coluna_ajuda #elimina estas variáveis globais com 
                        del mostrar_ajuda # elimina variável global com __de__
                    except: pass
                else: print("Erro: nenhum tabuleiro aberto.")
            else: print("Erro: Nº de argumentos inválido.")
        except: print("ERRO: no ver.")
        

    def do_sair(self, arg):
        "Sair do programa GandaGalo: sair"
        print('Obrigado por ter utilizado o Gandagalo, espero que tenha sido divertido!')
        global janela # pois pretendo atribuir um valor a um identificador global
        try:
            if janela is not None: del janela #invoca o destruidor __de__ da janela
        except: pass
        return True
    

if __name__ == '__main__':
    eng = GandaGaloEngine()
    janela = None
    sh = GandaGaloShell()
    sh.cmdloop()
    
'''


'''

