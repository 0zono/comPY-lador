from lexer.Lexer import Lexer
from lexer.Token import Token


def main():
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
