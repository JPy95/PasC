import sys
import copy

from tag import Tag
from token1 import Token
from lexer import Lexer
from no import No


class AnalisadorParser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.proxToken()  # Leitura inicial obrigatoria do primeiro simbolo
        if self.token is None:  # erro no Lexer
            sys.exit(0)

    def sinalizaErroSemantico(self, message):
        print("[Erro Semantico] na linha " + str(self.token.getLinha()) + " e coluna " + str(
            self.token.getColuna()) + ": ")
        print(message, "\n")

    def sinalizaErroSintatico(self, message):
        print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(
            self.token.getColuna()) + ": ")
        print(message, "\n")

    def advance(self):
        print("[DEBUG] token: ", self.token.toString())
        self.token = self.lexer.proxToken()
        if self.token is None:  # erro no Lexer
            sys.exit(0)

    def skip(self, message):
        self.sinalizaErroSintatico(message)
        self.advance()

    # verifica token esperado t
    def eat(self, t):
        if (self.token.getNome() == t):
            self.advance()
            return True
        else:
            return False

    def prog(self):
        if (not self.eat(Tag.KW_PROGRAM)):
            self.sinalizaErroSintatico("Esperado 'program'")
        if (not self.eat(Tag.ID)):
            self.sinalizaErroSintatico("Esperando 'identificador'")
        self.body()

    def body(self):
        self.declList()

        if not self.eat(Tag.SMB_OBC):
            self.sinalizaErroSintatico("Esperado '{'")

        self.stmtList()

        if not self.eat(Tag.SMB_CBC):
            self.sinalizaErroSintatico("Esperado '}'")

    def declList(self):
        if self.token.getNome() == Tag.KW_NUM or self.token.getNome() == Tag.KW_CHAR:
            self.decl()
            self.sinalizaErroSintatico("Esperado ';'")
            self.declList()

    def stmtList(self):
        pass

    def decl(self):
        self.type()
        self.idList()

    def type(self):
        if self.eat(Tag.KW_NUM):
            pass
        if self.eat(Tag.KW_CHAR):
            pass
        else:
            self.sinalizaErroSintatico("Aguardando 'num' ou 'char'")

    def idList(self):
        if (not self.eat(Tag.ID)):
            self.sinalizaErroSintatico("Iddentificador inesperado")
        self.idListLinha()

    def idListLinha(self):
        if self.eat(Tag.SMB_COM):
            self.idList()
        elif (self.token.getNome() == Tag.SMB_SEM):
            return
        else:
            self.sinalizaErroSintatico("Esperado ',' ou ';'")

    def stmtList(self):
        if (
                self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_READ or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE):
            self.stmt()
            self.eat(Tag.SMB_SEM)
            self.stmtList()

    def stmt(self):
        if (self.token.getNome() == Tag.ID):
            self.assignStmt()
        elif (self.token.getNome() == Tag.KW_IF):
            self.ifStmt()
        elif (self.token.getNome() == Tag.KW_WHILE):
            self.whileStmt()
        elif (self.token.getNome() == Tag.KW_READ):
            self.readStmt()
        elif (self.token.getNome() == Tag.KW_WRITE):
            self.writeStmt()
        else:
            self.sinalizaErroSintatico("Comando inválido'")

    def writeStmt(self):
        self.eat(Tag.KW_WRITE)
        self.simpleExpr()

    def readStmt(self):
        self.eat(Tag.KW_READ)
        self.eat(Tag.ID)

    def whileStmt(self):
        self.stmtPrefix()
        self.eat(Tag.SMB_OBC)
        self.stmtList()
        self.eat(Tag.SMB_CBC)

    def ifStmt(self):
        self.eat(Tag.KW_IF)
        self.eat(Tag.SMB_OPA)
        self.expression()
        self.eat(Tag.SMB_CPA)
        self.eat(Tag.SMB_OBC)
        self.stmtList()
        self.eat(Tag.SMB_CBC)
        self.ifStmtLinha()

    def ifStmtLinha(self):
        if self.eat(Tag.KW_ELSE):
            self.eat(Tag.SMB_OBC)
            self.stmtList()
            self.eat(Tag.SMB_CBC)

    def assignStmt(self):
        self.eat(Tag.ID)
        self.eat(Tag.OP_ATRIB)
        self.simpleExpr()

    def stmtPrefix(self):
        self.eat(Tag.KW_WHILE)
        self.eat(Tag.SMB_OPA)
        self.expression()
        self.eat(Tag.SMB_CPA)

    def expression(self):
        self.simpleExpr()
        self.expressionLinha()

    def simpleExpr(self):
        self.term()
        self.simpleExprLinha()

    def term(self):
        self.factorB()
        self.termLinha()

    def simpleExprLinha(self):
        pass

    def factorB(self):
        self.factorA()
        self.factorBLinha()

    def termLinha(self):
        if self.conferirToken([Tag.OP_AD, Tag.OP_MIN]):
            self.addOP()
            self.factorB()
            self.termLinha()

    def addOP(self):
        self.eat(Tag.OP_AD)
        self.eat(Tag.OP_MIN)

    def conferirToken(self, lista):
        return self.token.getNome() in lista

    def expressionLinha(self):
        if self.conferirToken([Tag.KW_OR, Tag.KW_AND]):
            
