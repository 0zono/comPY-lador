class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
 

    def exibir(self):
        return f"Token(tipo: {self.type}, valor: {self.value}, linha: {self.line}, coluna: {self.column})"