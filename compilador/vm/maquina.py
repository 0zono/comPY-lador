# maquina.py
from vm.instrucoes_exec import instrucoes_exec


class MaquinaVirtual:
    """
    Máquina Virtual para executar o código objeto gerado
    """

    def __init__(self):
        self.pilha = []            # Pilha de dados (D)
        self.memoria = {}          # Memória para variáveis
        self.pc = 0                # Program Counter (i)
        self.programa = []         # Array de instruções (C)
        self.executando = False    # Flag de execução
        self.pilha_retorno = []    # Pilha para endereços de retorno (CHPR/RTPR)

    def carregar_programa(self, arquivo):
        """Carrega programa do arquivo"""
        self.programa = []

        with open(arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    self.programa.append(linha)

        print(f"\n✓ Programa carregado: {len(self.programa)} instruções")

    def push(self, valor):
        """Empilha valor na pilha de dados"""
        self.pilha.append(valor)

    def pop(self):
        """Desempilha valor da pilha de dados"""
        if not self.pilha:
            raise Exception(f"Pilha vazia no PC={self.pc}")
        return self.pilha.pop()

    def executar(self, debug=False):
        """Executa o programa carregado"""
        print("\n" + "=" * 60)
        print("INICIANDO EXECUÇÃO DA VM")
        print("=" * 60)

        self.pc = 0
        self.executando = True

        while self.executando and self.pc < len(self.programa):
            instrucao = self.programa[self.pc]

            if debug:
                print(f"\nPC={self.pc}: {instrucao}")
                print("Pilha:", self.pilha)
                print("Pilha Retorno:", self.pilha_retorno)
                print("Memória:", self.memoria)

            # Executa instrução
            instrucoes_exec(self, instrucao)
            
            # Incrementa PC (a menos que a instrução já tenha alterado)
            self.pc += 1

        print("\n" + "=" * 60)
        print("EXECUÇÃO FINALIZADA")
        print("=" * 60)
        print("Pilha:", self.pilha)
        print("Memória:", self.memoria)