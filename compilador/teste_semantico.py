"""
Testes EXCLUSIVOS da Análise Semântica
Foca apenas nas verificações semânticas, não nos erros sintáticos

Autor: Teste Semântico
Data: 2026-02-04
"""

import sys
import os

from lexer.Lexer import Lexer
from parser.Parser import Parser


def testar_semantica(nome, codigo, deve_passar=True, erro_esperado=None):
    """
    Executa um teste semântico específico
    
    Args:
        nome: Nome descritivo do teste
        codigo: Código a ser testado
        deve_passar: True se o código é semanticamente correto
        erro_esperado: String que deve aparecer no erro (opcional)
    """
    print("\n" + "=" * 80)
    print(f"TESTE SEMÂNTICO: {nome}")
    print("=" * 80)
    print(f"Código:")
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
            # Verifica se o erro esperado está na mensagem
            if erro_esperado is None or erro_esperado.lower() in erro_msg.lower():
                print(f"✓ REJEITADO CORRETAMENTE!")
                print(f"   Erro: {erro_msg}")
            else:
                print(f"✗ ERRO DIFERENTE DO ESPERADO!")
                print(f"   Esperado: {erro_esperado}")
                print(f"   Obtido: {erro_msg}")
        else:
            print(f"✗ ERRO INESPERADO: {erro_msg}")


# ============================================================================
# TESTES SEMÂNTICOS - VARIÁVEIS
# ============================================================================

def teste_sem_01_variavel_nao_declarada():
    """Teste 1: Uso de variável não declarada"""
    codigo = """print(x)"""
    
    testar_semantica(
        "Variável não declarada",
        codigo,
        deve_passar=False,
        erro_esperado="não declarada"
    )


def teste_sem_02_variavel_nao_inicializada():
    """Teste 2: Uso de variável não inicializada em expressão"""
    codigo = """x = y + 5"""
    
    testar_semantica(
        "Variável não inicializada",
        codigo,
        deve_passar=False,
        erro_esperado="não inicializada"
    )


def teste_sem_03_variavel_nao_inicializada_print():
    """Teste 3: Tentativa de imprimir variável não inicializada"""
    codigo = """x = 10
y = x
print(z)"""
    
    testar_semantica(
        "Print de variável não declarada",
        codigo,
        deve_passar=False,
        erro_esperado="não declarada"
    )


def teste_sem_04_variavel_usada_antes_atribuicao():
    """Teste 4: Variável usada antes de receber valor"""
    codigo = """a = b
b = 10"""
    
    testar_semantica(
        "Uso antes da atribuição",
        codigo,
        deve_passar=False,
        erro_esperado="não declarada"
    )


def teste_sem_05_variavel_inicializacao_correta():
    """Teste 5: Inicialização correta de variável"""
    codigo = """x = 10
y = x + 5
print(y)"""
    
    testar_semantica(
        "Inicialização correta",
        codigo,
        deve_passar=True
    )


def teste_sem_06_reatribuicao_variavel():
    """Teste 6: Reatribuição de variável (deve passar)"""
    codigo = """x = 10
x = 20
x = x + 5
print(x)"""
    
    testar_semantica(
        "Reatribuição de variável",
        codigo,
        deve_passar=True
    )


# ============================================================================
# TESTES SEMÂNTICOS - FUNÇÕES
# ============================================================================

def teste_sem_07_funcao_nao_declarada():
    """Teste 7: Chamada de função não declarada"""
    codigo = """x = 10
calcular(x)"""
    
    testar_semantica(
        "Função não declarada",
        codigo,
        deve_passar=False,
        erro_esperado="não declarada"
    )


def teste_sem_08_numero_argumentos_menor():
    """Teste 8: Número de argumentos menor que o esperado"""
    codigo = """def soma(a, b, c):
  resultado = a + b + c
  print(resultado)

soma(1, 2)"""
    
    testar_semantica(
        "Poucos argumentos na chamada",
        codigo,
        deve_passar=False,
        erro_esperado="espera 3"
    )


def teste_sem_09_numero_argumentos_maior():
    """Teste 9: Número de argumentos maior que o esperado"""
    codigo = """def soma(a, b):
  resultado = a + b
  print(resultado)

soma(1, 2, 3, 4)"""
    
    testar_semantica(
        "Muitos argumentos na chamada",
        codigo,
        deve_passar=False,
        erro_esperado="espera 2"
    )


def teste_sem_10_funcao_sem_argumentos_ok():
    """Teste 10: Função sem argumentos chamada corretamente"""
    codigo = """def imprimir():
  x = 10
  print(x)

imprimir()"""
    
    testar_semantica(
        "Função sem argumentos (correto)",
        codigo,
        deve_passar=True
    )


