import sys
from pathlib import Path


from lexer.Lexer import Lexer
from parser.Parser import Parser
from gerador.gerador_cod import GeradorCodigo
from vm.maquina import MaquinaVirtual


def ler_arquivo(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f" Erro: Arquivo '{caminho}' não encontrado")
        sys.exit(1)
    except Exception as e:
        print(f" Erro ao ler arquivo: {e}")
        sys.exit(1)


def compilar(arquivo_fonte, arquivo_objeto):
    print("=" * 70)
    print(" " * 20 + "COMPILADOR LALG")
    print("=" * 70)
    
    try:
        # LEITURA
        print(f"\n[1/6] Lendo arquivo fonte: {arquivo_fonte}")
        codigo = ler_arquivo(arquivo_fonte)
        print(f"       {len(codigo)} caracteres lidos")
        
        # ANALISE LEXICA
        print("\n[2/6] Analise Lexica...")
        lexer = Lexer(codigo)
        print("       Lexer inicializado")
        
        # ANALISE SINTATICA
        print("\n[3/6] AnAlise Sintatica...")
        parser = Parser(lexer)
        print("       Parser inicializado")
        
        # ANALISE SEMANTICA + GERAÇOA DA AST
        print("\n[4/6] Analise Semantica e Geração da AST...")
        parser.programa()
        print("       Arvore Sintatica Abstrata (AST) gerada")
        
        # GERAÇAO DE CODIGO
        print("\n[5/6] Geração de Código Objeto...")
        gerador = GeradorCodigo()
        
        if not parser.ast:
            raise Exception("AST vazia — nada para gerar")
        
        gerador.gerar_programa(parser.ast)
        print(f"       {len(gerador.codigo)} instruções geradas")
        
        # SALVAR
        print(f"\n[6/6] Salvando código objeto em: {arquivo_objeto}")
        gerador.salvar(arquivo_objeto)
        
        # Exibir código gerado
        gerador.exibir()
        
        print("\n" + "=" * 70)
        print(" " * 15 + " COMPILAÇÃO CONCLUÍDA COM SUCESSO")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 70)
        print(" " * 20 + " ERRO DE COMPILAÇÃO")
        print("=" * 70)
        print(f"\n{e}\n")
        return False


def executar(arquivo_objeto, debug=False):
    print("\n" + "=" * 70)
    print(" " * 20 + "MÁQUINA VIRTUAL LALG")
    print("=" * 70)
    
    try:
        # Criar e configurar VM
        vm = MaquinaVirtual()
        
        # Carregar programa
        print(f"\nCarregando programa: {arquivo_objeto}")
        vm.carregar_programa(arquivo_objeto)
        
        # Executar
        print("\nIniciando execução...\n")
        vm.executar(debug=debug)
        
        print("\n" + "=" * 70)
        print(" " * 15 + " EXECUÇÃO FINALIZADA COM SUCESSO")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 70)
        print(" " * 20 + " ERRO DE EXECUÇÃO")
        print("=" * 70)
        print(f"\n{e}\n")
        return False


def compilar_e_executar(arquivo_fonte, arquivo_objeto="programa.obj", debug=False):
    print("\n" + " " * 70)
    print(" " * 15 + "LALG COMPILER & VIRTUAL MACHINE")
    print(" " * 70)
    
    # Compilar
    sucesso_compilacao = compilar(arquivo_fonte, arquivo_objeto)
    
    if not sucesso_compilacao:
        print("\n  Compilação falhou. Execução cancelada.\n")
        return False
    
    # Executar
    print("\n" + "▼" * 70)
    sucesso_execucao = executar(arquivo_objeto, debug=debug)
    
    if sucesso_execucao:
        print("\n" + " " * 70)
        print(" " * 20 + " PROCESSO COMPLETO")
        print("█" * 70 + "\n")
        return True
    else:
        return False


def criar_exemplo():
    """Cria um arquivo de exemplo para testar o compilador"""
    exemplo = """x = 10
y = 20
z = x + y
print(z)

a = input()
b = a * 2
print(b)

if x < y:
    print(y)
else:
    print(x)

contador = 0
while contador < 5:
    print(contador)
    contador = contador + 1
"""
    
    with open("exemplo.lalg", 'w', encoding='utf-8') as f:
        f.write(exemplo)
    
    print(" Arquivo 'exemplo.lalg' criado com sucesso!")
    return "exemplo.lalg"


def main():
    """Função principal"""
    print("\n" + "=" * 70)
    print(" " * 29 + "COMPY-lador!")
    print(" " * 12 + "Compilador & Máquina Virtual de python EM python")
    print("=" * 70 + "\n")

    base_dir = Path(__file__).parent.parent #pq a pasta exemplos tá lá em cima
    arquivo_padrao = base_dir / "exemplos" / "correto.python.txt"

    # Nenhum argumento → usa arquivo padrão
    if len(sys.argv) == 1:
        print(f"Nenhum arquivo informado.")
        print(f"Usando arquivo padrão: {arquivo_padrao}\n")

        if not Path(arquivo_padrao).exists():
            print(f" Erro: Arquivo '{arquivo_padrao}' não encontrado\n")
            return

        compilar_e_executar(arquivo_padrao, "programa.obj", debug=False)
        return

    # Processar argumentos
    arquivo_fonte = sys.argv[1]
    arquivo_objeto = (
        sys.argv[2]
        if len(sys.argv) > 2 and not sys.argv[2].startswith('--')
        else "programa.obj"
    )
    debug = "--debug" in sys.argv

    # Validar arquivo fonte
    if not Path(arquivo_fonte).exists():
        print(f" Erro: Arquivo '{arquivo_fonte}' não encontrado\n")
        return

    # Executar pipeline
    compilar_e_executar(arquivo_fonte, arquivo_objeto, debug=debug)

if __name__ == "__main__":
    main()