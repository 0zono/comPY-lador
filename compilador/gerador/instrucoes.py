#DICIONARIO COM TODAS AS INSTRUCOES 
# ASSEMBLY
INSTRUCOES = {
    # memoria
    'CRCT': 'carrega constante - carrega uma constante no topo', # RECEBE O VALOR (ex: CRCT 69 - no topo da pilha agora temos o int '69')
    'CRVL': 'load variavel - carrega valor de uma variável no topo', # RECEBE O ENDERECO DE MEMORIA (ex: CRCT 67 - no topo da pilha agora temos o valor contido no ENDEREÇO 67)
    'ARMZ': 'store - desempilha e armazena em variável', # mete o valor no topo da pilha na memoria (ex: STO 420 - ARMAZENA NO END 420)
    
    # operacoes
    'SOMA': 'adicao - adiciona valores',
    'SUBT': 'subtracao - subtrai dois valores',
    'MULT': 'multiplicacao - multiplica dois valores',
    'DIVI': 'DIVision - divide dois valores',
    'INVE': 'Inverte o sinal do topo',
    
    
    # comparacoes
    'CPIG': 'igual - compara se o TOS e NOS(Top on Stack, e Next on Stack) sao iguais a 1', # CRVL 69 (1), CRVL 67 (1), EQL  (69 == 67)
    'CDES': 'nao igual - compara se TOS e NOS sao diferentes', # (!=)
    'CPME': 'menor que - compara se TOS é menor q NOS', # <
    'CPMA': 'maior que - compara se TOS é maior que NOS', # >
    'CPMI': 'maior ou igual - compara se o TOS é menor ou igual ao NOS ', # <=
    'CMAI': 'menor ou igual - compara se o TOS é maior ou igual ao NOS', # >=
    
    # condicionais
    'DSVI': 'pula para instrucao - pula incondicionalmente para instrucao',  
    'DSVF': 'pula se falso - pula se falso para instrucao',
    #'DSVV': 'pula se verdade - pula se verdadeiro para instrucoa',
    
    # funcoes
    'CALL': 'CALL function - chama função',
    'PARAM': 'PARAMETER - empilha o valor da variável n como PARAMETRO de procedimento/função',
    'RTPR': 'RETURN - retorna de função',
    'ALME': 'ALLOCATE - aloca memoria',
    'PUSHER': 'PUSH RETURN - empilha o endereço de retorno da chamada do procedimento',
    
    # e/s
    'LEIT': 'READ - le entrada do usuario',
    'IMPR': 'PRINT - imprime valor',
    
    # util
    'INPP': 'INIT PROGRAM - inicia o programa e inicializa a pilha (s := -1)',
    'PARA': 'PARA - para execução',
    #'NOP': 'NO OP - não faz nada'
}