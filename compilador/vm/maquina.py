
from vm.instrucoes_exec import instrucoes_exec

class MaquinaVirtual:
    def __init__(self):
        self.pilha = []
        self.memoria = {}
        self.programa = []
        self.pc = 0  # contador de programa
        self.executando = False
        self.registrador_retorno = None  # endereco de retorno, util
    def carregar_programa(self, arquivo):
        """Carrega programa do arquivo"""
        with open(arquivo, 'r', encoding='utf-8') as f:
            self.programa = [linha.strip() for linha in f if linha.strip()]
        print(f"\n✓ Programa carregado: {len(self.programa)} instruções")

    def executar(self, debug=False):
        """Executa o programa"""
        self.executando = True
        self.pc = 0
        
        print("\n" + "="*60)
        print("INICIANDO EXECUÇÃO DA VM")
        print("="*60 + "\n")
        
        while self.executando and self.pc < len(self.programa):
            instrucao = self.programa[self.pc]
            
            if debug:
                print(f"[{self.pc:03d}] {instrucao:20s} | Pilha: {self.pilha}")
            
            try:
                instrucoes_exec(self, instrucao)
                self.pc += 1
            except Exception as e:
                print(f"\n❌ ERRO na instrução {self.pc}: {instrucao}")
                print(f"   {e}")
                print(f"   Pilha: {self.pilha}")
                print(f"   Memória: {self.memoria}")
                raise
        
        print("\n" + "="*60)
        print("EXECUÇÃO FINALIZADA")
        print("="*60)
        print(f"Pilha: {self.pilha}")
        print(f"Memória: {self.memoria}\n")

    def push(self, valor):
        """Empilha valor"""
        self.pilha.append(valor)

    def pop(self):
        """Desempilha valor"""
        if not self.pilha:
            raise Exception(f"Tentativa de desempilhar de pilha vazia no PC={self.pc}")
        return self.pilha.pop()

    def topo(self):
        """Retorna topo sem desempilhar"""
        if not self.pilha:
            raise Exception(f"Pilha vazia no PC={self.pc}")
        return self.pilha[-1]