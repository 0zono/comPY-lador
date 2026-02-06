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

    # 1. Leitura do código fonte
    codigo = ler_arquivo(arquivo_fonte)
    print("\n[1] Código fonte carregado")

    # 2. Analisador Léxico
    lexer = Lexer(codigo)
    print("[2] Lexer criado")

    # 3. Analisador Sintático + Semântico
    parser = Parser(lexer)
    print("[3] Parser criado (com análise semântica)")

    # Aqui ocorre TODA a validação sintática e semântica
    parser.programa()
    print("[4] Análise sintática e semântica OK")

    # 4. Gerador de código
    gerador = GeradorCodigo()
    print("[5] Gerador de código criado")

    # ⚠️ AQUI DEPENDE DO SEU PARSER
    # Se no futuro o parser retornar uma AST ou lista de comandos:
    #
    # programa_intermediario = parser.ast
    # gerador.gerar_programa(programa_intermediario)
    #
    # Por enquanto, você pode deixar isso como placeholder:
    print("[6] (Placeholder) Geração de código ainda não integrada ao parser")

    # 5. Salva código objeto
    gerador.salvar(arquivo_objeto)

    # 6. Exibe código gerado (opcional)
    gerador.exibir()

    print("\n✓ COMPILAÇÃO FINALIZADA COM SUCESSO")
    print("=" * 60)


if __name__ == "__main__":
    # Arquivos de teste
    arquivo_fonte = "pog.py"
    arquivo_objeto = "programa1.obj"

    compilar(arquivo_fonte, arquivo_objeto)
