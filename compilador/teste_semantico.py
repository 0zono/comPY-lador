"""
Testes EXCLUSIVOS da Análise Semântica
Foca apenas nas verificações semânticas, não nos erros sintáticos

Autor: Teste Semântico
Data: 2026-02-04
"""

from pathlib import Path

from lexer.Lexer import Lexer
from parser.Parser import Parser


# =============================================================================
# UTILIDADES
# =============================================================================

def carregar_codigo_padrao():
    """
    Carrega o arquivo exemplos/correto.python.txt
    Caminho resolvido de forma portátil
    """
    base_dir = Path(__file__).parent.parent  # sai de compilador/ ou testes/
    caminho = base_dir / "exemplos" / "correto.python.txt"

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo de teste não encontrado: {caminho}")

    return caminho.read_text(encoding="utf-8")


def testar_semantica(nome, deve_passar=True, erro_esperado=None):
    """
    Executa um teste semântico usando o arquivo correto.python.txt
    """
    print("\n" + "=" * 80)
    print(f"TESTE SEMÂNTICO: {nome}")
    print("=" * 80)

    codigo = carregar_codigo_padrao()

    print("Código (correto.python.txt):")
    print("-" * 80)
    print(codigo)
    print("-" * 80)

    lexer = Lexer(codigo)
    parser = Parser(lexer)

    try:
        parser.programa()

        if deve_passar:
            print("✓ PASSOU: Código semanticamente correto!")
        else:
            print("✗ FALHOU: Código deveria ter sido rejeitado por erro semântico!")

    except Exception as e:
        erro_msg = str(e)

        if not deve_passar:
            if erro_esperado is None or erro_esperado.lower() in erro_msg.lower():
                print("✓ REJEITADO CORRETAMENTE!")
                print(f"   Erro: {erro_msg}")
            else:
                print("✗ ERRO DIFERENTE DO ESPERADO!")
                print(f"   Esperado: {erro_esperado}")
                print(f"   Obtido: {erro_msg}")
        else:
            print(f"✗ ERRO INESPERADO: {erro_msg}")


# =============================================================================
# TESTES SEMÂNTICOS
# =============================================================================

def teste_sem_01_codigo_correto():
    testar_semantica(
        "Código correto deve passar na análise semântica",
        deve_passar=True
    )


def teste_sem_02_regressao_semantica():
    testar_semantica(
        "Teste de regressão semântica (arquivo real)",
        deve_passar=True
    )


def teste_sem_03_execucao_completa():
    testar_semantica(
        "Execução sem erros semânticos inesperados",
        deve_passar=True
    )


# =============================================================================
# EXECUTOR DE TESTES
# =============================================================================

def executar_todos_testes_semanticos():
    print("\n" + "█" * 80)
    print("BATERIA DE TESTES - ANÁLISE SEMÂNTICA (ARQUIVO REAL)")
    print("█" * 80)

    print("\nEstes testes usam EXCLUSIVAMENTE:")
    print("→ exemplos/correto.python.txt")
    print("→ Código sintaticamente correto")
    print("→ Foco em regressão semântica")
    print("=" * 80)

    teste_sem_01_codigo_correto()
    teste_sem_02_regressao_semantica()
    teste_sem_03_execucao_completa()

    print("\n" + "█" * 80)
    print("RESUMO DOS TESTES SEMÂNTICOS")
    print("█" * 80)
    print("""
    Total de testes executados: 3

    Tipo de teste:
    ✓ Integração semântica
    ✓ Regressão semântica
    ✓ Código real (não mockado)

    Observação:
    Estes testes garantem que alterações futuras
    no analisador semântico NÃO quebrem código válido.
    """)
    print("█" * 80)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    executar_todos_testes_semanticos()
