# # fazer  o stack management
# # Areas: CODIGO, DADOS, REGISTRADORES DE BASe
# # CODIGO: vetor (array)
# # DADOS: pilha
# # REGISTRADORES DE BASE: vai ficar na parte da VM

# class Gerador:
#     def __init__(self):
#         self.codigo = [] # vetor que conterá as instrucoes geradas
#         self.tabela_enderecos = {}
#         self.cont_endereco = 0

#     def novo_end(self, nome): #aloca end para variavel
#         if nome not in self.tabela_enderecos: #checa se a variavel ja existe (futuro, checar se ha memoria alocada pra ela)
#             self.tabela_enderecos[nome] = self.cont_endereco # se não existe cria um end pra ela
#             self.cont_endereco += 1
#         return self.tabela_enderecos[nome]
    
#     def get_end(self, nome):
#         if nome in self.tabela_enderecos:
#             return self.tabela_enderecos[nome]
#         else:
#             raise Exception("Variavel não encontrada.") #melhorar erro
    
#     def emitir(self, instrucao, argumento=None):
