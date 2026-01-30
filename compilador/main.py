import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Como executar: python main.py <arquivo.txt> [--run]")
        return

    arquivo = sys.argv[1]

    # Compilar
    if arquivo.endswith(".txt") and "--run" not in sys.argv:
        print(f"Compilando {arquivo} ...")
        print("** Compilador ainda não implementado **")
        # Aqui futuramente você chamará o compilador de verdade.

    # Executar VM
    if "--run" in sys.argv:
        print(f"Executando máquina virtual com {arquivo} ...")
        print("** VM ainda não implementada **")
        # Aqui futuramente você chamará a VM.

if __name__ == "__main__":
    main()
