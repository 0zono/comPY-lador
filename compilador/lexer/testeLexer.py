from lexer.Token import Token
from lexer.Lexer import Lexer


def main():
    # cria alguns tokens de teste
    codigo = '2 == 1 != 3 >= 4 <= 5 = b\n "sup bitches" = str'
    lexer = Lexer(codigo)

    print("Tokens encontrados:\n")
    while True:
        token = lexer.nextToken()
        print(token.exibir())
        if token.type == "EOF":
            break

if __name__ == "__main__":
    main()
