

class GeradorCodigo:
    def __init__(self, tabela_simbolos):
        self.codigo = []
        self.tabela = tabela_simbolos
        self.rotulo = 0
        self.enderecos_funcoes = {}

    def nova_label(self):
        lbl = self.rotulo
        self.rotulo += 1
        return lbl

    def emitir(self, instrucao):
        self.codigo.append(instrucao)

    def resolver_labels(self):
        label_map = {}
        codigo_sem_labels = []

        for instrucao in self.codigo:
            if instrucao.endswith(":"):
                label = instrucao[:-1]
                label_map[label] = len(codigo_sem_labels)
            else:
                codigo_sem_labels.append(instrucao)

        def eh_numero(s):
            try:
                int(s)
                return True
            except ValueError:
                try:
                    float(s)
                    return True
                except ValueError:
                    return False

        codigo_final = []
        for instrucao in codigo_sem_labels:
            partes = instrucao.split()
            if len(partes) == 2:
                op, arg = partes
                if not eh_numero(arg):
                    if arg not in label_map:
                        raise Exception(f"Label não definida: {arg}")
                    instrucao = f"{op} {label_map[arg]}"
            codigo_final.append(instrucao)

        return codigo_final

    def salvar(self, caminho):
        codigo_final = self.resolver_labels()
        with open(caminho, "w", encoding="utf-8") as f:
            for instrucao in codigo_final:
                f.write(instrucao + "\n")

    def exibir(self):
        codigo_final = self.resolver_labels()
        print("\n--- CÓDIGO OBJETO GERADO ---")
        for i, instrucao in enumerate(codigo_final):
            print(f"{i:03d}: {instrucao}")
        print("----------------------------\n")

    def gerar(self, ast):
        self.emitir("INPP")

        # Registrar func
        for d in ast["declaracoes"]:
            if d["tipo"] == "funcao":
                label = f"FUNC_{d['nome']}"
                self.enderecos_funcoes[d['nome']] = label

        # pula func
        label_main = self.nova_label()
        self.emitir(f"DSVI L{label_main}")

        # armazena cod de func
        for d in ast["declaracoes"]:
            if d["tipo"] == "funcao":
                self.gerar_funcao(d)

        # basta ler
        self.emitir(f"L{label_main}:")

        # global variables
        for d in ast["declaracoes"]:
            if d["tipo"] == "dc_v":
                self.gerar_declaracao(d)

        for cmd in ast.get("comandos", []):
            self.gerar_comando(cmd)

        self.emitir("PARA")

    def gerar_declaracao(self, no):
        self.gerar_expressao(no["expressao"])
        endereco = self.tabela.get(no["nome"])
        self.emitir(f"ARMZ {endereco}")

    def gerar_funcao(self, func):
        label = f"FUNC_{func['nome']}"
        self.emitir(f"{label}:")
        

        for param in reversed(func['parametros']):
            endereco = self.tabela.get(param)
            if endereco is None:
                raise Exception(f"Parâmetro não encontrado: {param}")
            self.emitir(f"ARMZ {endereco}")


        for cmd in func['corpo']:
            self.gerar_comando(cmd)

        self.emitir("RTPR")

    def gerar_call(self, call):
        for arg in call['argumentos']:
            self.gerar_expressao(arg)

        label = self.enderecos_funcoes.get(call['nome'])
        if label is None:
            raise Exception(f"Função não definida: {call['nome']}")

        self.emitir(f"CHPR {label}")

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
            self.gerar_call(no)

        else:
            raise Exception(f"Comando não suportado: {tipo}")

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