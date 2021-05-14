import sys

from ts import TS
from tag import Tag
from token import Token

class Lexer:

  def __init__(self, file):
    try:
      self.file = open(file, 'rb')
      self.lookahead = 0
      self.n_line = 1
      self.n_column = 0
      self.ts = TS()
    except IOError:
      print('Erro de abertura do arquivo. Encerrando.')
      sys.exit(0)

  def closeFile(self):
    try:
      self.file.close()
    except IOError:
      print('Erro ao fechar arquivo. Encerrando.')
      sys.exit(0)

  def sinalizaErroLexico(self, message):
    print("[Erro Lexico]: ", message, "\n")
  
  def retornaPonteiro(self):
    if(self.lookahead.decode('ascii') != ''):
      self.file.seek(self.file.tell()-1)
      self.n_column -= 1

  def printTS(self):
    self.ts.printTS()

  def proxToken(self):
    estado = 1
    lexema = ""
    c = '\u0000'

    while(True):
      self.lookahead = self.file.read(1)
      c = self.lookahead.decode('ascii')
      
      if c != '':
        self.n_column += 1 

      if estado == 1:
        if c == '':
          return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
        elif c in [' ','\n','\t','\r']:
          if c == '\n':
            self.n_column = 1
            self.n_line += 1
          estado = 1
        elif c == '+':
          estado = 2
        elif c == '-':
          estado = 3
        elif c == '{':
          estado = 4
        elif c == '}':
          estado = 5
        elif c == '(':
          estado = 6
        elif c == ')':
          estado = 7
        elif c == ',':
          estado = 8
        elif c == ';':
          estado = 9
        elif c == '/':
          estado = 10
        elif c == '*':
          estado = 13
        elif c == '=':
          estado = 16
        elif c == '!':
          estado = 19
        elif c == '>':
          estado = 21
        elif c == '<':
          estado = 24
        else:
          self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
          str(self.n_line) + " e coluna " + str(self.n_column))
          return None
      
      elif estado == 2:
        return Token(Tag.OP_AD, "+", self.n_line, self.n_column)
      elif estado == 3:
        return Token(Tag.OP_MIN, "-", self.n_line, self.n_column)
      elif estado == 4:
        return Token(Tag.SMB_OBC, "{", self.n_line, self.n_column)
      elif estado == 5:
        return Token(Tag.SMB_CBC, "}", self.n_line, self.n_column)
      elif estado == 6:
        return Token(Tag.SMB_OPA, "(", self.n_line, self.n_column)
      elif estado == 7:
        return Token(Tag.SMB_CPA, ")", self.n_line, self.n_column)
      elif estado == 8:
        return Token(Tag.SMB_COM, ",", self.n_line, self.n_column)
      elif estado == 9:
        return Token(Tag.SMB_SEM, ";", self.n_line, self.n_column)
      elif estado == 10:
        print(c)
        if c in ['/','*']:
          c = '\n'

        self.retornaPonteiro()
        return Token(Tag.OP_DIV, "/", self.n_line, self.n_column)

      elif estado == 16:
        if c == '=':
          return Token(Tag.OP_EQ, "==", self.n_line, self.n_column)
        
        self.retornaPonteiro()
        return Token(Tag.OP_ATRIB, "=", self.n_line, self.n_column)
      elif estado == 19:
        if(c == '='):
          return Token(Tag.OP_NE, "!=", self.n_line, self.n_column)

        self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
        str(self.n_line) + " e coluna " + str(self.n_column))
        return None
      elif estado == 21:
        if(c == '='):
          return Token(Tag.OP_GE, ">=", self.n_line, self.n_column)

        self.retornaPonteiro()
        return Token(Tag.OP_GT, ">", self.n_line, self.n_column)
      elif estado == 24:
        if(c == '='):
          return Token(Tag.OP_LE, "<=", self.n_line, self.n_column)

        self.retornaPonteiro()
        return Token(Tag.OP_LT, "<", self.n_line, self.n_column)
      













            