def teste_sem_11_funcao_sem_argumentos_erro():
    """Teste 11: Função sem argumentos chamada com argumentos"""
    codigo = """def imprimir():
  x = 10
  print(x)

imprimir(5)"""
    
    testar_semantica(
        "Função sem argumentos chamada com argumentos",
        codigo,
        deve_passar=False,
        erro_esperado="espera 0"
    )


def teste_sem_12_redeclaracao_funcao():
    """Teste 12: Redeclaração de função"""
    codigo = """def teste():
  x = 1
  print(x)

def teste():
  y = 2
  print(y)"""
    
    testar_semantica(
        "Redeclaração de função",
        codigo,
        deve_passar=False,
        erro_esperado="já declarada"
    )


def teste_sem_13_atribuir_valor_a_funcao():
    """Teste 13: Tentativa de atribuir valor a uma função"""
    codigo = """def soma(a, b):
  resultado = a + b
  print(resultado)

soma = 10"""
    
    testar_semantica(
        "Atribuição a função",
        codigo,
        deve_passar=False,
        erro_esperado="é uma função"
    )


def teste_sem_14_chamar_variavel_como_funcao():
    """Teste 14: Tentativa de chamar variável como função"""
    codigo = """x = 10
x(5)"""
    
    testar_semantica(
        "Chamar variável como função",
        codigo,
        deve_passar=False,
        erro_esperado="não é uma função"
    )


# ============================================================================
# TESTES SEMÂNTICOS - ESCOPOS
# ============================================================================

def teste_sem_15_variavel_local_funcao():
    """Teste 15: Variável local dentro de função"""
    codigo = """def teste():
  local = 10
  print(local)

teste()"""
    
    testar_semantica(
        "Variável local em função",
        codigo,
        deve_passar=True
    )


def teste_sem_16_variavel_local_fora_escopo():
    """Teste 16: Uso de variável local fora do escopo"""
    codigo = """def teste():
  local = 10
  print(local)

teste()
print(local)"""
    
    testar_semantica(
        "Variável local fora do escopo",
        codigo,
        deve_passar=False,
        erro_esperado="não declarada"
    )


def teste_sem_17_parametro_funcao():
    """Teste 17: Parâmetros são considerados inicializados"""
    codigo = """def soma(a, b):
  resultado = a + b
  print(resultado)

x = 5
y = 10
soma(x, y)"""
    
    testar_semantica(
        "Parâmetros já inicializados",
        codigo,
        deve_passar=True
    )


def teste_sem_18_variavel_global_em_funcao():
    """Teste 18: Acesso a variável global dentro de função"""
    codigo = """global_var = 100

def usar_global():
  resultado = global_var + 10
  print(resultado)

usar_global()"""
    
    testar_semantica(
        "Variável global em função",
        codigo,
        deve_passar=True
    )


def teste_sem_19_escopo_if():
    """Teste 19: Variável local no bloco if"""
    codigo = """x = 10

if x > 5:
  dentro_if = 20
  print(dentro_if)"""
    
    testar_semantica(
        "Variável no escopo if",
        codigo,
        deve_passar=True
    )


def teste_sem_20_variavel_if_fora_escopo():
    """Teste 20: Uso de variável do if fora do escopo"""
    codigo = """x = 10

if x > 5:
  dentro_if = 20

print(dentro_if)"""
    
    testar_semantica(
        "Variável do if fora do escopo",
        codigo,
        deve_passar=False,
        erro_esperado="não declarada"
    )


def teste_sem_21_escopo_else():
    """Teste 21: Variável local no bloco else"""
    codigo = """x = 5

if x > 10:
  a = 1
else:
  b = 2
  print(b)"""
    
    testar_semantica(
        "Variável no escopo else",
        codigo,
        deve_passar=True
    )


def teste_sem_22_escopo_while():
    """Teste 22: Variável local no bloco while"""
    codigo = """contador = 0

while contador < 5:
  dentro_while = contador
  contador = contador + 1
  print(dentro_while)"""
    
    testar_semantica(
        "Variável no escopo while",
        codigo,
        deve_passar=True
    )


def teste_sem_23_variavel_while_fora_escopo():
    """Teste 23: Uso de variável do while fora do escopo"""
    codigo = """contador = 0

while contador < 5:
  dentro_while = contador
  contador = contador + 1

print(dentro_while)"""
    
    testar_semantica(
        "Variável do while fora do escopo",
        codigo,
        deve_passar=False,
        erro_esperado="não declarada"
    )


# ============================================================================
# TESTES SEMÂNTICOS - CASOS COMPLEXOS
# ============================================================================

