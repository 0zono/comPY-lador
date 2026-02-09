# gerador_cod.py

class GeradorCodigo:
    def __init__(self, tabela_simbolos):
        self.codigo = []
        self.tabela = tabela_simbolos
        self.rotulo = 0

    # =========================================================
    # Utilitários
    # =========================================================

    def nova_label(self):
        lbl = self.rotulo
        self.rotulo += 1
        return lbl

    def emitir(self, instrucao):
        self.codigo.append(instrucao)

    def resolver_labels(self):
        """Resolve labels (L0, L1, FUNC_nome) para endereços numéricos"""
        label_map = {}
        codigo_sem_labels = []

        # Primeira passagem: mapeia labels para posições
        for instrucao in self.codigo:
            if instrucao.endswith(":"):
                label = instrucao[:-1]
                label_map[label] = len(codigo_sem_labels)
            else:
                codigo_sem_labels.append(instrucao)

        # Segunda passagem: substitui labels por endereços
        codigo_final = []
        for instrucao in codigo_sem_labels:
            partes = instrucao.split()
            if len(partes) > 1:
                # Resolve labels L0, L1, etc ou FUNC_nome
                if partes[1] in label_map:
                    instrucao = f"{partes[0]} {label_map[partes[1]]}"
            codigo_final.append(instrucao)

        return codigo_final

    def salvar(self, caminho):
        codigo_final = self.resolver_labels()
        with open(caminho, "w", encoding="utf-8") as f:
            for inst in codigo_final:
                f.write(inst + "\n")

    def exibir(self):
        codigo_final = self.resolver_labels()
        print("\n--- CÓDIGO OBJETO GERADO ---")
        for i, inst in enumerate(codigo_final):
            print(f"{i:03d}: {inst}")
        print("----------------------------\n")

    # =========================================================
    # Entrada principal
    # =========================================================

    def gerar(self, ast):
        """Gera código a partir da AST"""
        self.emitir("INPP")

        # Declarações de variáveis globais
        for d in ast.get("declaracoes", []):
            if d["tipo"] == "dc_v":
                self.gerar_declaracao_variavel(d)

        # Comandos do corpo principal
        for cmd in ast.get("comandos", []):
            self.gerar_comando(cmd)

        # Termina programa principal
        self.emitir("PARA")

        # Funções (após PARA, fora do fluxo principal)
        for d in ast.get("declaracoes", []):
            if d["tipo"] == "funcao":
                self.gerar_funcao(d)

        return self.codigo

    # =========================================================
    # Declarações
    # =========================================================

    def gerar_declaracao_variavel(self, no):
        """
        Gera código para declaração de variável global
        Exemplo: x = 5
        """
        # Avalia a expressão e empilha o resultado
        self.gerar_expressao(no["expressao"])
        
        # Armazena no endereço da variável
        endereco = self.tabela.get(no["nome"])
        self.emitir(f"ARMZ {endereco}")

    def gerar_funcao(self, no):
        """
        Gera código para definição de função
        
        Exemplo:
        def soma(a, b):
            r = 0
            r = a + b
            print(r)
        """
        label_func = f"FUNC_{no['nome']}"
        self.emitir(f"{label_func}:")
        
        # Desempilhar parâmetros da pilha e armazenar nas variáveis
        # Os parâmetros foram empilhados na ordem: primeiro arg, segundo arg, ...
        # Precisamos armazenar na ordem reversa
        num_params = len(no["parametros"])
        for i in range(num_params - 1, -1, -1):
            param_nome = no["parametros"][i]
            endereco = self.tabela.get(param_nome)
            self.emitir(f"ARMZ {endereco}")

        # Corpo da função
        for cmd in no["corpo"]:
            self.gerar_comando(cmd)

        # Retorna do procedimento
        self.emitir("RTPR")

    # =========================================================
    # Comandos
    # =========================================================

    def gerar_comando(self, no):
        """Gera código para um comando"""
        tipo = no["tipo"]

        if tipo == "atribuicao":
            # Exemplo: x = 10 + 5
            self.gerar_expressao(no["expressao"])
            endereco = self.tabela.get(no["nome"])
            self.emitir(f"ARMZ {endereco}")

        elif tipo == "print":
            # Exemplo: print(x)
            endereco = self.tabela.get(no["variavel"])
            self.emitir(f"CRVL {endereco}")
            self.emitir("IMPR")

        elif tipo == "call":
            # Exemplo: soma(x, y)
            # Empilha os argumentos na ordem
            for arg in no["argumentos"]:
                self.gerar_expressao(arg)
            
            # Chama a função
            self.emitir(f"CHPR FUNC_{no['nome']}")

        elif tipo == "while":
            self.gerar_while(no)

        elif tipo == "if":
            self.gerar_if(no)

        else:
            raise Exception(f"Comando não suportado: {tipo}")

    # =========================================================
    # Estruturas de Controle
    # =========================================================

    def gerar_while(self, no):
        """
        Gera código para laço while
        
        Exemplo:
        while x < 10:
            x = x + 1
        
        Código gerado:
        L0:                    # início do loop
            CRVL x
            CRCT 10
            CPME               # x < 10
            DSVF L1            # se falso, sai do loop
            ... corpo ...
            DSVI L0            # volta ao início
        L1:                    # fim do loop
        """
        lbl_inicio = self.nova_label()
        lbl_fim = self.nova_label()

        self.emitir(f"L{lbl_inicio}:")
        
        # Avalia condição
        self.gerar_expressao(no["condicao"])
        
        # Se falso, sai do loop
        self.emitir(f"DSVF L{lbl_fim}")

        # Corpo do loop
        for cmd in no["bloco"]:
            self.gerar_comando(cmd)

        # Volta ao início
        self.emitir(f"DSVI L{lbl_inicio}")
        
        self.emitir(f"L{lbl_fim}:")

    def gerar_if(self, no):
        """
        Gera código para if-else
        
        Exemplo:
        if x > 1:
            x = z
        else:
            y = 1
        
        Código gerado:
            CRVL x
            CRCT 1
            CPMA               # x > 1
            DSVF L0            # se falso, vai para else
            ... bloco then ...
            DSVI L1            # pula o else
        L0:                    # else
            ... bloco else ...
        L1:                    # fim
        """
        lbl_else = self.nova_label()
        lbl_fim = self.nova_label()

        # Avalia condição
        self.gerar_expressao(no["condicao"])
        
        # Se falso, vai para else
        self.emitir(f"DSVF L{lbl_else}")

        # Bloco then
        for cmd in no["then"]:
            self.gerar_comando(cmd)

        # Pula o else
        self.emitir(f"DSVI L{lbl_fim}")
        
        # Label do else
        self.emitir(f"L{lbl_else}:")

        # Bloco else (se existir)
        for cmd in no.get("else", []):
            self.gerar_comando(cmd)

        # Label fim
        self.emitir(f"L{lbl_fim}:")

    # =========================================================
    # Expressões
    # =========================================================

    def gerar_expressao(self, no):
        """Gera código para uma expressão"""
        tipo = no["tipo"]

        if tipo == "numero":
            # Carrega constante
            self.emitir(f"CRCT {no['valor']}")

        elif tipo == "variavel":
            # Carrega valor da variável
            endereco = self.tabela.get(no["nome"])
            self.emitir(f"CRVL {endereco}")

        elif tipo == "input":
            # Lê entrada
            self.emitir("LEIT")

        elif tipo == "binaria":
            # Expressão binária (ex: a + b)
            # Empilha operando esquerdo
            self.gerar_expressao(no["esquerda"])
            # Empilha operando direito
            self.gerar_expressao(no["direita"])
            # Executa operação
            self.gerar_operador(no["operador"])

        else:
            raise Exception(f"Expressão não suportada: {tipo}")

    def gerar_operador(self, op):
        """
        Mapeia operadores para instruções da máquina virtual
        Baseado na documentação fornecida
        """
        mapa = {
            # Aritméticos
            "+": "SOMA",
            "-": "SUBT",
            "*": "MULT",
            "/": "DIVI",
            
            # Relacionais (comparações)
            ">": "CPMA",      # maior
            "<": "CPME",      # menor
            ">=": "CMAI",     # maior ou igual
            "<=": "CPMI",     # menor ou igual
            "==": "CPIG",     # igual
            "!=": "CDES",     # diferente
            
            # Lógicos (se a linguagem suportar)
            "and": "CONJ",    # conjunção
            "or": "DISJ",     # disjunção
        }

        if op not in mapa:
            raise Exception(f"Operador inválido: {op}")

        self.emitir(mapa[op])