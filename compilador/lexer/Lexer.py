from lexer.Token import Token

palavras_reservadas = {
    "def": "DEF",
    "print": "PRINT",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "input": "INPUT",
    "read": "INPUT"
}

operacoes = {
    '+': "SOMA",
    '-': "SUB",
    '*': "MULT",
    '/': "DIV",
    '(': "ABREPAR",
    ')': "FECHAPAR",
    ',': "VIRG",
    ':': "DOISPTS",
    '=': "ATRIB",
    '<': "MENOR",
    '>': "MAIOR",
    '!': "NEG"
}

class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.tamanho = len(texto)
        self.pos = 0
        self.linha = 1
        self.coluna = 1
        
        # indent agora funciona
        self.pilha_indentacao = [0]
        self.tokens_pendentes = []
        self.inicio_linha = True
        self.nivel_parenteses = 0

    def nextToken(self):
        
        if self.tokens_pendentes:
            return self.tokens_pendentes.pop(0)
        
        # Pula espacos e coments
        while not self.isEOF():
            c = self.texto[self.pos]
            
            # coment '''
            if c == '"' and self.pos + 2 < self.tamanho:
                if self.texto[self.pos:self.pos+3] == '"""':
                    self.pular_comentario_triplo()
                    continue
            
            # comentario de linha
            if c == '#':
                self.pular_ate_fim_linha()
                continue
            
            # novalinha
            if c == '\n':
                self.nextChar()
                if self.nivel_parenteses == 0 and not self.inicio_linha:
                    self.inicio_linha = True
                continue
            
            # ini linha
            if self.inicio_linha and c not in [' ', '\t', '\r', '\n']:
                return self.processar_indentacao()
            
            
            if c in [' ', '\t', '\r']:
                self.nextChar()
                continue
            
            break
        
        if self.isEOF():
            
            while len(self.pilha_indentacao) > 1:
                self.pilha_indentacao.pop()
                self.tokens_pendentes.append(Token("DEDENT", "", self.linha, self.coluna))
            
            if self.tokens_pendentes:
                return self.tokens_pendentes.pop(0)
            
            return Token("EOF", "EOF", self.linha, self.coluna)
        
        
        token_linha = self.linha
        token_coluna = self.coluna
        c = self.nextChar()
        
        
        if c == '(':
            self.nivel_parenteses += 1
            return Token("ABREPAR", c, token_linha, token_coluna)
        if c == ')':
            self.nivel_parenteses -= 1
            return Token("FECHAPAR", c, token_linha, token_coluna)
        
        # IDENTIFICADORES E PALAVRAS CHAVE
        if self.isLetra(c):
            lexema = c
            while not self.isEOF():
                c = self.texto[self.pos]
                if self.isLetra(c) or self.isDigito(c) or c == '_':
                    lexema += c
                    self.nextChar()
                else:
                    break
            
            if lexema in palavras_reservadas:
                return Token(palavras_reservadas[lexema], lexema, token_linha, token_coluna)
            else:
                return Token("IDENT", lexema, token_linha, token_coluna)
        
        # NUMEROS
        elif self.isDigito(c):
            lexema = c
            tem_ponto = False
            
            while not self.isEOF():
                c = self.texto[self.pos]
                if self.isDigito(c):
                    lexema += c
                    self.nextChar()
                elif c == '.' and not tem_ponto:
                    if self.pos + 1 < self.tamanho and self.isDigito(self.texto[self.pos + 1]):
                        tem_ponto = True
                        lexema += c
                        self.nextChar()
                    else:
                        break
                else:
                    break
            
            return Token("NUM", lexema, token_linha, token_coluna)
        
        # STRINGS
        elif c == '"':
            lexema = ""
            while not self.isEOF():
                c = self.nextChar()
                
                if c == '"':
                    return Token("STRING", lexema, token_linha, token_coluna)
                elif c == '\\':
                    if self.isEOF():
                        return Token("ERRO", "String não fechada", token_linha, token_coluna)
                    
                    prox = self.nextChar()
                    if prox == 'n':
                        lexema += '\n'
                    elif prox == 't':
                        lexema += '\t'
                    elif prox == '"':
                        lexema += '"'
                    elif prox == '\\':
                        lexema += '\\'
                    else:
                        lexema += prox
                else:
                    lexema += c
            
            return Token("ERRO", "String não fechada", token_linha, token_coluna)
        
        # OPERACOES
        elif c in ['+', '-', '*', '/', ',', ':', '=', '<', '>', '!']:
            lexema = c
            
            # Operadores de igualdade
            if not self.isEOF():
                proximo = self.texto[self.pos]
                
                if proximo == '=':
                    if c == '=':
                        self.nextChar()
                        return Token("IGUAL", "==", token_linha, token_coluna)
                    elif c == '<':
                        self.nextChar()
                        return Token("MENOR_IGUAL", "<=", token_linha, token_coluna)
                    elif c == '>':
                        self.nextChar()
                        return Token("MAIOR_IGUAL", ">=", token_linha, token_coluna)
                    elif c == '!':
                        self.nextChar()
                        return Token("DIFF", "!=", token_linha, token_coluna)
            
            if lexema in operacoes:
                return Token(operacoes[lexema], lexema, token_linha, token_coluna)
            else:
                return Token("ERRO", lexema, token_linha, token_coluna)
        
        else:
            return Token("ERRO", c, token_linha, token_coluna)

    def processar_indentacao(self):
        """Processa indentação no início de linha"""
        self.inicio_linha = False
        
        
        pos_backup = self.pos
        
        
        while pos_backup > 0 and self.texto[pos_backup - 1] != '\n':
            pos_backup -= 1
        
        
        nivel_atual = 0
        i = pos_backup
        while i < self.tamanho and self.texto[i] in [' ', '\t']:
            if self.texto[i] == ' ':
                nivel_atual += 1
            else: 
                nivel_atual += 4
            i += 1
        
        
        if i < self.tamanho and self.texto[i] in ['\n', '#']:
            return self.nextToken()
        
        nivel_anterior = self.pilha_indentacao[-1]
        
        if nivel_atual > nivel_anterior:
            # INDENT
            self.pilha_indentacao.append(nivel_atual)
            return Token("INDENT", "", self.linha, 1)
        
        elif nivel_atual < nivel_anterior:
            
            dedents = []
            while self.pilha_indentacao and self.pilha_indentacao[-1] > nivel_atual:
                self.pilha_indentacao.pop()
                dedents.append(Token("DEDENT", "", self.linha, 1))
            
            if not self.pilha_indentacao or self.pilha_indentacao[-1] != nivel_atual:
                
                return Token("ERRO", f"Indentação inválida (esperado {self.pilha_indentacao[-1] if self.pilha_indentacao else 0}, encontrado {nivel_atual})", self.linha, 1)
            
            
            if len(dedents) > 1:
                self.tokens_pendentes = dedents[1:]
            return dedents[0]
        
        
        return self.nextToken()

    def pular_comentario_triplo(self):
        
        self.nextChar()
        self.nextChar()
        self.nextChar()
        
        while not self.isEOF():
            if self.pos + 2 < self.tamanho:
                if self.texto[self.pos:self.pos+3] == '"""':
                    self.nextChar()
                    self.nextChar()
                    self.nextChar()
                    return
            self.nextChar()

    def pular_ate_fim_linha(self):
        
        while not self.isEOF() and self.texto[self.pos] != '\n':
            self.nextChar()

    def isLetra(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z')
    
    def isDigito(self, c):
        return ('0' <= c <= '9')

    def isEOF(self):
        return self.pos >= self.tamanho
    
    def nextChar(self):
        c = self.texto[self.pos]
        self.pos += 1
        
        if c == '\n':
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
            
        return c