def teste_sem_24_funcao_aninhada_chamadas():
    """Teste 24: Funções com múltiplas chamadas"""
    codigo = """def dobro(x):
  resultado = x + x
  print(resultado)

def quadruplo(y):
  dobro(y)
  dobro(y)

numero = 5
quadruplo(numero)"""
    
    testar_semantica(
        "Funções aninhadas corretas",
        codigo,
        deve_passar=True
    )


def teste_sem_25_shadowing_variavel():
    """Teste 25: Shadowing de variável (mesmo nome em escopos diferentes)"""
    codigo = """x = 10

def teste():
  x = 20
  print(x)

teste()
print(x)"""
    
    testar_semantica(
        "Shadowing de variável",
        codigo,
        deve_passar=True
    )


def teste_sem_26_expressao_complexa():
    """Teste 26: Expressão complexa com múltiplas variáveis"""
    codigo = """a = 10
b = 20
c = 30
d = 40

resultado = a + b * c - d
print(resultado)"""
    
    testar_semantica(
        "Expressão complexa",
        codigo,
        deve_passar=True
    )


def teste_sem_27_expressao_com_variavel_nao_declarada():
    """Teste 27: Expressão com variável não declarada no meio"""
    codigo = """a = 10
b = 20
c = 30

resultado = a + b * x - c
print(resultado)"""
    
    testar_semantica(
        "Expressão com variável não declarada",
        codigo,
        deve_passar=False,
        erro_esperado="não declarada"
    )


def teste_sem_28_condicao_com_variaveis():
    """Teste 28: Condição usando variáveis declaradas"""
    codigo = """x = 10
y = 20

if x < y:
  maior = y
  print(maior)
else:
  maior = x
  print(maior)"""
    
    testar_semantica(
        "Condição com variáveis declaradas",
        codigo,
        deve_passar=True
    )


def teste_sem_29_condicao_com_variavel_nao_declarada():
    """Teste 29: Condição usando variável não declarada"""
    codigo = """x = 10

if x < z:
  print(x)"""
    
    testar_semantica(
        "Condição com variável não declarada",
        codigo,
        deve_passar=False,
        erro_esperado="não declarada"
    )


def teste_sem_30_input_inicializa_variavel():
    """Teste 30: Input inicializa variável corretamente"""
    codigo = """x = input()
y = x + 10
print(y)"""
    
    testar_semantica(
        "Input inicializa variável",
        codigo,
        deve_passar=True
    )


# ============================================================================
# EXECUTOR DE TESTES SEMÂNTICOS
# ============================================================================

def executar_todos_testes_semanticos():
    """Executa todos os testes semânticos"""
    
    print("\n" + "█" * 80)
    print("BATERIA DE TESTES - ANÁLISE SEMÂNTICA EXCLUSIVA")
    print("█" * 80)
    print("\nEstes testes focam APENAS em erros semânticos.")
    print("Todos os códigos testados são SINTATICAMENTE CORRETOS.")
    print("=" * 80)
    
    # ========== TESTES DE VARIÁVEIS ==========
    print("\n" + "▓" * 80)
    print("CATEGORIA 1: VARIÁVEIS")
    print("▓" * 80)
    
    teste_sem_01_variavel_nao_declarada()
    teste_sem_02_variavel_nao_inicializada()
    teste_sem_03_variavel_nao_inicializada_print()
    teste_sem_04_variavel_usada_antes_atribuicao()
    teste_sem_05_variavel_inicializacao_correta()
    teste_sem_06_reatribuicao_variavel()
    
    # ========== TESTES DE FUNÇÕES ==========
    print("\n" + "▓" * 80)
    print("CATEGORIA 2: FUNÇÕES")
    print("▓" * 80)
    
    teste_sem_07_funcao_nao_declarada()
    teste_sem_08_numero_argumentos_menor()
    teste_sem_09_numero_argumentos_maior()
    teste_sem_10_funcao_sem_argumentos_ok()
    teste_sem_11_funcao_sem_argumentos_erro()
    teste_sem_12_redeclaracao_funcao()
    teste_sem_13_atribuir_valor_a_funcao()
    teste_sem_14_chamar_variavel_como_funcao()
    
    # ========== TESTES DE ESCOPOS ==========
    print("\n" + "▓" * 80)
    print("CATEGORIA 3: ESCOPOS")
    print("▓" * 80)
    
    teste_sem_15_variavel_local_funcao()
    teste_sem_16_variavel_local_fora_escopo()
    teste_sem_17_parametro_funcao()
    teste_sem_18_variavel_global_em_funcao()
    teste_sem_19_escopo_if()
    teste_sem_20_variavel_if_fora_escopo()
    teste_sem_21_escopo_else()
    teste_sem_22_escopo_while()
    teste_sem_23_variavel_while_fora_escopo()
    
    # ========== TESTES COMPLEXOS ==========
    print("\n" + "▓" * 80)
    print("CATEGORIA 4: CASOS COMPLEXOS")
    print("▓" * 80)
    
    teste_sem_24_funcao_aninhada_chamadas()
    teste_sem_25_shadowing_variavel()
    teste_sem_26_expressao_complexa()
    teste_sem_27_expressao_com_variavel_nao_declarada()
    teste_sem_28_condicao_com_variaveis()
    teste_sem_29_condicao_com_variavel_nao_declarada()
    teste_sem_30_input_inicializa_variavel()
    
    # ========== RESUMO ==========
    print("\n" + "█" * 80)
    print("RESUMO DOS TESTES SEMÂNTICOS")
    print("█" * 80)
    print("""
    Total de testes executados: 30
    
    Categorias:
    ✓ Variáveis (6 testes)
    ✓ Funções (8 testes)
    ✓ Escopos (9 testes)
    ✓ Casos Complexos (7 testes)
    
    Verificações semânticas testadas:
    • Declaração de variáveis
    • Inicialização de variáveis
    • Declaração de funções
    • Número de argumentos em chamadas
    • Escopos (global, função, if, else, while)
    • Shadowing de variáveis
    • Diferenciação entre variáveis e funções
    • Acesso a variáveis fora do escopo
    
    """)
    print("█" * 80)


