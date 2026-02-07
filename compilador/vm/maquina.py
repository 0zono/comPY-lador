from vm.instrucoes_exec import instrucoes_exec


class MaquinaVirtual:

    def __init__(self):
        self.pilha = []
        self.memoria = {}
        self.pc = 0
        self.programa = []
        self.executando = False

    def carregar_programa(self, arquivo):
        self.programa = []

        with open(arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    self.programa.append(linha)

        print(f"\n✓ Programa carregado: {len(self.programa)} instruções")

    def push(self, valor):
        self.pilha.append(valor)

    def pop(self):
        if not self.pilha:
            raise Exception(f"Pilha vazia no PC={self.pc}")
        return self.pilha.pop()

    def executar(self, debug=False):
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
                print("Memória:", self.memoria)

            instrucoes_exec(self, instrucao)
            self.pc += 1

        print("\n" + "=" * 60)
        print("EXECUÇÃO FINALIZADA")
        print("=" * 60)
        print("Pilha:", self.pilha)
        print("Memória:", self.memoria)
