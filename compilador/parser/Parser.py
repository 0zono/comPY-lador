#ideia: transformar todos os estados da gramática em uma função que chama o próximo estado.
#tem que verificar se o token recebido é válido ou não, então todas podem ter o retorno true ou false, ou só parar a exec mesmo sla
#começando pela raiz pra ser top down 

# 63, 88, 126, 184, 186 problemas aqui, decidir solução
from lexer.Lexer import Lexer
from lexer.Token import Token

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.nextToken()
    
    def consumir(self, tipo):
        if self.token_atual.type == tipo:
            token_consumido = self.token_atual
            self.token_atual = self.lexer.nextToken()
            return token_consumido
        else:
            self.erro(f"Esperado {tipo}, encontrado {self.token_atual.type}")

    def programa(self):
        self.corpo()
        if self.token_atual.type != "EOF":
            self.erro("Código após fim do programa")

    def erro(self, msg):
        raise Exception(f"Erro de sintaxe: {msg} → na linha {self.token_atual.line}, coluna {self.token_atual.column}")

    def corpo(self):
        self.dc()
        self.comandos()

    def dc(self):
        if self.token_atual.type == "DEF":
            self.dc_f()
            return
        elif self.token_atual.type == "IDENT":
            self.dc_v()
            self.mais_dc()
            return
        else:
            return
    
    def mais_dc(self):
        if self.token_atual.type in ["DEF", "IDENT"]:
            self.dc()
        else:
            return

    def dc_v(self):
        variavel = self.consumir("IDENT")
        variavel_nome = variavel.value
        self.consumir("ATRIB")
        self.expressao()
    
    def dc_f(self):
        self.consumir("DEF")
        funcao = self.consumir("IDENT")
        funcao_nome = funcao.value
        self.parametros()
        self.consumir("DOISPTS")
        self.corpo_f()
    
    def parametros(self):
        if self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            self.lista_par()
            self.consumir("FECHAPAR")

    def lista_par(self):
        parametro = self.consumir("IDENT")
        parametro_nome = parametro.value
        self.mais_par()

    def mais_par(self):
        if self.token_atual.type == "VIRG":
            self.consumir("VIRG")
            self.lista_par()
    
    def corpo_f(self):
        self.bloco()
    
    def bloco(self):
        self.comandos()

    def comandos(self):
        while (self.token_atual.type == "PRINT" or self.token_atual.type == "IF" or self.token_atual.type == "IDENT" or self.token_atual.type == "WHILE"):
            self.comando()

    def comando(self):
        if self.token_atual.type == "PRINT":
            self.consumir("PRINT")
            self.consumir("ABREPAR")
            self.consumir("IDENT")
            self.consumir("FECHAPAR")
        elif self.token_atual.type == "IF":
            self.consumir("IF")
            self.condicao()
            self.consumir("DOISPTS")
            self.bloco()
            self.pfalsa()
        elif self.token_atual.type == "IDENT":
            nome = self.consumir("IDENT")
            self.restoIdent()
        elif self.token_atual.type == "WHILE":
            self.consumir("WHILE")
            self.condicao()
            self.consumir("DOISPTS")
            self.bloco()
        else:
            self.erro(f"Comando inválido: {self.token_atual.type}")

    def condicao(self):
        self.expressao()
        self.relacao()
        self.expressao()

    def relacao(self):
        if self.token_atual.type in ["IGUAL", "DIFF", "MAIOR_IGUAL", "MENOR_IGUAL", "MAIOR", "MENOR"]:
            self.consumir(self.token_atual.type)
        else:
            self.erro(f"Esperado operador relacional, encontrado {self.token_atual.type}")

    def pfalsa(self):
        if self.token_atual.type == "ELSE":
            self.consumir("ELSE")
            self.consumir("DOISPTS")
            self.bloco()

    def restoIdent(self):
        if self.token_atual.type == "ATRIB":
            self.consumir("ATRIB")
            self.expressao()
        elif self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            self.lista_arg()
            self.consumir("FECHAPAR")
    
    def lista_arg(self):
        if self.token_atual.type not in ["FECHAPAR"]:
            self.expressao()
            self.mais_arg()

    def mais_arg(self):
        if self.token_atual.type == "VIRG":
            self.consumir("VIRG")
            self.expressao()
            self.mais_arg()

    def expressao(self):
        if self.token_atual.type == "INPUT":
            self.consumir("INPUT")
            self.consumir("ABREPAR")
            self.consumir("FECHAPAR")
        else:
            self.termo()
            self.outros_termos()

    def termo(self):
        self.fator()
        self.mais_fatores()
    
    def outros_termos(self):
        if self.token_atual.type in ["SOMA", "SUB"]:
            self.op_ad()
            self.termo()
            self.outros_termos()

    def fator(self):
        if self.token_atual.type == "IDENT":
            nome = self.consumir("IDENT")
        elif self.token_atual.type == "NUM":
            num = self.consumir("NUM")
        elif self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            self.expressao()
            self.consumir("FECHAPAR")
        else:
            self.erro(f"Inválido: do tipo {self.token_atual.type}")
        
    def mais_fatores(self):
        if self.token_atual.type in ["MULT", "DIV"]:
            self.op_mul()
            self.fator()
            self.mais_fatores()

    def op_ad(self):
        if self.token_atual.type == "SOMA":
            self.consumir("SOMA")
        elif self.token_atual.type == "SUB":
            self.consumir("SUB")
        else:
            self.erro(f"Esperado + ou -, mas recebeu: {self.token_atual.type}")
    
    def op_mul(self):
        if self.token_atual.type == "MULT":
            self.consumir("MULT")
        elif self.token_atual.type == "DIV":
            self.consumir("DIV")
        else:
            self.erro(f"Esperado * ou /, mas recebeu: {self.token_atual.type}")