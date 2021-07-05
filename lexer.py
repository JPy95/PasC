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
        if (self.lookahead.decode('ascii') != ''):
            self.file.seek(self.file.tell() - 1)
            self.n_column -= 1

    def printTS(self):
        self.ts.printTS()

    def calcularColuna(self, coluna, lexema):
        return coluna - len(lexema)

    def proxToken(self):
        estado = 1
        lexema = ""
        c = '\u0000'

        while True:
            self.lookahead = self.file.read(1)
            try:
                c = self.lookahead.decode('ascii')
            except:
                self.sinalizaErroLexico("Caractere nao ASCII na linha " +
                                        str(self.n_line) + " e coluna " + str(self.n_column))
                return None

            if c == '\t':
                self.n_column += 3
            elif c != '':
                self.n_column += 1
            if c == '\n':
                self.n_line += 1
                self.n_column = 1

            if estado == 1:
                if c == '':
                    return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
                elif c == ' ' or c == '\n' or c == '\t' or c == '\r':
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
                elif c == '"':
                    estado = 29
                elif c.isalpha():
                    lexema += c
                    estado = 26
                elif c.isdigit():
                    lexema += c
                    estado = 31
                else:
                    self.retornaPonteiro()
                    self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
                                            str(self.n_line) + " e coluna " + str(self.n_column))
                    return None

            elif estado == 2:
                self.retornaPonteiro()
                return Token(Tag.OP_AD, "+", self.n_line, self.calcularColuna(self.n_column, "+"))
            elif estado == 3:
                self.retornaPonteiro()
                return Token(Tag.OP_MIN, "-", self.n_line, self.calcularColuna(self.n_column, "-"))
            elif estado == 4:
                self.retornaPonteiro()
                return Token(Tag.SMB_OBC, "{", self.n_line, self.calcularColuna(self.n_column, "{"))
            elif estado == 5:
                self.retornaPonteiro()
                return Token(Tag.SMB_CBC, "}", self.n_line, self.calcularColuna(self.n_column, "}"))
            elif estado == 6:
                self.retornaPonteiro()
                return Token(Tag.SMB_OPA, "(", self.n_line, self.calcularColuna(self.n_column, "("))
            elif estado == 7:
                self.retornaPonteiro()
                return Token(Tag.SMB_CPA, ")", self.n_line, self.calcularColuna(self.n_column, ")"))
            elif estado == 8:
                self.retornaPonteiro()
                return Token(Tag.SMB_COM, ",", self.n_line, self.calcularColuna(self.n_column, ","))
            elif estado == 9:
                self.retornaPonteiro()
                return Token(Tag.SMB_SEM, ";", self.n_line, self.calcularColuna(self.n_column, ";"))
            elif estado == 10:
                if c == '/':
                    estado = 12
                elif c == '*':
                    estado = 35
                else:
                    self.retornaPonteiro()
                    return Token(Tag.OP_DIV, "/", self.n_line, self.calcularColuna(self.n_column, "/"))
            elif estado == 12:
                if c == '\n' or c == "":
                    estado = 1
            elif estado == 13:
                self.retornaPonteiro()
                return Token(Tag.OP_MUL, "*", self.n_line, self.calcularColuna(self.n_column, "*"))
            elif estado == 16:
                if c == '=':
                    return Token(Tag.OP_EQ, "==", self.n_line, self.calcularColuna(self.n_column, "=="))

                self.retornaPonteiro()
                return Token(Tag.OP_ATRIB, "=", self.n_line, self.calcularColuna(self.n_column, "="))
            elif estado == 19:
                if (c == '='):
                    return Token(Tag.OP_NE, "!=", self.n_line, self.calcularColuna(self.n_column, "!="))

                self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
                                        str(self.n_line) + " e coluna " + str(self.n_column))
                return None
            elif estado == 21:
                if (c == '='):
                    return Token(Tag.OP_GE, ">=", self.n_line, self.calcularColuna(self.n_column, ">="))

                self.retornaPonteiro()
                return Token(Tag.OP_GT, ">", self.n_line, self.calcularColuna(self.n_column, ">"))
            elif estado == 24:
                if (c == '='):
                    return Token(Tag.OP_LE, "<=", self.n_line, self.calcularColuna(self.n_column, "<="))

                self.retornaPonteiro()
                return Token(Tag.OP_LT, "<", self.n_line, self.calcularColuna(self.n_column, "<"))
            elif estado == 26:
                if (c.isalnum()):
                    lexema += c
                else:
                    self.retornaPonteiro()
                    token = self.ts.getToken(lexema.lower())
                    if (token is None):

                        token = Token(Tag.ID, lexema, self.n_line, self.calcularColuna(self.n_column, lexema))
                        self.ts.addToken(lexema, token)

                    else:
                        token.linha = self.n_line
                        token.coluna = self.calcularColuna(self.n_column, lexema)

                    return token
            elif estado == 29:
                if c != '"':
                    if c == '\r' or c == '\n' or c == '':
                        self.sinalizaErroLexico("Erro de sintaxe [" + lexema + "] na linha " +
                                                str(self.n_line) + " e coluna " + str(self.n_column))
                        lexema = ''
                        estado = 1
                        return None
                    lexema += c
                else:
                    estado = 1
                    return Token(Tag.CHAR_CONST, lexema, self.n_line, self.calcularColuna(self.n_column - 2, lexema))
            elif estado == 31:
                if c.isdigit():
                    lexema += c
                elif c == '.':
                    lexema += c
                else:
                    self.retornaPonteiro()
                    return Token(Tag.NUM_CONST, lexema, self.n_line, self.calcularColuna(self.n_column, lexema))
            elif estado == 35:
                if c == '*':
                    estado = 36
                elif c == "":
                    self.sinalizaErroLexico("Erro de sintaxe na linha " +
                                            str(self.n_line) + " e coluna " + str(self.n_column))
                    return None
            elif estado == 36:
                if c == '/':
                    estado = 1
                elif c == '*':
                    estado = 36
                elif c == "":
                    self.sinalizaErroLexico("Erro de sintaxe na linha " +
                                            str(self.n_line) + " e coluna " + str(self.n_column))
                    return None
                else:
                    estado = 35
