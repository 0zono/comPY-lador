# instrucoes_exec.py
# Implementação das instruções da máquina virtual
# Baseado na documentação oficial da linguagem

def instrucoes_exec(vm, instrucao):
    partes = instrucao.split()
    opcode = partes[0]
    argumento = None
    if len(partes) > 1:
        argumento = float(partes[1]) if '.' in partes[1] else int(partes[1])

    # ============== MEMÓRIA ==============
    
    if opcode == "CRCT":
        # Carrega constante k no topo
        # s := s+1; D[s] := k
        vm.push(argumento)

    elif opcode == "CRVL":
        # Carrega valor do endereço n
        # s := s+1; D[s] := D[n]
        if argumento not in vm.memoria:
            vm.memoria[argumento] = 0
        vm.push(vm.memoria[argumento])

    elif opcode == "ARMZ":
        # Armazena topo no endereço n
        # D[n] := D[s]; s := s-1
        vm.memoria[argumento] = vm.pop()

    # ============== OPERAÇÕES ARITMÉTICAS ==============

    elif opcode == "SOMA":
        # D[s-1] := D[s-1] + D[s]; s := s-1
        b = vm.pop()
        a = vm.pop()
        vm.push(a + b)

    elif opcode == "SUBT":
        # D[s-1] := D[s-1] - D[s]; s := s-1
        b = vm.pop()
        a = vm.pop()
        vm.push(a - b)

    elif opcode == "MULT":
        # D[s-1] := D[s-1] * D[s]; s := s-1
        b = vm.pop()
        a = vm.pop()
        vm.push(a * b)

    elif opcode == "DIVI":
        # D[s-1] := D[s-1] div D[s]; s := s-1
        b = vm.pop()
        a = vm.pop()
        if b == 0:
            raise Exception(f"Divisão por zero no PC={vm.pc}")
        vm.push(a // b)

    elif opcode == "INVE":
        # Inverte sinal do topo
        # D[s] := -D[s]
        vm.push(-vm.pop())

    # ============== OPERAÇÕES LÓGICAS ==============

    elif opcode == "CONJ":
        # Conjunção (AND)
        # se D[s-1]=1 e D[s]=1 então D[s-1]:=1 senão D[s-1]:=0
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if (a == 1 and b == 1) else 0)

    elif opcode == "DISJ":
        # Disjunção (OR)
        # se D[s-1]=1 ou D[s]=1 então D[s-1]:=1 senão D[s-1]:=0
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if (a == 1 or b == 1) else 0)

    elif opcode == "NEGA":
        # Negação lógica (NOT)
        # D[s] := 1 - D[s]
        vm.push(1 - vm.pop())

    # ============== COMPARAÇÕES ==============

    elif opcode == "CPME":
        # Comparação menor que (<)
        # se D[s-1] < D[s] então D[s-1]:=1 senão D[s-1]:=0
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if a < b else 0)

    elif opcode == "CPMA":
        # Comparação maior que (>)
        # se D[s-1] > D[s] então D[s-1]:=1 senão D[s-1]:=0
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if a > b else 0)

    elif opcode == "CPIG":
        # Comparação igual (==)
        # se D[s-1] = D[s] então D[s-1]:=1 senão D[s-1]:=0
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if a == b else 0)

    elif opcode == "CDES":
        # Comparação diferente (!=)
        # se D[s-1] <> D[s] então D[s-1]:=1 senão D[s-1]:=0
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if a != b else 0)

    elif opcode == "CPMI":
        # Comparação menor ou igual (<=)
        # se D[s-1] <= D[s] então D[s-1]:=1 senão D[s-1]:=0
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if a <= b else 0)

    elif opcode == "CMAI":
        # Comparação maior ou igual (>=)
        # se D[s-1] >= D[s] então D[s-1]:=1 senão D[s-1]:=0
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if a >= b else 0)

    # ============== DESVIOS ==============

    elif opcode == "DSVI":
        # Desvio incondicional
        # i := p
        vm.pc = argumento - 1  # -1 porque será incrementado no loop

    elif opcode == "DSVF":
        # Desvio condicional se falso
        # se D[s]=0 então i:=p; s:=s-1
        if vm.pop() == 0:
            vm.pc = argumento - 1

    # ============== ENTRADA/SAÍDA ==============

    elif opcode == "LEIT":
        # Lê entrada
        # s := s+1; D[s] := "valor da entrada"
        try:
            valor = float(input("? "))
            # Verifica se é inteiro
            if valor == int(valor):
                valor = int(valor)
            vm.push(valor)
        except ValueError:
            vm.push(0)

    elif opcode == "IMPR":
        # Imprime valor do topo
        # "imprimir D[s]"; s := s-1
        print(f"> {vm.pop()}")

    # ============== GERENCIAMENTO DE PROGRAMA ==============

    elif opcode == "INPP":
        # Inicializa programa
        # s := -1
        vm.pilha = []
        vm.memoria = {}

    elif opcode == "PARA":
        # Para execução
        vm.executando = False

    # ============== ALOCAÇÃO DE MEMÓRIA ==============

    elif opcode == "ALME":
        # Aloca m posições na pilha
        # s := s + m
        # Em Python, não precisamos fazer nada explicitamente
        # A pilha cresce dinamicamente
        pass

    elif opcode == "DESM":
        # Desaloca m posições do topo
        # s := s - m
        for _ in range(argumento):
            if vm.pilha:
                vm.pilha.pop()

    # ============== CHAMADA DE PROCEDIMENTO ==============

    elif opcode == "CHPR":
        # Chama procedimento no endereço p
        # Salva endereço de retorno na pilha de retorno
        vm.pilha_retorno.append(vm.pc)
        vm.pc = argumento - 1  # -1 porque será incrementado

    elif opcode == "RTPR":
        # Retorna de procedimento
        # Recupera endereço de retorno da pilha de retorno
        if vm.pilha_retorno:
            vm.pc = vm.pilha_retorno.pop()
        else:
            # Se não há retorno, termina execução
            vm.executando = False

    # ============== INSTRUÇÃO DESCONHECIDA ==============

    else:
        raise Exception(f"Instrução desconhecida '{opcode}' no PC={vm.pc}")