# ============================================================================
# TESTES INDIVIDUAIS
# ============================================================================

def menu_testes():
    """Menu para escolher testes individuais"""
    print("\n" + "=" * 80)
    print("MENU DE TESTES SEMÂNTICOS")
    print("=" * 80)
    print("""
    Escolha uma categoria:
    
    1. Testes de Variáveis (6 testes)
    2. Testes de Funções (8 testes)
    3. Testes de Escopos (9 testes)
    4. Testes Complexos (7 testes)
    5. Executar TODOS os testes (30 testes)
    0. Sair
    """)
    
    escolha = input("Digite sua escolha: ").strip()
    
    if escolha == "1":
        print("\n▓ EXECUTANDO: Testes de Variáveis")
        teste_sem_01_variavel_nao_declarada()
        teste_sem_02_variavel_nao_inicializada()
        teste_sem_03_variavel_nao_inicializada_print()
        teste_sem_04_variavel_usada_antes_atribuicao()
        teste_sem_05_variavel_inicializacao_correta()
        teste_sem_06_reatribuicao_variavel()
        
    elif escolha == "2":
        print("\n▓ EXECUTANDO: Testes de Funções")
        teste_sem_07_funcao_nao_declarada()
        teste_sem_08_numero_argumentos_menor()
        teste_sem_09_numero_argumentos_maior()
        teste_sem_10_funcao_sem_argumentos_ok()
        teste_sem_11_funcao_sem_argumentos_erro()
        teste_sem_12_redeclaracao_funcao()
        teste_sem_13_atribuir_valor_a_funcao()
        teste_sem_14_chamar_variavel_como_funcao()
        
    elif escolha == "3":
        print("\n▓ EXECUTANDO: Testes de Escopos")
        teste_sem_15_variavel_local_funcao()
        teste_sem_16_variavel_local_fora_escopo()
        teste_sem_17_parametro_funcao()
        teste_sem_18_variavel_global_em_funcao()
        teste_sem_19_escopo_if()
        teste_sem_20_variavel_if_fora_escopo()
        teste_sem_21_escopo_else()
        teste_sem_22_escopo_while()
        teste_sem_23_variavel_while_fora_escopo()
        
    elif escolha == "4":
        print("\n▓ EXECUTANDO: Testes Complexos")
        teste_sem_24_funcao_aninhada_chamadas()
        teste_sem_25_shadowing_variavel()
        teste_sem_26_expressao_complexa()
        teste_sem_27_expressao_com_variavel_nao_declarada()
        teste_sem_28_condicao_com_variaveis()
        teste_sem_29_condicao_com_variavel_nao_declarada()
        teste_sem_30_input_inicializa_variavel()
        
    elif escolha == "5":
        executar_todos_testes_semanticos()
        
    elif escolha == "0":
        print("\nSaindo...")
        return
    else:
        print("\n✗ Opção inválida!")


if __name__ == "__main__":
    # Executa todos os testes automaticamente
    executar_todos_testes_semanticos()
    
    # Ou descomente para usar o menu interativo:
    # menu_testes()