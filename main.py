from tag import Tag
from lexer import Lexer
from analisadorParser import AnalisadorParser

if __name__ == "__main__":
    lexer = Lexer('teste.pasc')
    parser = AnalisadorParser(lexer)

    parser.prog()
    parser.lexer.closeFile

    print("\n=>Tabela de simbolos:")
    lexer.printTS()
    lexer.closeFile()

    print('\n=> Fim da compilacao')
