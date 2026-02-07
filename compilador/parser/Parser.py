from lexer.Lexer import Lexer
from semantico.simbolos import TabelaSimbolos


class Parser:
    """
    Parser Descendente Recursivo da linguagem LALG
    com análise semântica integrada e geração de AST
    """

    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.nextToken()
        self.tabela_simbolos = TabelaSimbolos()
        self.funcao_atual = None
        self.ast = None

    # ================= UTIL =================

    def pular_lixo(self):
        while self.token_atual.type in ["NEWLINE", "INDENT", "DEDENT"]:
            self.token_atual = self.lexer.nextToken()

    def consumir(self, tipo):
        if self.token_atual.type == tipo:
            token = self.token_atual
            self.token_atual = self.lexer.nextToken()
            return token
        self.erro(f"Esperado {tipo}, encontrado {self.token_atual.type}")

    def erro(self, msg):
        raise Exception(
            f"{msg} → linha {self.token_atual.line}, coluna {self.token_atual.column}"
        )

    # ================= PROGRAMA =================

    def programa(self):
        self.pular_lixo()
        self.ast = self.corpo()

        print("\n[Tabela de Símbolos]")
        self.tabela_simbolos.exibir()

        print("\n[AST Gerada]")
        import pprint
        pprint.pprint(self.ast, width=120)

        return self.ast

    def corpo(self):
        self.pular_lixo()
        declaracoes = self.dc()
        self.pular_lixo()
        comandos = self.comandos()

        return {
            'tipo': 'programa',
            'declaracoes': declaracoes,
            'comandos': comandos
        }

    # ================= DECLARAÇÕES =================

    def dc(self):
        self.pular_lixo()
        declaracoes = []

        if self.token_atual.type == "IDENT":
            declaracoes.append(self.dc_v())
            declaracoes.extend(self.mais_dc())

        elif self.token_atual.type == "DEF":
            declaracoes.append(self.dc_f())
            declaracoes.extend(self.mais_dc())  # <<< FIX

        return declaracoes

    def mais_dc(self):
        self.pular_lixo()
        declaracoes = []

        if self.token_atual.type in ["IDENT", "DEF"]:
            declaracoes.extend(self.dc())

        return declaracoes

    def dc_v(self):
        ident = self.consumir("IDENT")

        simbolo = self.tabela_simbolos.buscar(ident.value)
        if simbolo is None:
            simbolo = self.tabela_simbolos.declarar_variavel(
                ident.value, ident.line, ident.column
            )

        self.consumir("ATRIB")
        expr = self.expressao()
        simbolo.inicializado = True

        return {
            'tipo': 'dc_v',
            'nome': ident.value,
            'expressao': expr
        }

    # ================= FUNÇÕES =================

    def dc_f(self):
        self.consumir("DEF")
        ident = self.consumir("IDENT")
        self.funcao_atual = ident.value

        params = self.parametros()
        self.consumir("DOISPTS")

        # escopo da função
        self.tabela_simbolos.entrar_escopo()

        # declara parâmetros como variáveis locais inicializadas
        for nome in params:
            simbolo = self.tabela_simbolos.declarar_variavel(
                nome, ident.line, ident.column
            )
            simbolo.inicializado = True

        corpo = self.comandos()

        self.tabela_simbolos.sair_escopo()
        self.funcao_atual = None

        return {
            'tipo': 'funcao',
            'nome': ident.value,
            'parametros': params,
            'corpo': corpo
        }


    def parametros(self):
        if self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            params = self.lista_par()
            self.consumir("FECHAPAR")
            return params
        return []

    def lista_par(self):
        ident = self.consumir("IDENT")
        params = [ident.value]
        params.extend(self.mais_par())
        return params

    def mais_par(self):
        if self.token_atual.type == "VIRG":
            self.consumir("VIRG")
            return self.lista_par()
        return []

    # ================= COMANDOS =================

    def comandos(self):
        self.pular_lixo()
        comandos = []

        if self.token_atual.type in ["PRINT", "IF", "WHILE", "IDENT"]:
            comandos.append(self.comando())
            comandos.extend(self.mais_comandos())

        return comandos

    def mais_comandos(self):
        self.pular_lixo()
        comandos = []

        if self.token_atual.type in ["PRINT", "IF", "WHILE", "IDENT"]:
            comandos.extend(self.comandos())

        return comandos

    def comando(self):
        self.pular_lixo()

        if self.token_atual.type == "PRINT":
            self.consumir("PRINT")
            self.consumir("ABREPAR")
            ident = self.consumir("IDENT")
            self.consumir("FECHAPAR")

            self.tabela_simbolos.verificar_inicializado(
                ident.value, ident.line, ident.column
            )

            return {'tipo': 'print', 'variavel': ident.value}

        elif self.token_atual.type == "IF":
            self.consumir("IF")
            cond = self.condicao()
            self.consumir("DOISPTS")
            bloco = self.bloco()
            pfalsa = self.pfalsa()

            return {'tipo': 'if', 'condicao': cond, 'then': bloco, 'else': pfalsa}

        elif self.token_atual.type == "WHILE":
            self.consumir("WHILE")
            cond = self.condicao()
            self.consumir("DOISPTS")
            bloco = self.bloco()  # <<< FIX

            return {'tipo': 'while', 'condicao': cond, 'bloco': bloco}

        elif self.token_atual.type == "IDENT":
            ident = self.consumir("IDENT")
            return self.restoIdent(ident)

        else:
            self.erro("Comando inválido")

    # ================= RESTO IDENT =================

    def restoIdent(self, ident):
        if self.token_atual.type == "ATRIB":
            self.consumir("ATRIB")
            expr = self.expressao()

            simbolo = self.tabela_simbolos.buscar(ident.value)
            if simbolo is None:
                simbolo = self.tabela_simbolos.declarar_variavel(
                    ident.value, ident.line, ident.column
                )
            simbolo.inicializado = True

            return {'tipo': 'atribuicao', 'nome': ident.value, 'expressao': expr}

        elif self.token_atual.type == "ABREPAR":
            args = self.lista_arg()
            return {'tipo': 'call', 'nome': ident.value, 'argumentos': args}

        else:
            self.erro("Esperado atribuição ou chamada de função")

    def lista_arg(self):
        self.consumir("ABREPAR")
        args = self.argumentos()
        self.consumir("FECHAPAR")
        return args

    def argumentos(self):
        args = [self.expressao()]
        args.extend(self.mais_argumentos())
        return args

    def mais_argumentos(self):
        if self.token_atual.type == "VIRG":
            self.consumir("VIRG")
            return self.argumentos()
        return []

    # ================= BLOCO =================

    def bloco(self):
        self.tabela_simbolos.entrar_escopo()
        comandos = self.comandos()
        self.tabela_simbolos.sair_escopo()
        return comandos

    # ================= CONDIÇÃO =================

    def condicao(self):
        esquerda = self.expressao()
        op = self.token_atual.value
        self.consumir(self.token_atual.type)
        direita = self.expressao()

        return {
            'tipo': 'binaria',
            'operador': op,
            'esquerda': esquerda,
            'direita': direita
        }

    # ================= EXPRESSÕES =================

    def expressao(self):
        if self.token_atual.type == "INPUT":
            self.consumir("INPUT")
            self.consumir("ABREPAR")
            self.consumir("FECHAPAR")
            return {'tipo': 'input'}

        expr = self.termo()
        return self.outros_termos(expr)

    def outros_termos(self, esquerda):
        if self.token_atual.type in ["SOMA", "SUB"]:
            op = self.token_atual.value
            self.consumir(self.token_atual.type)
            direita = self.termo()
            expr = {'tipo': 'binaria', 'operador': op, 'esquerda': esquerda, 'direita': direita}
            return self.outros_termos(expr)
        return esquerda

    def termo(self):
        expr = self.fator()
        return self.mais_fatores(expr)

    def mais_fatores(self, esquerda):
        if self.token_atual.type in ["MULT", "DIV"]:
            op = self.token_atual.value
            self.consumir(self.token_atual.type)
            direita = self.fator()
            expr = {'tipo': 'binaria', 'operador': op, 'esquerda': esquerda, 'direita': direita}
            return self.mais_fatores(expr)
        return esquerda

    def fator(self):
        if self.token_atual.type == "NUM":
            token = self.consumir("NUM")
            return {'tipo': 'numero', 'valor': token.value}

        elif self.token_atual.type == "IDENT":
            token = self.consumir("IDENT")
            self.tabela_simbolos.verificar_inicializado(
                token.value, token.line, token.column
            )
            return {'tipo': 'variavel', 'nome': token.value}

        elif self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            expr = self.expressao()
            self.consumir("FECHAPAR")
            return expr

        else:
            self.erro("Fator inválido")

    # ================= ELSE =================

    def pfalsa(self):
        if self.token_atual.type == "ELSE":
            self.consumir("ELSE")
            self.consumir("DOISPTS")
            return self.bloco()
        return []
