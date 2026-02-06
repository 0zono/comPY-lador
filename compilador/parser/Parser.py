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

    # util
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

    # PROGRAMA
    def programa(self):
        # <programa> -> <corpo>
        self.ast = self.corpo()

        print("\n[Tabela de Símbolos]")
        self.tabela_simbolos.exibir()

        print("\n[AST Gerada]")
        import pprint
        pprint.pprint(self.ast, width=120)

        return self.ast

    # CORPO
    def corpo(self):
        # <corpo> -> <dc> <comandos>
        declaracoes = self.dc()
        comandos = self.comandos()

        return {
            'tipo': 'programa',
            'declaracoes': declaracoes,
            'comandos': comandos
        }

    # DECLARAÇÕES
    def dc(self):
        # <dc> -> <dc_v> <mais_dc> | <dc_f> | λ
        declaracoes = []

        if self.token_atual.type == "IDENT":
            declaracoes.append(self.dc_v())
            declaracoes.extend(self.mais_dc())

        elif self.token_atual.type == "DEF":
            declaracoes.append(self.dc_f())

        return declaracoes
    #mais_dc
    def mais_dc(self): 
        #<mais_dc> -> <dc> | λ
        declaracoes = []

        if self.token_atual.type in ["IDENT", "DEF"]:
            declaracoes.extend(self.dc())

        return declaracoes

    #dc_v
    def dc_v(self): #declara_var
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

    # FUNÇÕES
    def dc_f(self): #declara_func
        # <dc_f> -> def ident <parametros> : <corpo_f>
        self.consumir("DEF")
        ident = self.consumir("IDENT")
        self.funcao_atual = ident.value

        params = self.parametros()
        self.consumir("DOISPTS")
        corpo = self.bloco()

        self.funcao_atual = None

        return {
            'tipo': 'funcao',
            'nome': ident.value,
            'parametros': params,
            'corpo': corpo
        }

    def parametros(self):
        #<parametros> -> ( <lista_par> ) | λ
        if self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            params = self.lista_par()
            self.consumir("FECHAPAR")
            return params
        return []

    def lista_par(self):
        #<lista_par> -> ident <mais_par>
        ident = self.consumir("IDENT")
        params = [ident.value]
        params.extend(self.mais_par())
        return params

    def mais_par(self):
        #<mais_par> -> , <lista_par> | λ
        if self.token_atual.type == "VIRG":
            self.consumir("VIRG")
            return self.lista_par()
        return []

    # COMANDOS
    def comandos(self):
        # <comandos> -> <comando> <mais_comandos>
        comandos = []

        if self.token_atual.type in ["PRINT", "IF", "WHILE", "IDENT"]:
            comandos.append(self.comando())
            comandos.extend(self.mais_comandos())

        return comandos

    def mais_comandos(self):
        #<mais_comandos> -> <comandos> | λ
        comandos = []

        if self.token_atual.type in ["PRINT", "IF", "WHILE", "IDENT"]:
            comandos.extend(self.comandos())

        return comandos

    def comando(self):
        #<comando> -> print (ident) |
            #   if <condicao> : <bloco> <pfalsa> |
            #   while <condicao> : <bloco> |
            #   ident <restoIdent>
        if self.token_atual.type == "PRINT":
            self.consumir("PRINT")
            self.consumir("ABREPAR")
            ident = self.consumir("IDENT")
            self.consumir("FECHAPAR")

            self.tabela_simbolos.verificar_inicializado(
                ident.value, ident.line, ident.column
            )

            return {
                'tipo': 'print',
                'variavel': ident.value
            }

        elif self.token_atual.type == "IF":
            self.consumir("IF")
            cond = self.condicao()
            self.consumir("DOISPTS")
            bloco = self.bloco()
            pfalsa = self.pfalsa()

            return {
                'tipo': 'if',
                'condicao': cond,
                'then': bloco,
                'else': pfalsa
            }

        elif self.token_atual.type == "WHILE":
            self.consumir("WHILE")
            cond = self.condicao()
            self.consumir("DOISPTS")
            bloco = self.bloco()

            return {
                'tipo': 'while',
                'condicao': cond,
                'bloco': bloco
            }

        elif self.token_atual.type == "IDENT":
            ident = self.consumir("IDENT")
            return self.restoIdent(ident)

        else:
            self.erro("Comando inválido")

    # RESTO IDENT
    def restoIdent(self, ident):
        # <restoIdent> -> = <expressao> | <lista_arg>
        if self.token_atual.type == "ATRIB":
            self.consumir("ATRIB")
            expr = self.expressao()
            return {
                'tipo': 'atribuicao',
                'nome': ident.value,
                'expressao': expr
            }

        elif self.token_atual.type == "ABREPAR":
            args = self.lista_arg()
            return {
                'tipo': 'chamada_funcao',
                'nome': ident.value,
                'argumentos': args
            }

        else:
            self.erro("Esperado '=' ou '(' após identificador")

    def lista_arg(self):
        #<lista_arg> -> ( <argumentos> ) | λ
        self.consumir("ABREPAR")
        args = self.argumentos()
        self.consumir("FECHAPAR")
        return args

    def argumentos(self):
        #<argumentos> -> <expressao> <mais_argumentos>
        args = [self.expressao()]
        args.extend(self.mais_argumentos())
        return args

    def mais_argumentos(self):
        #<mais_argumentos> -> , <argumentos> | λ
        if self.token_atual.type == "VIRG":
            self.consumir("VIRG")
            return self.argumentos()
        return []

    # BLOCO
    def bloco(self):
        # <bloco> -> tabulacao <comandos>
        self.tabela_simbolos.entrar_escopo()
        comandos = self.comandos()
        self.tabela_simbolos.sair_escopo()
        return comandos

    # CONDIÇÃO
    def condicao(self):
        # <condicao> -> <expressao> <relacao> <expressao>
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

    # EXPRESSÕES
    def expressao(self):
        #<termo> <outros_termos> | input()
        if self.token_atual.type == "INPUT":
            self.consumir("INPUT")
            self.consumir("ABREPAR")
            self.consumir("FECHAPAR")
            return {'tipo': 'input'}

        expr = self.termo()
        return self.outros_termos(expr)

    def outros_termos(self, esquerda):
        #<outros_termos> -> <op_ad> <termo> <outros_termos> | λ
        if self.token_atual.type in ["SOMA", "SUB"]:
            op = self.token_atual.value
            self.consumir(self.token_atual.type)
            direita = self.termo()
            expr = {
                'tipo': 'binaria',
                'operador': op,
                'esquerda': esquerda,
                'direita': direita
            }
            return self.outros_termos(expr)
        return esquerda

    def termo(self):
        #<termo> -> <fator> <mais_fatores>
        expr = self.fator()
        return self.mais_fatores(expr)

    def mais_fatores(self, esquerda):
        #<mais_fatores> -> <op_mul> <fator> <mais_fatores> | λ
        if self.token_atual.type in ["MULT", "DIV"]:
            op = self.token_atual.value
            self.consumir(self.token_atual.type)
            direita = self.fator()
            expr = {
                'tipo': 'binaria',
                'operador': op,
                'esquerda': esquerda,
                'direita': direita
            }
            return self.mais_fatores(expr)
        return esquerda

    def fator(self):
        #<fator> -> ident | numero | ( <expressao> )
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

    # PFALSA
    def pfalsa(self):
        # <pfalsa> -> else : <bloco> | λ
        if self.token_atual.type == "ELSE":
            self.consumir("ELSE")
            self.consumir("DOISPTS")
            return self.bloco()
        return []
