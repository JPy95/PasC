from enum import Enum


class Tag(Enum):
    '''
   Uma representacao em constante de todos os nomes 
   de tokens para a linguagem.
   '''

    # Fim de arquivo
    EOF = -1

    # Palavras-chave
    KW_PROGRAM = 1
    KW_IF = 2
    KW_ELSE = 3
    KW_WHILE = 4
    KW_WRITE = 6
    KW_READ = 7
    KW_NOT = 8
    KW_OR = 9
    KW_AND = 10
    KW_NUM = 11
    KW_CHAR = 12

    # Operadores
    OP_EQ = 20
    OP_NE = 21
    OP_GT = 22
    OP_LT = 23
    OP_GE = 24
    OP_LE = 25
    OP_AD = 26
    OP_MIN = 27
    OP_MUL = 28
    OP_DIV = 29
    OP_ATRIB = 30

    # Símbolos
    SMB_OBC = 40
    SMB_CBC = 41
    SMB_OPA = 42
    SMB_CPA = 43
    SMB_COM = 44
    SMB_SEM = 45

    # Identificador
    ID = 50

    # Numeros
    NUM_CONST = 61

    # Caracteres
    CHAR_CONST = 71

    # tipos
    TIPO_VAZIO = 1000
    TIPO_LOGICO = 1001
    TIPO_NUMERO = 1002
    TIPO_LITERAL = 1003
    TIPO_ERRO = 1004

    tags_names = {
        1: "program",
        2: "if",
        3: "else",
        4: "while",
        6: "write",
        7: "read",
        8: "not",
        9: "or",
        10: "and",
        11: "num",
        12: "char",
        20: "==",
        21: "!=",
        22: ">",
        23: "<",
        24: ">=",
        25: "<=",
        26: "+",
        27: "-",
        28: "*",
        29: "/",
        30: "=",
        40: "{",
        41: "}",
        42: "(",
        43: ")",
        44: ",",
        45: ";"
    }

    def tagNome(self):
        tags_names = {
            -1: "EOF",
            1: "program",
            2: "if",
            3: "else",
            4: "while",
            6: "write",
            7: "read",
            8: "not",
            9: "or",
            10: "and",
            11: "num",
            12: "char",
            20: "==",
            21: "!=",
            22: ">",
            23: "<",
            24: ">=",
            25: "<=",
            26: "+",
            27: "-",
            28: "*",
            29: "/",
            30: "=",
            40: "{",
            41: "}",
            42: "(",
            43: ")",
            44: ",",
            45: ";",
            50: "ID",
            61: "NUMERICO",
            71: "LITERAL",

        }
        return tags_names[self.value]
