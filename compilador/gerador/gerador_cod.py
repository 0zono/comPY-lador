"""
Gerador de Código para Máquina Hipotética a Pilha
Gera código Assembly com as instruções: CRCT, CRVL, ARMZ, SOMA, etc.
"""

class GeradorCodigo:
    """Gera código Assembly para máquina a pilha"""
    
    def __init__(self):
        self.codigo = []                    # Lista de instruções geradas
        self.tabela_enderecos = {}          # {nome_variavel: endereco}
        self.contador_endereco = 0          # Próximo endereço disponível
        self.contador_label = 0             # Para gerar labels únicos
        
    def novo_endereco(self, nome):
        """Aloca novo endereço para variável"""
        if nome not in self.tabela_enderecos:
            self.tabela_enderecos[nome] = self.contador_endereco
            self.contador_endereco += 1
        return self.tabela_enderecos[nome]
    
    def obter_endereco(self, nome):
        """Retorna endereço de variável existente"""
        if nome not in self.tabela_enderecos:
            raise Exception(f"Variável '{nome}' não encontrada")
        return self.tabela_enderecos[nome]
    
    def novo_label(self):
        """Gera um novo label único"""
        label = f"L{self.contador_label}"
        self.contador_label += 1
        return label
    
    def emitir(self, instrucao, argumento=None):
        """Emite uma instrução"""
        if argumento is not None:
            self.codigo.append(f"{instrucao} {argumento}")
        else:
            self.codigo.append(instrucao)
    
    def endereco_atual(self):
        """Retorna o endereço da próxima instrução"""
        return len(self.codigo)
    
    def backpatch(self, endereco, novo_destino):
        """Corrige endereço de salto após saber o destino"""
        instrucao = self.codigo[endereco]
        partes = instrucao.split()
        self.codigo[endereco] = f"{partes[0]} {novo_destino}"
    
    # ===== GERAÇÃO DE CÓDIGO =====
    
    def gerar_expressao(self, node):
        """Gera código para expressão"""
        if node['tipo'] == 'numero':
            self.emitir("CRCT", node['valor'])
            
        elif node['tipo'] == 'variavel':
            endereco = self.obter_endereco(node['nome'])
            self.emitir("CRVL", endereco)
            
        elif node['tipo'] == 'binaria':
            # Gera código para operandos (ordem: esquerda, direita)
            self.gerar_expressao(node['esquerda'])
            self.gerar_expressao(node['direita'])
            
            # Gera operação
            operador = node['operador']
            if operador == '+':
                self.emitir("SOMA")
            elif operador == '-':
                self.emitir("SUBT")
            elif operador == '*':
                self.emitir("MULT")
            elif operador == '/':
                self.emitir("DIVI")
            elif operador == '==':
                self.emitir("CPIG")
            elif operador == '!=':
                self.emitir("CDES")
            elif operador == '<':
                self.emitir("CPME")
            elif operador == '>':
                self.emitir("CPMA")
            elif operador == '<=':
                self.emitir("CPMI")
            elif operador == '>=':
                self.emitir("CMAI")
                
        elif node['tipo'] == 'unaria':
            # Para operador unário (ex: -x)
            self.gerar_expressao(node['operando'])
            if node['operador'] == '-':
                self.emitir("INVE")
                
        elif node['tipo'] == 'input':
            self.emitir("LEIT")
    
    def gerar_comando(self, node):
        """Gera código para comando"""
        if node['tipo'] == 'declaracao':
            # x = expressao
            self.gerar_expressao(node['expressao'])
            endereco = self.novo_endereco(node['nome'])
            self.emitir("ARMZ", endereco)
            
        elif node['tipo'] == 'atribuicao':
            # x = expressao (variável já existe)
            self.gerar_expressao(node['expressao'])
            endereco = self.obter_endereco(node['nome'])
            self.emitir("ARMZ", endereco)
            
        elif node['tipo'] == 'print':
            # print(x)
            endereco = self.obter_endereco(node['variavel'])
            self.emitir("CRVL", endereco)
            self.emitir("IMPR")
            
        elif node['tipo'] == 'if':
            # if condicao: bloco_then else: bloco_else
            self.gerar_expressao(node['condicao'])
            
            endereco_dsvf = self.endereco_atual()
            self.emitir("DSVF", "???")  # Será corrigido
            
            # Bloco THEN
            for cmd in node['then']:
                self.gerar_comando(cmd)
            
            if node.get('else'):
                # Tem ELSE
                endereco_dsvi = self.endereco_atual()
                self.emitir("DSVI", "???")  # Pula o else
                
                # Corrige DSVF para apontar para o ELSE
                self.backpatch(endereco_dsvf, self.endereco_atual())
                
                # Bloco ELSE
                for cmd in node['else']:
                    self.gerar_comando(cmd)
                
                # Corrige DSVI para apontar depois do ELSE
                self.backpatch(endereco_dsvi, self.endereco_atual())
            else:
                # Sem ELSE, DSVF pula direto para depois do IF
                self.backpatch(endereco_dsvf, self.endereco_atual())
                
        elif node['tipo'] == 'while':
            # while condicao: bloco
            inicio_loop = self.endereco_atual()
            
            self.gerar_expressao(node['condicao'])
            
            endereco_dsvf = self.endereco_atual()
            self.emitir("DSVF", "???")  # Sai do loop se falso
            
            # Corpo do loop
            for cmd in node['bloco']:
                self.gerar_comando(cmd)
            
            # Volta para início do loop
            self.emitir("DSVI", inicio_loop)
            
            # Corrige DSVF para apontar depois do loop
            self.backpatch(endereco_dsvf, self.endereco_atual())
    
    def gerar_programa(self, programa):
        """Gera código completo"""
        self.emitir("INPP")  # Inicializa programa
        
        for comando in programa:
            self.gerar_comando(comando)
        
        self.emitir("PARA")  # Para execução
    
    def salvar(self, arquivo):
        """Salva código em arquivo .obj"""
        with open(arquivo, 'w', encoding='utf-8') as f:
            for instr in self.codigo:
                f.write(f"{instr}\n")
        print(f"\n✓ Código objeto salvo em: {arquivo}")
    
    def exibir(self):
        """Exibe código gerado"""
        print("\n" + "="*60)
        print("CÓDIGO ASSEMBLY GERADO")
        print("="*60)
        for i, instr in enumerate(self.codigo):
            print(f"{i:3d}: {instr}")
        print("="*60)
        print(f"\nVariáveis: {self.tabela_enderecos}")
        print(f"Total de instruções: {len(self.codigo)}")
        print("="*60)