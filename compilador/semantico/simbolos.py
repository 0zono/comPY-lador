"""
Tabela de Símbolos para o Analisador Semântico
Gerencia variáveis, funções e escopos
"""

class Simbolo:
    """Representa um símbolo (variável ou função)"""
    def __init__(self, nome, tipo_simbolo, nivel_escopo, valor=None, parametros=None):
        self.nome = nome
        self.tipo_simbolo = tipo_simbolo  # 'var', 'func'
        self.nivel_escopo = nivel_escopo
        self.valor = valor  # Para variáveis
        self.parametros = parametros or []  # Para funções (lista de nomes de parâmetros)
        self.inicializado = False

    def __repr__(self):
        if self.tipo_simbolo == 'func':
            return f"Funcao({self.nome}, params={self.parametros}, escopo={self.nivel_escopo})"
        return f"Variavel({self.nome}, escopo={self.nivel_escopo}, inicializada={self.inicializado})"


class TabelaSimbolos:
    """Gerencia tabela de símbolos com suporte a escopos"""
    
    def __init__(self):
        self.simbolos = {}  # {nome: [Simbolo, Simbolo, ...]} - pilha por nome
        self.pilha_escopos = [0]  # Pilha de escopos (0 = global)
        self.escopo_atual = 0
        self.contador_escopo = 0

    def entrar_escopo(self):
        """Entra em um novo escopo (ex: dentro de uma função)"""
        self.contador_escopo += 1
        self.escopo_atual = self.contador_escopo
        self.pilha_escopos.append(self.escopo_atual)
        print(f"[Semântico] Entrando no escopo {self.escopo_atual}")

    def sair_escopo(self):
        """Sai do escopo atual e remove símbolos desse escopo"""
        escopo_antigo = self.pilha_escopos.pop()
        print(f"[Semântico] Saindo do escopo {escopo_antigo}")
        
        # Remove símbolos do escopo que está sendo fechado
        remover = []
        for nome, lista_simbolos in self.simbolos.items():
            # Remove símbolos do escopo atual
            self.simbolos[nome] = [s for s in lista_simbolos if s.nivel_escopo != escopo_antigo]
            if not self.simbolos[nome]:
                remover.append(nome)
        
        for nome in remover:
            del self.simbolos[nome]
        
        self.escopo_atual = self.pilha_escopos[-1] if self.pilha_escopos else 0

    def declarar_variavel(self, nome, linha, coluna):
        """Declara uma nova variável no escopo atual"""
        # reatribuir?
        if self.existe_no_escopo_atual(nome):
            raise Exception(
                f"Erro semântico: Variável '{nome}' já declarada no escopo atual "
                f"→ linha {linha}, coluna {coluna}"
            )
        
        simbolo = Simbolo(nome, 'var', self.escopo_atual)
        
        if nome not in self.simbolos:
            self.simbolos[nome] = []
        self.simbolos[nome].append(simbolo)
        
        print(f"[Semântico] Variável '{nome}' declarada no escopo {self.escopo_atual}")
        return simbolo

    def declarar_funcao(self, nome, parametros, linha, coluna):
        """Declara uma nova função"""
        # Funções são sempre no escopo global (0)
        if self.existe_no_escopo(nome, 0):
            raise Exception(
                f"Erro semântico: Função '{nome}' já declarada "
                f"→ linha {linha}, coluna {coluna}"
            )
        
        simbolo = Simbolo(nome, 'func', 0, parametros=parametros)
        
        if nome not in self.simbolos:
            self.simbolos[nome] = []
        self.simbolos[nome].insert(0, simbolo)  # Funções no topo
        
        print(f"[Semântico] Função '{nome}' declarada com parâmetros {parametros}")
        return simbolo

    def buscar(self, nome):
        """Busca um símbolo nos escopos (do mais interno ao mais externo)"""
        if nome not in self.simbolos:
            return None
        
        # Busca do escopo atual para os externos
        for simbolo in reversed(self.simbolos[nome]):
            if simbolo.nivel_escopo in self.pilha_escopos:
                return simbolo
        
        return None

    def existe_no_escopo_atual(self, nome):
        """Verifica se existe no escopo atual"""
        return self.existe_no_escopo(nome, self.escopo_atual)

    def existe_no_escopo(self, nome, nivel_escopo):
        """Verifica se existe em um escopo específico"""
        if nome not in self.simbolos:
            return False
        
        for simbolo in self.simbolos[nome]:
            if simbolo.nivel_escopo == nivel_escopo:
                return True
        return False

    def marcar_inicializado(self, nome, linha, coluna):
        """Marca uma variável como inicializada"""
        simbolo = self.buscar(nome)
        if simbolo is None:
            raise Exception(
                f"Erro semântico: Variável '{nome}' não declarada "
                f"→ linha {linha}, coluna {coluna}"
            )
        simbolo.inicializado = True

    def verificar_inicializado(self, nome, linha, coluna):
        """Verifica se uma variável foi inicializada antes do uso"""
        simbolo = self.buscar(nome)
        if simbolo is None:
            raise Exception(
                f"Erro semântico: Variável '{nome}' não declarada "
                f"→ linha {linha}, coluna {coluna}"
            )
        
        if simbolo.tipo_simbolo == 'var' and not simbolo.inicializado:
            raise Exception(
                f"Erro semântico: Variável '{nome}' usada antes de ser inicializada "
                f"→ linha {linha}, coluna {coluna}"
            )
        
        return simbolo


    #UTILITARIO
    def exibir(self):
        """Exibe o conteúdo da tabela de símbolos"""
        print("\n" + "="*60)
        print("TABELA DE SÍMBOLOS")
        print("="*60)
        for nome, lista_simbolos in self.simbolos.items():
            for simbolo in lista_simbolos:
                print(f"  {simbolo}")
        print("="*60 + "\n")