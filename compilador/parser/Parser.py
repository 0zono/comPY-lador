"""
Parser com Análise Semântica Integrada (Descendente Recursivo)
Estende o parser sintático adicionando verificações semânticas
"""

from lexer.Lexer import Lexer
from lexer.Token import Token
from semantico.simbolos import TabelaSimbolos


class Parser:
    """Parser Descendente Recursivo com análise semântica integrada"""
    
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.nextToken()
        self.tabela_simbolos = TabelaSimbolos()
        self.funcao_atual = None  #funcao atual aqiu
        
    def consumir(self, tipo):
        """Consome um token esperado"""
        if self.token_atual.type == tipo:
            token_consumido = self.token_atual
            self.token_atual = self.lexer.nextToken()
            return token_consumido
        else:
            self.erro(f"Esperado {tipo}, encontrado {self.token_atual.type}")

    def erro(self, msg):
        """Gera erro de sintaxe ou semântico"""
        raise Exception(
            f"{msg} → na linha {self.token_atual.line}, "
            f"coluna {self.token_atual.column}"
        )

    # ===== REGRAS GRAMATICAIS COM SEMÂNTICA =====

    def programa(self):
        """<programa> -> <corpo>"""
        print("[Parser] Iniciando análise do programa...")
        self.corpo()
        if self.token_atual.type != "EOF":
            self.erro("Código após fim do programa")
        
        print("\n[Parser] Análise concluída com sucesso!")
        self.tabela_simbolos.exibir()

    def corpo(self):
        """<corpo> -> <dc> <comandos>"""
        self.dc()
        self.comandos()

    def dc(self):
        """<dc> -> <dc_v> <mais_dc> | <dc_f> | λ"""
        if self.token_atual.type == "DEF":
            self.dc_f()
            return
        elif self.token_atual.type == "IDENT":
            self.dc_v()
            self.mais_dc()
            return
        else:
            return  # λ (epsilon)
    
    def mais_dc(self):
        """<mais_dc> -> <dc> | λ"""
        if self.token_atual.type in ["DEF", "IDENT"]:
            self.dc()
        else:
            return  # λ

    def dc_v(self):
        """<dc_v> -> <ident> = <expressao>"""
        variavel = self.consumir("IDENT")
        nome = variavel.value

        simbolo = self.tabela_simbolos.buscar(nome)

        if simbolo is None:
            # primeira atribuição → cria variável
            simbolo = self.tabela_simbolos.declarar_variavel(
                nome,
                variavel.line,
                variavel.column
            )
            print(f"[Semântico] Variável '{nome}' criada")
        else:
            # reatribuição → permitido
            print(f"[Semântico] Variável '{nome}' reatribuída")

        self.consumir("ATRIB")
        self.expressao()

        simbolo.inicializado = True
        print(f"[Semântico] Variável '{nome}' inicializada")

    
    def dc_f(self):
        """<dc_f> -> def ident <parametros> : <corpo_f>"""
        self.consumir("DEF")
        funcao = self.consumir("IDENT")
        funcao_nome = funcao.value
        
        # Coleta parâmetros antes de declarar
        parametros = self.parametros()
        
        # funcao declarada
        self.tabela_simbolos.declarar_funcao(
            funcao_nome,
            parametros,
            funcao.line,
            funcao.column
        )
        
        self.funcao_atual = funcao_nome
        
        self.consumir("DOISPTS")
        
        # entra no escopo da funcao
        self.tabela_simbolos.entrar_escopo()
        
        # pega os parametros e inicializa como variavel
        for param in parametros:
            simbolo = self.tabela_simbolos.declarar_variavel(param, funcao.line, funcao.column)
            simbolo.inicializado = True 
        
        self.corpo_f()
        
        # sai da funcao
        self.tabela_simbolos.sair_escopo()
        
        self.funcao_atual = None
    
    def parametros(self):
        """<parametros> -> ( <lista_par> ) | λ"""
        parametros = []
        if self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            parametros = self.lista_par()
            self.consumir("FECHAPAR")
        return parametros

    def lista_par(self):
        """<lista_par> -> ident <mais_par>"""
        parametros = []
        parametro = self.consumir("IDENT")
        parametros.append(parametro.value)
        parametros.extend(self.mais_par())
        return parametros

    def mais_par(self):
        """<mais_par> -> , <lista_par> | λ"""
        if self.token_atual.type == "VIRG":
            self.consumir("VIRG")
            return self.lista_par()
        return []
    
    def corpo_f(self):
        """<corpo_f> -> <bloco>"""
        self.bloco()
    
    def bloco(self):
        """<bloco> -> <comandos>"""
        self.comandos()

    def comandos(self):
        """<comandos> -> <comando> <mais_comandos>"""
        while self.token_atual.type in ["PRINT", "IF", "IDENT", "WHILE"]:
            self.comando()

    def comando(self):
        """<comando> -> print (ident) | if ... | while ... | ident <restoIdent>"""
        if self.token_atual.type == "PRINT":
            self.consumir("PRINT")
            self.consumir("ABREPAR")
            ident = self.consumir("IDENT")
            
            # verificar se a variavel usada emquaisquer comands foi inicialiazada
            self.tabela_simbolos.verificar_inicializado(
                ident.value,
                ident.line,
                ident.column
            )
            
            self.consumir("FECHAPAR")
            
        elif self.token_atual.type == "IF":
            self.consumir("IF")
            self.condicao()
            self.consumir("DOISPTS")
            
            # if
            self.tabela_simbolos.entrar_escopo()
            self.bloco()
            self.tabela_simbolos.sair_escopo()
            
            self.pfalsa()
            
        elif self.token_atual.type == "IDENT":
            nome = self.consumir("IDENT")
            self.restoIdent(nome)
            
        elif self.token_atual.type == "WHILE":
            self.consumir("WHILE")
            self.condicao()
            self.consumir("DOISPTS")
            
            # while
            self.tabela_simbolos.entrar_escopo()
            self.bloco()
            self.tabela_simbolos.sair_escopo()
        else:
            self.erro(f"Comando inválido: {self.token_atual.type}")

    def condicao(self):
        """<condicao> -> <expressao> <relacao> <expressao>"""
        self.expressao()
        self.relacao()
        self.expressao()

    def relacao(self):
        """<relacao> -> == | != | >= | <= | > | <"""
        if self.token_atual.type in ["IGUAL", "DIFF", "MAIOR_IGUAL", 
                                      "MENOR_IGUAL", "MAIOR", "MENOR"]:
            self.consumir(self.token_atual.type)
        else:
            self.erro(f"Esperado operador relacional, encontrado {self.token_atual.type}")

    def pfalsa(self):
        """<pfalsa> -> else : <bloco> | λ"""
        if self.token_atual.type == "ELSE":
            self.consumir("ELSE")
            self.consumir("DOISPTS")
            
            # else
            self.tabela_simbolos.entrar_escopo()
            self.bloco()
            self.tabela_simbolos.sair_escopo()

    def restoIdent(self, ident_token):
        """<restoIdent> -> = <expressao> | <lista_arg>"""
        if self.token_atual.type == "ATRIB":
            
            self.consumir("ATRIB")
            
            # 
            simbolo = self.tabela_simbolos.buscar(ident_token.value)
            if simbolo is None:
                self.erro(f"Variável '{ident_token.value}' não declarada")
            
            if simbolo.tipo_simbolo != 'var':
                self.erro(f"'{ident_token.value}' é uma função, não pode ser atribuída")
            
            self.expressao()
            
        
            self.tabela_simbolos.marcar_inicializado(
                ident_token.value,
                ident_token.line,
                ident_token.column
            )
            
        elif self.token_atual.type == "ABREPAR":
            # Chamada de função
            # funcao existe?
            simbolo = self.tabela_simbolos.buscar(ident_token.value)
            if simbolo is None:
                self.erro(f"Função '{ident_token.value}' não declarada")
            
            if simbolo.tipo_simbolo != 'func':
                self.erro(f"'{ident_token.value}' não é uma função")
            
            self.consumir("ABREPAR")
            num_args = self.lista_arg()
            self.consumir("FECHAPAR")
            
            # quantidade de argumentos correta?
            if len(simbolo.parametros) != num_args:
                self.erro(
                    f"Função '{ident_token.value}' espera {len(simbolo.parametros)} "
                    f"argumentos, mas recebeu {num_args}"
                )
    
    def lista_arg(self):
        """<lista_arg> -> ( <argumentos> ) | λ"""
        count = 0
        if self.token_atual.type not in ["FECHAPAR"]:
            count = self.argumentos()
        return count

    def argumentos(self):
        """<argumentos> -> <expressao> <mais_argumentos>"""
        self.expressao()
        return 1 + self.mais_argumentos()

    def mais_argumentos(self):
        """<mais_argumentos> -> , <argumentos> | λ"""
        if self.token_atual.type == "VIRG":
            self.consumir("VIRG")
            return self.argumentos()
        return 0

    def expressao(self):
        """<expressao> -> <termo> <outros_termos> | input()"""
        if self.token_atual.type == "INPUT":
            self.consumir("INPUT")
            self.consumir("ABREPAR")
            self.consumir("FECHAPAR")
        else:
            self.termo()
            self.outros_termos()

    def termo(self):
        """<termo> -> <fator> <mais_fatores>"""
        self.fator()
        self.mais_fatores()
    
    def outros_termos(self):
        """<outros_termos> -> <op_ad> <termo> <outros_termos> | λ"""
        if self.token_atual.type in ["SOMA", "SUB"]:
            self.op_ad()
            self.termo()
            self.outros_termos()

    def fator(self):
        """<fator> -> ident | numero | ( <expressao> )"""
        if self.token_atual.type == "IDENT":
            nome = self.consumir("IDENT")
            
            # variavel existe?
            self.tabela_simbolos.verificar_inicializado(
                nome.value,
                nome.line,
                nome.column
            )
            
        elif self.token_atual.type == "NUM":
            num = self.consumir("NUM")
            
        elif self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            self.expressao()
            self.consumir("FECHAPAR")
        else:
            self.erro(f"Inválido: do tipo {self.token_atual.type}")
        
    def mais_fatores(self):
        """<mais_fatores> -> <op_mul> <fator> <mais_fatores> | λ"""
        if self.token_atual.type in ["MULT", "DIV"]:
            self.op_mul()
            self.fator()
            self.mais_fatores()

    def op_ad(self):
        """<op_ad> -> + | -"""
        if self.token_atual.type == "SOMA":
            self.consumir("SOMA")
        elif self.token_atual.type == "SUB":
            self.consumir("SUB")
        else:
            self.erro(f"Esperado + ou -, mas recebeu: {self.token_atual.type}")
    
    def op_mul(self):
        """<op_mul> -> * | /"""
        if self.token_atual.type == "MULT":
            self.consumir("MULT")
        elif self.token_atual.type == "DIV":
            self.consumir("DIV")
        else:
            self.erro(f"Esperado * ou /, mas recebeu: {self.token_atual.type}")