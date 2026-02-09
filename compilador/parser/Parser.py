from lexer.Lexer import Lexer
from semantico.simbolos import TabelaSimbolos

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.buffer = []
        self.token_atual = self.nextToken()
        self.tabela_simbolos = TabelaSimbolos()
        self.ast = None

    def nextToken(self):
        if self.buffer:
            return self.buffer.pop(0)
        tok = self.lexer.nextToken()
        # Pula NEWLINEs que não são importantes
        while tok.type == "NEWLINE" and self.buffer and self.buffer[0].type == "NEWLINE":
            tok = self.lexer.nextToken()
        return tok

    def peekToken(self):
        if not self.buffer:
            self.buffer.append(self.nextToken())
        return self.buffer[0]

    def consumir(self, tipo):
        if self.token_atual.type == tipo:
            tok = self.token_atual
            self.token_atual = self.nextToken()
            return tok
        self.erro(f"Esperado {tipo}, encontrado {self.token_atual.type}")

    def consumir_opcional(self, tipo):
        """Consome o token se for do tipo especificado, senão ignora"""
        if self.token_atual.type == tipo:
            self.consumir(tipo)

    def erro(self, msg):
        raise Exception(f"{msg} (linha {self.token_atual.line}, coluna {self.token_atual.column})")

    # PROGRAMA

    def programa(self):
        corpo = self.corpo()
        self.ast = {
            "tipo": "programa",
            **corpo
        }

        print("\n[Tabela de Símbolos]")
        self.tabela_simbolos.exibir()

        print("\n[AST Gerada]")
        import pprint
        pprint.pprint(self.ast, width=120)

        return self.ast

    def corpo(self):
        """
        Lê declarações (variáveis e funções) e depois comandos do corpo principal
        """
        declaracoes = self.dc()
        
        # Pula NEWLINEs antes dos comandos principais
        while self.token_atual.type == "NEWLINE":
            self.consumir("NEWLINE")
        
        comandos = self.comandos()
        return {
            "declaracoes": declaracoes,
            "comandos": comandos
        }

    # DECLARAÇÕES

    def dc(self):
        decls = []
        
        while self.token_atual.type in ("DEF", "IDENT", "NEWLINE"):
            # Pula NEWLINEs extras
            if self.token_atual.type == "NEWLINE":
                self.consumir("NEWLINE")
                continue
                
            if self.token_atual.type == "DEF" or (self.token_atual.type == "IDENT" and self.token_atual.value == "def"):
                decls.append(self.dc_f())
            elif self._eh_dc_v():
                decls.append(self.dc_v())
            else:
                break
                
        return decls

    def _eh_dc_v(self):
        if self.token_atual.type != "IDENT":
            return False
        prox = self.peekToken()
        return prox.type == "ATRIB"

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
        
        self.consumir_opcional("NEWLINE")
        
        return {"tipo": "dc_v", "nome": ident.value, "expressao": expr}

    def dc_f(self):
        # Consome 'def'
        if self.token_atual.type == "DEF":
            self.consumir("DEF")
        elif self.token_atual.type == "IDENT" and self.token_atual.value == "def":
            self.consumir("IDENT")
        else:
            self.erro("Esperado 'def' para declaração de função")

        nome = self.consumir("IDENT").value
        params = self.parametros()
        self.consumir("DOISPTS")
        self.consumir_opcional("NEWLINE")
        
        # Espera INDENT para corpo da função
        self.consumir("INDENT")

        # Entra em escopo da função
        self.tabela_simbolos.entrar_escopo()
        for p in params:
            s = self.tabela_simbolos.declarar_variavel(p, 0, 0)
            s.inicializado = True

        corpo = self.bloco_indentado()
        
        # Espera DEDENT para sair do corpo da função
        self.consumir("DEDENT")
        
        self.tabela_simbolos.sair_escopo()

        return {"tipo": "funcao", "nome": nome, "parametros": params, "corpo": corpo}

    def parametros(self):
        params = []
        if self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            if self.token_atual.type == "IDENT":
                params.append(self.consumir("IDENT").value)
                while self.token_atual.type == "VIRG":
                    self.consumir("VIRG")
                    params.append(self.consumir("IDENT").value)
            self.consumir("FECHAPAR")
        return params

    # COMANDOS

    def comandos(self):
        """Lê comandos do corpo principal (sem INDENT/DEDENT)"""
        cmds = []
        while self.token_atual.type in ("PRINT", "IF", "WHILE", "IDENT"):
            cmds.append(self.comando())
            self.consumir_opcional("NEWLINE")
        return cmds

    def bloco_indentado(self):
        """Lê comandos dentro de um bloco indentado (até encontrar DEDENT)"""
        self.tabela_simbolos.entrar_escopo()
        cmds = []
        
        while self.token_atual.type not in ("DEDENT", "EOF"):
            if self.token_atual.type == "NEWLINE":
                self.consumir("NEWLINE")
                continue
                
            if self.token_atual.type in ("PRINT", "IF", "WHILE", "IDENT"):
                cmds.append(self.comando())
                self.consumir_opcional("NEWLINE")
            else:
                break
        
        self.tabela_simbolos.sair_escopo()
        return cmds

    def comando(self):
        if self.token_atual.type == "PRINT":
            self.consumir("PRINT")
            self.consumir("ABREPAR")
            ident = self.consumir("IDENT")
            self.consumir("FECHAPAR")

            self.tabela_simbolos.verificar_inicializado(ident.value, ident.line, ident.column)
            return {"tipo": "print", "variavel": ident.value}

        elif self.token_atual.type == "IF":
            self.consumir("IF")
            cond = self.condicao()
            self.consumir("DOISPTS")
            self.consumir_opcional("NEWLINE")
            self.consumir("INDENT")
            bloco = self.bloco_indentado()
            self.consumir("DEDENT")
            pfalsa = self.pfalsa()
            return {"tipo": "if", "condicao": cond, "then": bloco, "else": pfalsa}

        elif self.token_atual.type == "WHILE":
            self.consumir("WHILE")
            cond = self.condicao()
            self.consumir("DOISPTS")
            self.consumir_opcional("NEWLINE")
            self.consumir("INDENT")
            bloco = self.bloco_indentado()
            self.consumir("DEDENT")
            return {"tipo": "while", "condicao": cond, "bloco": bloco}

        elif self.token_atual.type == "IDENT":
            ident = self.consumir("IDENT")
            return self.restoIdent(ident)

        else:
            self.erro("Comando inválido")

    def restoIdent(self, ident):
        if self.token_atual.type == "ATRIB":
            self.consumir("ATRIB")
            expr = self.expressao()
            s = self.tabela_simbolos.buscar(ident.value)
            if s is None:
                s = self.tabela_simbolos.declarar_variavel(ident.value, ident.line, ident.column)
            s.inicializado = True
            return {"tipo": "atribuicao", "nome": ident.value, "expressao": expr}

        elif self.token_atual.type == "ABREPAR":
            args = self.lista_arg()
            return {"tipo": "call", "nome": ident.value, "argumentos": args}

        else:
            self.erro("Esperado '=' ou '(' após identificador")

    # CONDIÇÃO

    def condicao(self):
        esq = self.expressao()
        op = self.token_atual.value
        self.consumir(self.token_atual.type)
        dir = self.expressao()
        return {"tipo": "binaria", "operador": op, "esquerda": esq, "direita": dir}

    def pfalsa(self):
        if self.token_atual.type == "ELSE":
            self.consumir("ELSE")
            self.consumir("DOISPTS")
            self.consumir_opcional("NEWLINE")
            self.consumir("INDENT")
            bloco = self.bloco_indentado()
            self.consumir("DEDENT")
            return bloco
        return []

    # EXPRESSÕES

    def expressao(self):
        if self.token_atual.type == "INPUT":
            self.consumir("INPUT")
            self.consumir("ABREPAR")
            self.consumir("FECHAPAR")
            return {"tipo": "input"}

        expr = self.termo()
        while self.token_atual.type in ("SOMA", "SUB"):
            op = self.token_atual.value
            self.consumir(self.token_atual.type)
            expr = {"tipo": "binaria", "operador": op, "esquerda": expr, "direita": self.termo()}
        return expr

    def termo(self):
        expr = self.fator()
        while self.token_atual.type in ("MULT", "DIV"):
            op = self.token_atual.value
            self.consumir(self.token_atual.type)
            expr = {"tipo": "binaria", "operador": op, "esquerda": expr, "direita": self.fator()}
        return expr

    def fator(self):
        if self.token_atual.type == "NUM":
            return {"tipo": "numero", "valor": self.consumir("NUM").value}

        if self.token_atual.type == "IDENT":
            tok = self.consumir("IDENT")
            self.tabela_simbolos.verificar_inicializado(tok.value, tok.line, tok.column)
            return {"tipo": "variavel", "nome": tok.value}

        if self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            expr = self.expressao()
            self.consumir("FECHAPAR")
            return expr

        self.erro("Fator inválido")

    # LISTA DE ARGUMENTOS

    def lista_arg(self):
        args = []
        self.consumir("ABREPAR")
        if self.token_atual.type != "FECHAPAR":
            args.append(self.expressao())
            while self.token_atual.type == "VIRG":
                self.consumir("VIRG")
                args.append(self.expressao())
        self.consumir("FECHAPAR")
        return args