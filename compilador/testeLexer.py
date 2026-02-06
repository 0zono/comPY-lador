from lexer.Lexer import Lexer


def ler_arquivo(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    codigo = ler_arquivo("pog.py")
    lexer = Lexer(codigo)

    print("Tokens encontrados:\n")
    while True:
        token = lexer.nextToken()
        print(token.exibir())
        if token.type == "EOF":
            break


if __name__ == "__main__":
    main()
