#DICIONARIO COM TODAS AS INSTRUCOES 
INSTRUCOES = {
    # Manipulação de Pilha
    'LDC': 'LoaD Constant - empilha constante',
    'LDV': 'LoaD Variable - empilha valor de variável',
    'STO': 'STOre - desempilha e armazena em variável',
    
    # Aritmética
    'ADD': 'ADDition - soma dois valores',
    'SUB': 'SUBtraction - subtrai dois valores',
    'MUL': 'MULtiplication - multiplica dois valores',
    'DIV': 'DIVision - divide dois valores',
    
    # Comparação
    'EQL': 'EQuaL - compara se igual (==)',
    'NEQ': 'Not EQual - compara se diferente (!=)',
    'LSS': 'LeSS than - menor que (<)',
    'GTR': 'GreaTeR than - maior que (>)',
    'LEQ': 'Less or EQual - menor ou igual (<=)',
    'GEQ': 'Greater or EQual - maior ou igual (>=)',
    
    # Controle de Fluxo
    'JMP': 'JuMP - pula incondicionalmente',
    'JMF': 'JuMp if False - pula se falso',
    'JMT': 'JuMp if True - pula se verdadeiro',
    
    # Funções
    'CALL': 'CALL function - chama função',
    'RET': 'RETurn - retorna de função',
    'ALLOC': 'ALLOCate - aloca memória',
    
    # I/O
    'READ': 'READ - lê entrada do usuário',
    'PRN': 'PRiNt - imprime valor',
    
    # Controle
    'HLT': 'HaLT - para execução',
    'NOP': 'No OPeration - não faz nada'
}