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
      self.n_column += 1

      if estado == 1:
        if c == '':
          return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
        elif c == '\n':
          self.n_column = 1
          self.n_line += 1
        elif c in [' ','\t','\r']:
          estado = 1
            