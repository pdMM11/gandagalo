# -*- coding:utf-8 -*-
'''
Created on 1/12/2018

@author: victor Alves
'''

from graphics import *
from tkinter.constants import CENTER

class GandaGaloWindow:
    
    '''
    Classe que cria uma janela para vizualização grafica do estado do GandaGalo
    '''

    def __init__(self, cell_size, linhas, colunas):
        '''
        Cria nova instancia de GandaGaloWindow
        :param cell_size: tamanho da casa no ecra, em pixeis
        :param filename: nome do ficheiro a ler
        '''
        self.cell_size = cell_size
        self.nlinhas = linhas
        self.ncolunas = colunas
        self.puzzle = GraphWin("GandaGalo", self.nlinhas * self.cell_size + self.cell_size, self.ncolunas * self.cell_size + self.cell_size)
        pass   
    
    
    def __del__(self):
        self.puzzle.close()  # fechar a janela
        
    
    def desenhaCasa(self, coluna, linha):
        '''
        Desenha uma casa vazia 
        :param coluna: indice da coluna 
        :param linha: indice da linha
        '''
        p1 = Point(coluna * self.cell_size, linha * self.cell_size)
        p2 = Point(p1.getX() + self.cell_size, p1.getY() + self.cell_size)
        r = Rectangle(p1, p2)
        r.setFill("white")
        r.draw(self.puzzle)
        return r

    
    def desenhaCasaIluminada(self, coluna, linha):
        '''
        Desenha uma casa que esteja iluminada 
        :param coluna: indice da coluna 
        :param linha: indice da linha
        '''
        p1 = Point(coluna * self.cell_size, linha * self.cell_size)
        p2 = Point(p1.getX() + self.cell_size, p1.getY() + self.cell_size)
        r = Rectangle(p1, p2)
        r.setFill("#%02x%02x%02x" % (255, 247, 162))  # cor RGB da luz 
        r.draw(self.puzzle)
    
    def desenhaLampada(self, coluna, linha):
        '''
        Desenha uma casa que contenha  
        :param coluna: indice da coluna 
        :param linha: indice da linha
        '''
        self.desenhaCasaIluminada(coluna, linha)
        
        p1 = Point(coluna * self.cell_size + self.cell_size / 2, linha * self.cell_size + self.cell_size / 2)
        c = Circle(p1, self.cell_size / 3)
        c.setFill("yellow")
        c.draw(self.puzzle)
                    
    def desenhaCasaBloqueada(self, coluna, linha):
        '''
        Desenha uma casa que esteja bloqueada sem conter qualquer numero 
        :param coluna: indice da coluna 
        :param linha: indice da linha
        '''
        p1 = Point(coluna * self.cell_size, linha * self.cell_size)
        p2 = Point(p1.getX() + self.cell_size, p1.getY() + self.cell_size)
        r = Rectangle(p1, p2)
        r.setFill("black")
        r.draw(self.puzzle)
        return r
        
    def desenhaCasaBloqueadaNum(self, coluna, linha, char):
        '''
        Desenha uma casa que esteja bloqueada e contenha um numero
        :param coluna: indice da coluna 
        :param linha: indice da linha
        :param char: caracter numerico a inserir na casa bloqueada
        '''
        r = self.desenhaCasa(coluna, linha)  # aqui aproveitamos o retangulo que definimos para lhe colocar texto centrado
        label = Text(r.getCenter(), char)
        label.setTextColor("black")
        label.setStyle("bold")
        label.setSize(24)
        label.draw(self.puzzle) 
    
    def desenhaCasaMarcada(self, coluna, linha):
        '''
        Desenha uma casa que esteja marcada 
        :param coluna: indice da coluna 
        :param linha: indice da linha
        '''
        self.desenhaCasa(coluna, linha)
        p1 = Point(coluna * self.cell_size + self.cell_size / 2, linha * self.cell_size + self.cell_size / 2)
        
        c = Circle(p1, self.cell_size / 10)
        c.setFill("black")
        c.draw(self.puzzle)

        
    def desenhaLinha(self, x1, y1, x2, y2, espessura, cor):
        '''
        Desenha uma linha
        :param x1: (x1,y1)
        :param y1: (x1,y1)
        :param x2: (x2,y2)
        :param x2: (x2,y2)
        '''    
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        l = Line(p1, p2)
        l.setFill(cor)
        l.setWidth(espessura)
        l.draw(self.janela)
     

    
    def desenhaNumLinha(self, linha):
        '''
        Desenha os numeros das linhas e as linhas horizontais da grelha
        ''' 
        label = Text(Point(0 + self.cell_size / 2, linha * self.cell_size + self.cell_size / 2), str(linha))
        label.setTextColor("black")
        label.draw(self.puzzle)
    
    def desenhaNumsColunas(self, colunas):
        '''
        Desenha os numeros das colunas e as linhas verticais da grelha
        ''' 
        for i in range(1, colunas + 1):
            label = Text(Point(i * self.cell_size + self.cell_size / 2 , self.cell_size / 2), str(i))
            label.setTextColor("black")
            label.draw(self.puzzle)
    
    def mostraJanela(self, matriz):
        '''
        Percorre todo o puzzle, linha a linha e dentro de cada linha coluna a coluna, desenhando cada casa correspondente no puzzle
        '''
        try:
            self.puzzle.delete("all")
            linha = 0
            coluna = 0
            self.desenhaNumsColunas(self.ncolunas)
            for line in matriz:
                for simbolo in line:
                    self.desenhaNumLinha(linha + 1) # para linha 0 aparecer 1, coluna 1 aparecer 2
                    if simbolo == '.':
                        self.desenhaCasa(coluna + 1, linha + 1)
                    elif simbolo == '#':
                        self.desenhaCasaBloqueada(coluna + 1, linha + 1)
                    elif simbolo == 'X':
                        self.desenhaCasaBloqueadaNum(coluna + 1, linha + 1, simbolo)
                    elif simbolo == 'O':
                        self.desenhaCasaBloqueadaNum(coluna + 1, linha + 1, simbolo)
                    else:
                        self.desenhaCasaBloqueadaNum(coluna + 1, linha + 1, column)
                    coluna = coluna + 1
                coluna = 0
                linha = linha + 1
        except BaseException as e:
            print("erro ao desenhar:", e)
            return "NÃO"
        return "SIM"
      

