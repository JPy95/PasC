import sys
import copy

from tag import Tag
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
        if self.token.getNome() == t:
            self.advance()
            return True
        else:
            self.sinalizaErroSintatico("token esperado " + t.tagNome())
            return False

    def prog(self):
        self.eat(Tag.KW_PROGRAM)
        self.lexer.ts.setType(self.token.lexema, Tag.TIPO_VAZIO)
        self.eat(Tag.ID)
        self.body()
        self.eat(Tag.EOF)

    def body(self):
        self.declList()
        self.eat(Tag.SMB_OBC)
        self.stmtList()
        self.eat(Tag.SMB_CBC)

    def declList(self):
        if self.token.getNome() == Tag.KW_NUM or self.token.getNome() == Tag.KW_CHAR:
            self.decl()
            self.eat(Tag.SMB_SEM)
            self.declList()

    def stmtList(self):
        if self.conferirToken([Tag.ID, Tag.KW_IF, Tag.KW_WHILE, Tag.KW_READ, Tag.KW_WRITE]):
            self.stmt()
            self.eat(Tag.SMB_SEM)
            self.stmtList()

    def decl(self):
        self.idList(self.type())

    def type(self):
        type = No()
        if self.conferirToken([Tag.KW_NUM]):
            type.tipo = Tag.TIPO_NUMERO
            self.advance()
        elif self.conferirToken([Tag.KW_CHAR]):
            type.tipo = Tag.TIPO_LITERAL
            self.advance()
        else:
            self.sinalizaErroSintatico("Aguardando 'num' ou 'char'")
        return type

    def idList(self, tipo):
        if self.conferirToken([Tag.ID]):
            self.lexer.ts.setType(self.token.lexema, tipo.tipo)
            self.advance()
        self.idListLinha(tipo)

    def idListLinha(self, tipo):
        if self.conferirToken([Tag.SMB_COM]):
            self.advance()
            self.idList(tipo)

    def stmtList(self):
        if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_READ or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE:
            self.stmt()
            self.eat(Tag.SMB_SEM)
            self.stmtList()

    def stmt(self):
        if self.token.getNome() == Tag.ID:
            self.assignStmt()
        elif self.token.getNome() == Tag.KW_IF:
            self.ifStmt()
        elif self.token.getNome() == Tag.KW_WHILE:
            self.whileStmt()
        elif self.token.getNome() == Tag.KW_READ:
            self.readStmt()
        elif self.token.getNome() == Tag.KW_WRITE:
            self.writeStmt()
        else:
            self.sinalizaErroSintatico("Comando inválido'")

    def writeStmt(self):
        self.eat(Tag.KW_WRITE)
        tipo = self.simpleExpr().tipo

        if tipo == Tag.TIPO_LITERAL and tipo == Tag.TIPO_NUMERO:
            self.sinalizaErroSemantico("Imcompatibilidade para a impressão de valores")

    def readStmt(self):
        self.eat(Tag.KW_READ)
        if self.conferirToken([Tag.ID]):
            if self.lexer.ts.idIsNull(self.token.lexema):
                self.sinalizaErroSemantico("Identificador não declarado")
            self.advance()

    def whileStmt(self):
        self.stmtPrefix()
        self.eat(Tag.SMB_OBC)
        self.stmtList()
        self.eat(Tag.SMB_CBC)

    def ifStmt(self):
        self.eat(Tag.KW_IF)
        self.eat(Tag.SMB_OPA)
        expression = self.expression()
        if expression.tipo != Tag.TIPO_LOGICO:
            self.sinalizaErroSemantico("Expressão lógica mal formada")
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
        tokenTemp = copy.copy(self.token)
        if self.conferirToken([Tag.ID]):
            if self.lexer.ts.idIsNull(self.token.lexema):
                self.sinalizaErroSemantico("Identificador não foi declarado: " + self.token.lexema)
            self.advance()
        if self.eat(Tag.OP_ATRIB):
            simpleExpr = self.simpleExpr()
            if simpleExpr.tipo != tokenTemp.tipo:
                self.sinalizaErroSemantico("Atribuição imcompatível")

    def stmtPrefix(self):
        self.eat(Tag.KW_WHILE)
        self.eat(Tag.SMB_OPA)
        express = self.expression()
        self.eat(Tag.SMB_CPA)
        if express.tipo != Tag.TIPO_LOGICO:
            self.sinalizaErroSemantico("Expressão lógica mal formada")

    def expression(self):
        noExp = No()
        noSimpleExp = self.simpleExpr()
        noExpLinha = self.expressionLinha()
        if noExpLinha.tipo == Tag.TIPO_VAZIO:
            noExp.tipo = noSimpleExp.tipo
        elif noExpLinha.tipo == noSimpleExp.tipo and noSimpleExp.tipo == Tag.TIPO_LOGICO:
            noExp.tipo = Tag.TIPO_LOGICO
        else:
            noExp.tipo = Tag.TIPO_ERRO
        return noExp

    def simpleExpr(self):
        simpExp = No()
        term = self.term()
        simExpLinha = self.simpleExprLinha()
        if simExpLinha.tipo == Tag.TIPO_VAZIO:
            simpExp.tipo = term.tipo
        elif simExpLinha.tipo == term.tipo and simExpLinha.tipo == Tag.TIPO_NUMERO:
            simpExp.tipo = Tag.TIPO_LOGICO
        else:
            simpExp.tipo = Tag.TIPO_ERRO
        return simpExp

    def term(self):
        term = No()
        factoB = self.factorB()
        termLinha = self.termLinha()
        if termLinha.tipo == Tag.TIPO_VAZIO:
            term.tipo = factoB.tipo
        elif termLinha.tipo == factoB.tipo and termLinha.tipo == Tag.TIPO_NUMERO:
            term.tipo = Tag.TIPO_NUMERO
        else:
            term.tipo = Tag.TIPO_ERRO
        return term

    def simpleExprLinha(self):
        simpleExprLinha = No()
        if self.conferirToken([Tag.OP_EQ, Tag.OP_GT, Tag.OP_GE, Tag.OP_LT, Tag.OP_LE, Tag.OP_NE]):
            self.relop()
            term = self.term()
            simpleExprLinhaFilho = self.simpleExprLinha()
            if simpleExprLinhaFilho.tipo == Tag.TIPO_VAZIO and term.tipo == Tag.TIPO_NUMERO:
                simpleExprLinha.tipo = Tag.TIPO_NUMERO
            elif simpleExprLinhaFilho.tipo == term.tipo and term.tipo == Tag.TIPO_NUMERO:
                simpleExprLinha.tipo = Tag.TIPO_NUMERO
            else:
                simpleExprLinha.tipo = Tag.TIPO_ERRO
        return simpleExprLinha

    def factorB(self):
        factorB = No()
        factorA = self.factorA()
        factorBLinha = self.factorBLinha()
        if factorBLinha.tipo == Tag.TIPO_VAZIO:
            factorB.tipo = factorA.tipo
        elif factorBLinha.tipo == factorA.tipo and factorBLinha.tipo == Tag.TIPO_NUMERO:
            factorB.tipo = Tag.TIPO_NUMERO
        else:
            factorB.tipo = Tag.TIPO_ERRO
        return factorB

    def termLinha(self):
        termLinha = No()
        if self.conferirToken([Tag.OP_AD, Tag.OP_MIN]):
            self.addOp()
            factorB = self.factorB()
            termLinhaFilho = self.termLinha()
            if termLinhaFilho.tipo == Tag.TIPO_VAZIO and factorB.tipo == Tag.TIPO_NUMERO:
                termLinha.tipo = Tag.TIPO_NUMERO
            elif termLinhaFilho == factorB.tipo and factorB.tipo == Tag.TIPO_NUMERO:
                termLinha.tipo = Tag.TIPO_NUMERO
            else:
                termLinha.tipo = Tag.TIPO_ERRO
        return termLinha

    def expressionLinha(self):
        expLinha = No()
        if self.conferirToken([Tag.KW_OR, Tag.KW_AND]):
            self.logop()
            simpleExpres = self.simpleExpr()
            exprLinhaFilho = self.expressionLinha()
            if exprLinhaFilho.tipo == Tag.TIPO_VAZIO and simpleExpres.tipo == Tag.TIPO_LOGICO:
                expLinha.tipo = Tag.TIPO_LOGICO
            elif exprLinhaFilho.tipo == simpleExpres.tipo and simpleExpres.tipo == Tag.TIPO_LOGICO:
                expLinha.tipo = Tag.TIPO_LOGICO
            else:
                expLinha.tipo = Tag.TIPO_ERRO
        return expLinha

    def addOp(self):
        if self.conferirToken([Tag.OP_AD, Tag.OP_MIN]):
            self.advance()
        else:
            self.sinalizaErroSintatico("Operação inválida")

    def logop(self):
        if self.conferirToken([Tag.KW_OR, Tag.KW_AND]):
            self.advance()
        else:
            self.sinalizaErroSintatico("Esperado 'or' ou 'and'")

    def factor(self):
        factor = No()
        if self.conferirToken([Tag.ID]):
            factor.tipo = self.lexer.ts.getType(self.token.lexema)
            self.advance()
        elif self.conferirToken([Tag.SMB_OPA]):
            self.eat(Tag.SMB_OPA)
            factor = self.expression()
            self.eat(Tag.SMB_CPA)
        elif self.conferirToken([Tag.NUM_CONST, Tag.CHAR_CONST]):
            factor = self.constant()
        else:
            self.sinalizaErroSintatico("Fator inválido")
        return factor

    def factorA(self):
        factorA = No()
        if self.conferirToken([Tag.KW_NOT]):
            self.advance()
            factor = self.factor()
            if factor.tipo != Tag.TIPO_LOGICO:
                factorA.tipo = Tag.TIPO_ERRO
            else:
                factorA.tipo = Tag.TIPO_LOGICO
        else:
            factor = self.factor()
            factorA.tipo = factor.tipo

        return factorA

    def constant(self):
        constant = No()
        if self.conferirToken([Tag.NUM_CONST]):
            constant.tipo = Tag.TIPO_NUMERO
            self.advance()
        elif self.conferirToken([Tag.CHAR_CONST]):
            constant.tipo = Tag.TIPO_LITERAL
            self.advance()
        else:
            self.sinalizaErroSintatico("Constante esperada'")
        return constant

    def factorBLinha(self):
        factorBlinha = No()
        if self.conferirToken([Tag.OP_DIV, Tag.OP_MUL]):
            self.mulop()
            factorA = self.factorA()
            factorBlinhaFilho = self.factorBLinha()
            if factorBlinhaFilho.tipo == Tag.TIPO_VAZIO and factorA.tipo == Tag.TIPO_NUMERO:
                factorBlinha.tipo = Tag.TIPO_NUMERO
            elif factorBlinhaFilho.tipo == factorA.tipo and factorA.tipo == Tag.TIPO_NUMERO:
                factorBlinha.tipo = Tag.TIPO_NUMERO
            else:
                factorBlinha.tipo = Tag.TIPO_ERRO
        return factorBlinha

    def mulop(self):
        if self.conferirToken([Tag.OP_MUL, Tag.OP_DIV]):
            self.advance()
        else:
            self.sinalizaErroSintatico("Operador inválido, utilize * ou /")

    def relop(self):
        relop = No
        if self.conferirToken([Tag.OP_EQ, Tag.OP_GT, Tag.OP_GE, Tag.OP_LT, Tag.OP_LE, Tag.OP_NE]):
            self.advance()
        else:
            self.sinalizaErroSintatico("Aguardando operador")
        return relop

    def conferirToken(self, lista):
        return self.token.getNome() in lista
