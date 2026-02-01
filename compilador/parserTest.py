"""
Teste do Parser com código simples
"""

# Simulação das classes Token e Lexer para testar
class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def exibir(self):
        return f"Token(tipo: {self.type}, valor: {self.value}, linha: {self.line}, coluna: {self.column})"



from parser.Parser import Parser
from lexer.Lexer import Lexer

def teste_simples():
    """
    Teste com código muito simples
    """
    print("=" * 60)
    print("TESTE 1: Declaração de variável simples")
    print("=" * 60)
    
    codigo = "a = 5"
    print(f"Código: {codigo}\n")
    
    lexer = Lexer(codigo)
    parser = Parser(lexer)
     
    try:
        parser.programa()
        print("\n SUCESSO: Código aceito!")
    except Exception as e:
        print(f"\n ERRO: {e}")


def teste_com_print():
    print("\nESPERADO:  SUCESSO: Código aceito!")
    """
    Teste com declaração e print
    """
    print("\n" + "=" * 60)
    print("TESTE 2: Declaração e Print")
    print("=" * 60)
    
    codigo = """a = 5
print(a)"""
    
    print(f"Código:\n{codigo}\n")
    
    lexer = Lexer(codigo)
    parser = Parser(lexer)
     
    try:
        parser.programa()
        print("\n SUCESSO: Código aceito!")
    except Exception as e:
        print(f"\n ERRO: {e}")


def teste_funcao():
    """
    Teste com função simples
    """
    print("\n" + "=" * 60)
    print("TESTE 3: Função simples")
    print("=" * 60)
    
    codigo = """def soma(a, b):
  c = a + b
  print(c)

x = 10
y = 20
soma(x, y)"""
    
    print(f"Código:\n{codigo}\n")
    
    lexer = Lexer(codigo)
    parser = Parser(lexer)
     
    try:
        parser.programa()
        print("\n SUCESSO: Código aceito!")
    except Exception as e:
        print(f"\n ERRO: {e}")


def teste_simples_falha():
    print("\n" + "=" * 60)
    print("TESTE FALHA 1: Atribuição sem expressão")
    print("=" * 60)

    codigo = "a ="

    print(f"Código:\n{codigo}\n")

    lexer = Lexer(codigo)
    parser = Parser(lexer)

    try:
        parser.programa()
        print("\n ERRO: Código deveria falhar, mas foi aceito!")
    except Exception as e:
        print(f"\n FALHA CORRETA: {e}")


def teste_chamada_funcao_falha():
    print("\n" + "=" * 60)
    print("TESTE FALHA 4: Chamada de função inválida")
    print("=" * 60)

    codigo = "soma(1, )"

    print(f"Código:\n{codigo}\n")

    lexer = Lexer(codigo)
    parser = Parser(lexer)

    try:
        parser.programa()
        print("\n ERRO: Código deveria falhar, mas foi aceito!")
    except Exception as e:
        print(f"\n FALHA CORRETA: {e}")

def teste_operador_sem_operando():
    print("\n" + "=" * 60)
    print("TESTE FALHA 3: Operador sem operando")
    print("=" * 60)

    codigo = "a = 5 +"

    print(f"Código:\n{codigo}\n")

    lexer = Lexer(codigo)
    parser = Parser(lexer)

    try:
        parser.programa()
        print("\n ERRO: Código deveria falhar, mas foi aceito!")
    except Exception as e:
        print(f"\n FALHA CORRETA: {e}")

def teste_parenteses_falha():
    print("\n" + "=" * 60)
    print("TESTE FALHA 2: Parênteses não fechados")
    print("=" * 60)

    codigo = "a = (2 + 3"

    print(f"Código:\n{codigo}\n")

    lexer = Lexer(codigo)
    parser = Parser(lexer)

    try:
        parser.programa()
        print("\n ERRO: Código deveria falhar, mas foi aceito!")
    except Exception as e:
        print(f"\n FALHA CORRETA: {e}")


if __name__ == "__main__":
    
    teste_simples()
    teste_com_print()
    teste_funcao()

    teste_simples_falha()
    teste_parenteses_falha()
    teste_operador_sem_operando()
    teste_chamada_funcao_falha()
    
    print("\n" + "=" * 60)
    print("INSTRUÇÕES PARA USAR:")
    print("=" * 60)