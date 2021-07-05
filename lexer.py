import sys

from ts import TS
from tag import Tag
from token1 import Token


class Lexer:

    def __init__(self, file):
        try:
            self.file = open(file, 'rb')
            self.lookahead = 0
            self.n_line = 1
            self.n_column = 1
            self.n_columnInicial= 1
            self.n_lineInicial=1
            self.ts = TS()
            self.c = '\u0000'
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
        if self.lookahead.decode('ascii') != '':
            self.file.seek(self.file.tell() - 1)

    def printTS(self):
        self.ts.printTS()


    def proxToken(self):
        estado = 1
        lexema = ""
        self.c = '\u0000'

        while True:
            self.lookahead = self.file.read(1)
            try:
                self.c = self.lookahead.decode('ascii')
            except:
                self.sinalizaErroLexico("Caractere nao ASCII na linha " +
                                        str(self.n_line) + " e coluna " + str(self.n_column))
                return None


            if estado == 1:
                self.n_lineInicial = self.n_line
                self.n_columnInicial = self.n_column
                if self.c == '':
                    return Token(Tag.EOF, "EOF", self.n_lineInicial, self.n_columnInicial)
                elif self.c == ' ' or self.c == '\n' or self.c == '\t' or self.c == '\r':
                    estado = 1
                elif self.c == '+':
                    estado = 2
                elif self.c == '-':
                    estado = 3
                elif self.c == '{':
                    estado = 4
                elif self.c == '}':
                    estado = 5
                elif self.c == '(':
                    estado = 6
                elif self.c == ')':
                    estado = 7
                elif self.c == ',':
                    estado = 8
                elif self.c == ';':
                    estado = 9
                elif self.c == '/':
                    estado = 10
                elif self.c == '*':
                    estado = 13
                elif self.c == '=':
                    estado = 16
                elif self.c == '!':
                    estado = 19
                elif self.c == '>':
                    estado = 21
                elif self.c == '<':
                    estado = 24
                elif self.c == '"':
                    estado = 29
                elif self.c.isalpha():
                    lexema += self.c
                    estado = 26
                elif self.c.isdigit():
                    lexema += self.c
                    estado = 31
                else:
                    self.retornaPonteiro()
                    self.sinalizaErroLexico("Caractere invalido [" + self.c + "] na linha " +
                                            str(self.n_lineInicial) + " e coluna " + str(self.n_columnInicial))
                    return None

            elif estado == 2:
                self.retornaPonteiro()
                return Token(Tag.OP_AD, "+", self.n_lineInicial, self.n_columnInicial)
            elif estado == 3:
                self.retornaPonteiro()
                return Token(Tag.OP_MIN, "-", self.n_lineInicial, self.n_columnInicial)
            elif estado == 4:
                self.retornaPonteiro()
                return Token(Tag.SMB_OBC, "{", self.n_lineInicial, self.n_columnInicial)
            elif estado == 5:
                self.retornaPonteiro()
                return Token(Tag.SMB_CBC, "}", self.n_lineInicial, self.n_columnInicial)
            elif estado == 6:
                self.retornaPonteiro()
                return Token(Tag.SMB_OPA, "(", self.n_lineInicial, self.n_columnInicial)
            elif estado == 7:
                self.retornaPonteiro()
                return Token(Tag.SMB_CPA, ")", self.n_lineInicial, self.n_columnInicial)
            elif estado == 8:
                self.retornaPonteiro()
                return Token(Tag.SMB_COM, ",", self.n_lineInicial, self.n_columnInicial)
            elif estado == 9:
                self.retornaPonteiro()
                return Token(Tag.SMB_SEM, ";", self.n_lineInicial, self.n_columnInicial)
            elif estado == 10:
                if self.c == '/':
                    estado = 12
                elif self.c == '*':
                    estado = 35
                else:
                    self.retornaPonteiro()
                    return Token(Tag.OP_DIV, "/", self.n_lineInicial, self.n_columnInicial)
            elif estado == 12:
                if self.c == '\n' or self.c == "":
                    estado = 1
            elif estado == 13:
                self.retornaPonteiro()
                return Token(Tag.OP_MUL, "*", self.n_lineInicial, self.n_columnInicial)
            elif estado == 16:
                if self.c == '=':
                    return Token(Tag.OP_EQ, "==", self.n_lineInicial, self.n_columnInicial)

                self.retornaPonteiro()
                return Token(Tag.OP_ATRIB, "=", self.n_lineInicial, self.n_columnInicial)
            elif estado == 19:
                if (self.c == '='):
                    return Token(Tag.OP_NE, "!=", self.n_lineInicial, self.n_columnInicial)

                self.sinalizaErroLexico("Caractere invalido [" + self.c + "] na linha " +
                                        str(self.n_lineInicial) + " e coluna " + str(self.n_columnInicial))
                return None
            elif estado == 21:
                if self.c == '=':
                    return Token(Tag.OP_GE, ">=", self.n_lineInicial, self.n_columnInicial)

                self.retornaPonteiro()
                return Token(Tag.OP_GT, ">", self.n_lineInicial, self.n_columnInicial)
            elif estado == 24:
                if self.c == '=':
                    return Token(Tag.OP_LE, "<=", self.n_lineInicial, self.n_columnInicial)

                self.retornaPonteiro()
                return Token(Tag.OP_LT, "<", self.n_lineInicial, self.n_columnInicial)
            elif estado == 26:
                if self.c.isalnum():
                    lexema += self.c
                else:
                    self.retornaPonteiro()
                    token = self.ts.getToken(lexema.lower())
                    if token is None:

                        token = Token(Tag.ID, lexema, self.n_lineInicial, self.n_columnInicial)
                        self.ts.addToken(lexema, token)

                    else:
                        token.linha = self.n_lineInicial
                        token.coluna = self.n_columnInicial

                    return token
            elif estado == 29:
                if self.c != '"':
                    if self.c == '\r' or self.c == '\n' or self.c == '':
                        self.sinalizaErroLexico("Erro de sintaxe [" + lexema + "] na linha " +
                                                str(self.n_lineInicial) + " e coluna " + str(self.n_columnInicial))
                        lexema = ''
                        estado = 1
                        return None
                    lexema += self.c
                else:
                    estado = 1

                    return Token(Tag.CHAR_CONST, lexema, self.n_lineInicial, self.n_columnInicial)
            elif estado == 31:
                if self.c.isdigit():
                    lexema += self.c
                elif self.c == '.':
                    lexema += self.c
                else:
                    self.retornaPonteiro()
                    return Token(Tag.NUM_CONST, lexema, self.n_lineInicial, self.n_columnInicial)
            elif estado == 35:
                if self.c == '*':
                    estado = 36
                elif self.c == "":
                    self.sinalizaErroLexico("Erro de sintaxe na linha " +
                                            str(self.n_lineInicial) + " e coluna " + str(self.n_columnInicial))
                    return None
            elif estado == 36:
                if self.c == '/':
                    estado = 1
                elif self.c == '*':
                    estado = 36
                elif self.c == "":
                    self.sinalizaErroLexico("Erro de sintaxe na linha " +
                                            str(self.n_lineInicial) + " e coluna " + str(self.n_columnInicial))
                    return None
                else:
                    estado = 35
            if self.c == '\t':
                self.n_column += 3
            else:
                self.n_column += 1
            if self.c == '\n':
                self.n_line += 1
                self.n_column = 1
