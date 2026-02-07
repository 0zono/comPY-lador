# gerador_cod.py

class GeradorCodigo:
    def __init__(self, tabela_simbolos):
        self.codigo = []
        self.tabela = tabela_simbolos
        self.rotulo = 0

    # =========================
    # Utilitários
    # =========================
    def resolver_labels(self):
        # Primeira passagem: mapear labels para endereços
        label_map = {}
        codigo_sem_labels = []
        
        for instrucao in self.codigo:
            if instrucao.endswith(':'):
                # É um label - mapeia para o próximo endereço disponível
                label_name = instrucao[:-1]  # Remove ':'
                label_map[label_name] = len(codigo_sem_labels)
            else:
                codigo_sem_labels.append(instrucao)
        
        # Segunda passagem: substituir referências a labels
        codigo_final = []
        for instrucao in codigo_sem_labels:
            partes = instrucao.split()
            
            # Se a instrução tem argumento que começa com 'L', é referência a label
            if len(partes) > 1 and partes[1].startswith('L'):
                label_ref = partes[1]
                if label_ref in label_map:
                    # Substituir pelo endereço numérico
                    instrucao = f"{partes[0]} {label_map[label_ref]}"
            
            codigo_final.append(instrucao)
        
        return codigo_final

    def salvar(self, caminho_arquivo):
        """Salva as instruções geradas em um arquivo .obj"""
        try:
            codigo_final = self.resolver_labels() #se não os valores ficam como str ao inves de int
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                for instrucao in codigo_final:
                    f.write(f"{instrucao}\n")
        except Exception as e:
            raise Exception(f"Erro ao salvar arquivo objeto: {e}")

    def exibir(self):

        codigo_final = self.resolver_labels()
        print("\n--- CÓDIGO OBJETO GERADO ---")
        for i, instrucao in enumerate(codigo_final):
            print(f"{i:03d}: {instrucao}")
        print("----------------------------\n")
    
    def nova_label(self):
        lbl = self.rotulo
        self.rotulo += 1
        return lbl

    def emitir(self, instrucao):
        self.codigo.append(instrucao)

    # =========================
    # Entrada principal
    # =========================

    def gerar(self, ast):
        self.emitir("INPP")

        # declarações globais
        for d in ast.get("declaracoes", []):
            if d["tipo"] == "dc_v":
                self.gerar_declaracao(d)

        # funções
        for d in ast.get("declaracoes", []):
            if d["tipo"] == "funcao":
                self.gerar_funcao(d)

        self.emitir("PARA")
        return self.codigo

    # =========================
    # Declarações
    # =========================

    def gerar_declaracao(self, no):
        self.gerar_expressao(no["expressao"])
        endereco = self.tabela.get(no["nome"])
        self.emitir(f"ARMZ {endereco}")

    def gerar_funcao(self, no):
        # funções são apenas percorridas
        for cmd in no["corpo"]:
            self.gerar_comando(cmd)

    # =========================
    # Comandos
    # =========================

    def gerar_comando(self, no):
        tipo = no["tipo"]

        if tipo == "atribuicao":
            self.gerar_expressao(no["expressao"])
            endereco = self.tabela.get(no["nome"])
            self.emitir(f"ARMZ {endereco}")

        elif tipo == "print":
            endereco = self.tabela.get(no["variavel"])
            self.emitir(f"CRVL {endereco}")
            self.emitir("IMPR")

        elif tipo == "while":
            self.gerar_while(no)

        elif tipo == "if":
            self.gerar_if(no)

        elif tipo == "call":
            # chamadas são ignoradas na VM atual
            pass

        else:
            raise Exception(f"Comando não suportado: {tipo}")

    # =========================
    # Estruturas de controle
    # =========================

    def gerar_while(self, no):
        inicio = self.nova_label()
        fim = self.nova_label()

        self.emitir(f"L{inicio}:")
        self.gerar_expressao(no["condicao"])
        self.emitir(f"DSVF L{fim}")

        for cmd in no["bloco"]:
            self.gerar_comando(cmd)

        self.emitir(f"DSVI L{inicio}")
        self.emitir(f"L{fim}:")

    def gerar_if(self, no):
        lbl_else = self.nova_label()
        lbl_fim = self.nova_label()

        self.gerar_expressao(no["condicao"])
        self.emitir(f"DSVF L{lbl_else}")

        for cmd in no["then"]:
            self.gerar_comando(cmd)

        self.emitir(f"DSVI L{lbl_fim}")
        self.emitir(f"L{lbl_else}:")

        for cmd in no.get("else", []):
            self.gerar_comando(cmd)

        self.emitir(f"L{lbl_fim}:")

    # =========================
    # Expressões
    # =========================

    def gerar_expressao(self, no):
        tipo = no["tipo"]

        if tipo == "numero":
            self.emitir(f"CRCT {no['valor']}")

        elif tipo == "variavel":
            endereco = self.tabela.get(no["nome"])
            self.emitir(f"CRVL {endereco}")

        elif tipo == "input":
            self.emitir("LEIT")

        elif tipo == "binaria":
            self.gerar_expressao(no["esquerda"])
            self.gerar_expressao(no["direita"])
            self.gerar_operador(no["operador"])

        else:
            raise Exception(f"Expressão não suportada: {tipo}")

    def gerar_operador(self, op):
        operadores = {
            "+": "SOMA",
            "-": "SUBT",
            "*": "MULT",
            "/": "DIVI",
            ">": "CPMA",
            "<": "CPME",
            ">=": "CMAI",
            "<=": "CPMI",
            "==": "CPIG",
            "!=": "CDES"
        }

        if op not in operadores:
            raise Exception(f"Operador inválido: {op}")

        self.emitir(operadores[op])


def gerar_programa(self, programa):
    if programa['tipo'] != 'programa':
        raise Exception("AST inválida: esperado nó 'programa'")

    self.emitir("INPP")

    # 1. Declarações
    for decl in programa.get('declaracoes', []):
        self.gerar_comando(decl)

    # 2. Comandos
    for cmd in programa.get('comandos', []):
        self.gerar_comando(cmd)

    self.emitir("PARA")





