# CRCT, CRVL, ARMZ, SOMA, SUBT, MULT, DIVI, INVE, CPIG, CDES, CPME, CPMA, CPMI, CMAI, DSVI, DSVF, CALL, PARAM, RTPR, ALME, PUSHER, LEIT, IMPR, INPP, PARA

def instrucoes_exec(vm, instrucao):
    partes = instrucao.split()
    opcode = partes[0]
    argumento = None
    if len(partes) > 1:
        argumento = float(partes[1]) if '.' in partes[1] else int(partes[1])

    if opcode == "CRCT":
        vm.push(argumento)

    elif opcode == "CRVL":
        if argumento not in vm.memoria:
            vm.memoria[argumento] = 0
        vm.push(vm.memoria[argumento])

    elif opcode == "ARMZ":
        vm.memoria[argumento] = vm.pop()

    elif opcode == "SOMA":
        b = vm.pop()
        a = vm.pop()
        vm.push(a + b)

    elif opcode == "SUBT":
        b = vm.pop()
        a = vm.pop()
        vm.push(a - b)

    elif opcode == "MULT":
        b = vm.pop()
        a = vm.pop()
        vm.push(a * b)

    elif opcode == "DIVI":
        b = vm.pop()
        a = vm.pop()
        if b == 0:
            raise Exception(f"Divisão por zero no PC={vm.pc}")
        vm.push(a // b)

    elif opcode == "INVE":
        vm.push(-vm.pop())

    elif opcode == "CPIG":
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if a == b else 0)

    elif opcode == "CDES":
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if a != b else 0)

    elif opcode == "CPME":
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if a < b else 0)

    elif opcode == "CPMA":
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if a > b else 0)

    elif opcode == "CPMI":
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if a <= b else 0)

    elif opcode == "CMAI":
        b = vm.pop()
        a = vm.pop()
        vm.push(1 if a >= b else 0)

    elif opcode == "DSVI":
        vm.pc = argumento - 1

    elif opcode == "DSVF":
        if vm.pop() == 0:
            vm.pc = argumento - 1

    elif opcode == "LEIT":
        try:
            vm.push(int(input("? ")))
        except ValueError:
            vm.push(0)

    elif opcode == "IMPR":
        print(f"PRINT:> {vm.pop()}")

    elif opcode == "INPP":
        vm.pilha = []
        vm.memoria = {}
        vm.pc = 0

    elif opcode == "PARA":
        vm.executando = False

    elif opcode == "PARAM":
        vm.push(vm.pop())

    elif opcode == "CHPR":
        vm.push(vm.pc + 1)   # endereço de retorno
        vm.pc = argumento - 1

    elif opcode == "RTPR":
        retorno = vm.pop()
        vm.pc = retorno - 1





    else:
        raise Exception(f"Instrução desconhecida '{opcode}' no PC={vm.pc}")
