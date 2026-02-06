from lexer.Lexer import Lexer
from parser.Parser import Parser
from gerador.gerador_cod import GeradorCodigo


def ler_arquivo(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()


def compilar(arquivo_fonte, arquivo_objeto):
    print("=" * 60)
    print("INICIANDO COMPILAÇÃO")
    print("=" * 60)

    # 1. Código fonte
    codigo = ler_arquivo(arquivo_fonte)
    print("\n[1] Código fonte carregado")

    # 2. Lexer
    lexer = Lexer(codigo)
    print("[2] Lexer criado")

    # 3. Parser (sintático + semântico)
    parser = Parser(lexer)
    print("[3] Parser criado")

    parser.programa()
    print("[4] Análise sintática e semântica OK")

    # 4. Gerador
    gerador = GeradorCodigo()
    print("[5] Gerador de código criado")

    # 5. AST → Código objeto
    programa_intermediario = parser.ast

    if not programa_intermediario:
        raise Exception("AST vazia — nada para gerar")

    gerador.gerar_programa(programa_intermediario)
    print("[6] Código objeto gerado")

    # 6. Salva e exibe
    gerador.salvar(arquivo_objeto)
    gerador.exibir()

    print("\n✓ COMPILAÇÃO FINALIZADA COM SUCESSO")
    print("=" * 60)


if __name__ == "__main__":
    compilar("pog.py", "programa1.obj")
