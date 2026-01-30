#ideia: transformar todos os estados da gramática em uma função que chama o próximo estado.
#tem que verificar se o token recebido é válido ou não, então todas podem ter o retorno true ou false, ou só parar a exec mesmo sla
#começando pela raiz pra ser top down 
from lexer.Lexer import Lexer
from lexer.Token import Token

#TO DO: tirar TODOS os elses que levariam pra λ pq é completamente inutil eles existirem (a não ser pra "claridade" de leitura)
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.nextToken()
    
    def consumir(self, tipo):
      if self.token_atual.type == tipo:
          self.token_atual = self.lexer.nextToken()
      else:
          self.erro(f"Esperado {tipo}, encontrado {self.token_atual.type}")

    def programa(self):
        # <programa> -> <corpo>
        self.corpo()
        #programa PRECISA terminar com EOF
        if self.token_atual.type != "EOF":
            self.erro("Código após fim do programa")
#        else:
#            self.erro("Erro de sintaxe: token inesperado")

    def erro(self, msg):
        raise Exception(f"Erro de sintaxe: {msg} "
                        f"→ na linha {self.token_atual.line}, coluna {self.token_atual.column}")

    def corpo(self):
        # <corpo> -> <dc> <comandos>
        self.dc()
        self.comandos()

    def dc(self):
        # <dc> -> <dc_v> <mais_dc> | <dc_f> | λ
        if self.token_atual.type == "DEF":
            self.dc_f() #<dc_f>
            return
        
        # <dc_v> <mais_dc>
        elif self.token_atual.type == "IDENT":
            self.dc_v()
            self.mais_dc()
            return
        
        #λ
        else:
            return
    
    def mais_dc(self):
        #<mais_dc> -> <dc> | λ
        if self.token_atual.type in ["DEF", "IDENT"]:
            self.dc
        else:
            #λ
            return

    def dc_v(self):
        #<dc_v> -> <ident> = <expressoa>
        variavel_nome = self.consumir("IDENT")

        self.consumir("ATRIB") #'=': "ATRIB", atribuiçoa

        self.expressao()
    
    def dc_f(self):
        #<dc_f> -> def ident <parametros> : <corpo_f> 
        #<declarar_funcao> -> def (palavra reservada) identificador <parametros da funcao>
        self.consumir("DEF")
        funcao_nome = self.consumir("IDENT")

        self.parametros()
        self.consumir("DOISPTS") #':': "DOISPTS"
        self.corpo_f()
    
    def parametros(self):
        #<parametros> -> ( <lista_para> ) | λ
        if self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            self.lista_par()
            self.consumir("FECHAPAR")

    def lista_par(self):
        #<lista_par> - ident <mais_par>
        parametro = self.consumir("IDENT")
        self.mais_par()

    def mais_par(self):
        # virgula pra representar mais de um parametro
        if self.token_atual.type == "VIRG":
            self.consumir("VIRG")
            self.lista_par()
    
    def corpo_f(self):
        # <corpo_f> -> <bloco
        self.bloco()
    
    def bloco(self):
        #tabulacao<comandos>
        self.comandos()

    def comandos(self):
        #<comandos> -> <COMANDO> <mais_comandos>
        while (self.token_atual.type == "PRINT" or self.token_atual.type == "IF" or self.token_atual.type == "IDENT" or self.token_atual.type == "WHILE"):
            self.comando()

    def comando(self):
        if self.token_atual.type == "PRINT":
            #print (ident)
            self.consumir("PRINT")
            self.consumir("ABREPAR")   
            self.consumir("IDENT")  #VARIAVEL MAS DEVERIA SER CAPAZ DE RECEBER STRING TAMBÉM?
            self.consumir("FECHAPAR")

        elif self.token_atual.type == "IF":
            #<condicao> : <bloco> <pfalsa>
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
            self.condicao()             # condição
            self.consumir("DOISPTS")    # :
            self.bloco()          
        else:
            self.erro(f"Comando inválido: {self.token_atual.type}")

    def restoIdent(self):
        #<restoIdent> -> = <expressao> | <lista_arg>]
        if self.token_atual.type == "ATRIB":
            self.consumir("ATRIB")
            self.expressao()
        elif self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            self.lista_arg()
            self.consumir("FECHAPAR")
    
    def lista_arg(self):
    # <lista_arg> -> <expressao> <mais_arg> | λ
        if self.token_atual.type not in ["FECHAPAR"]:
            self.expressao()
            self.mais_arg()

    def mais_arg(self):
        if self.token_atual.type == "VIRG":
            self.consumir("VIRG")
            self.expressao()
            self.mais_arg()


    def expressao(self):
        #<expresao> -> <termo> <outros_termos> | input()
        if self.token_atual == "INPUT":
            self.consumir("INPUT")
            self.consumir("ABREPAR") # (
            self.consumir("FECHAPAR") # )
        else:
            self.termo()
            self.outros_termos()

    def termo(self):
        #<termo> -> <fator> <mais_fatores>
        self.fator()
        self.mais_fatores()
    
    def outros_termos(self):
        # <outros_termos> -> <op_ad> <termo> <outros_termos> | λ
        if self.token_atual.type in ["SOMA", "SUB"]:
            self.op_ad()
            self.termo()
            self.outros_termos() #recursion babyyyyyyyyyy

    def fator(self):
        #<fator> -> ident | numero | ( <expressao> )
        if self.token_atual.type == "IDENT":
            nome = self.consumir("IDENT")
        elif self.token_atual.type == "NUM":
            num = self.consumir("NUM")
        elif self.token_atual.type == "ABREPAR":
            self.consumir("ABREPAR")
            self.expressao()
            self.consumir("FECHAPAR")
            #TO DO: tratar parenteses não fechados aq
        else:
            self.erro(f"Inválido: do tipo {self.token_atual.type}")   
        
    def mais_fatores(self):
        #<termo> -> <fator> <mais_fatores>
        if self.token_atual.type in ["MULT", "DIV"]:
            self.op_mul()
            self.fator()
            self.mais_fatores()

    def op_ad(self):
        #<op_ad> -> + | -
        if self.token_atual.type =="SOMA":
            self.consumir("SOMA")
        elif self.token_atual.type == "SUB":
            self.consumir("SUB")
        else:
            self.erro(f"Eseprado + ou -, mas recebeu: {self.token_atual.type}")
    
    def op_mul(self):
        #<op_mul> -> * | /
        if self.token_atual.type == "MULT":
            self.consumir("MULT")
        elif self.token_atual.type == "DIV":
            self.consumir("DIV")
        else:
            self.erro(f"Esperado * ou /, mas recebeu: ^{self.token_atual.type}")
        

    def erro(self, texto):
        #usar esse metodo pra erro sintatico
        raise Exception(f"Erro feio erro rude de sintaxe: {texto} "
                        #boa burro vai ter que mexer no lexer de novo pq vc esqueceu de armazenar linha
                        f"Linha {self.token_atual.line}, coluna {self.token_atual.column}")