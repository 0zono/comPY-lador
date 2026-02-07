from lexer.Token import Token

palavras_reservadas = {
    "def": "DEF",
    "print": "PRINT",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "input": "INPUT",
    "read": "INPUT"  # ADICIONADO: aceitar 'read' como sinônimo de 'input'
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

    def nextToken(self):
        # Pula espaços e comentários
        while not self.isEOF():
            c = self.texto[self.pos]
            
            # Verificar comentário triplo """
            if c == '"' and self.pos + 2 < self.tamanho:
                if self.texto[self.pos:self.pos+3] == '"""':
                    self.pular_comentario_triplo()
                    continue
            
            if self.isEspaco(c):
                self.nextChar()
            else:
                break
        
        if self.isEOF():
            return Token("EOF", "EOF", self.linha, self.coluna)
        
        # Atualizar token position
        token_linha = self.linha
        token_coluna = self.coluna
        
        c = self.nextChar()
        
        # IDENTIFICADORES E KEYWORDS
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
        
        # NÚMEROS
        elif self.isDigito(c):
            lexema = c
            tem_ponto = False
            
            while not self.isEOF():
                c = self.texto[self.pos]
                if self.isDigito(c):
                    lexema += c
                    self.nextChar()
                elif c == '.' and not tem_ponto:
                    # Verificar se há dígito depois do ponto
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
        
        # OPERAÇÕES
        elif c in ['+', '-', '*', '/', '(', ')', ',', ':', '=', '<', '>', '!']:
            lexema = c
            
            # Operadores compostos: ==, <=, >=, !=
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
            
            # Operador simples
            if lexema in operacoes:
                return Token(operacoes[lexema], lexema, token_linha, token_coluna)
            else:
                return Token("ERRO", lexema, token_linha, token_coluna)
        
        # Caractere desconhecido
        else:
            return Token("ERRO", c, token_linha, token_coluna)

    def pular_comentario_triplo(self):
        """Pula comentário delimitado por três aspas duplas"""
        # Consumir as três aspas iniciais
        self.nextChar()  # primeira "
        self.nextChar()  # segunda "
        self.nextChar()  # terceira "
        
        # Procurar as três aspas finais
        while not self.isEOF():
            if self.pos + 2 < self.tamanho:
                if self.texto[self.pos:self.pos+3] == '"""':
                    # Consumir as três aspas finais
                    self.nextChar()
                    self.nextChar()
                    self.nextChar()
                    return
            self.nextChar()

    # Métodos utilitários
    def isLetra(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z')
    
    def isDigito(self, c):
        return ('0' <= c <= '9')
    
    def isEspaco(self, c):
        return c in [' ', '\n', '\t', '\r']

    def isEOF(self):
        return self.pos >= self.tamanho
    
    def nextChar(self):
        c = self.texto[self.pos]
        self.pos += 1
        
        # Atualiza linha e coluna
        if c == '\n':
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
            
        return c
    
    def back(self):
        if self.pos > 0:
            self.pos -= 1
            if self.coluna > 1:
                self.coluna -= 1