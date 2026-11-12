import os


def limpar_tela():
    os.system("clear")


def exibir_cabecalho():
    print("=" * 35)
    print("       MONITOR DE SISTEMAS")
    print("=" * 35)


def exibir_recursos(cpu, memoria, disco):
    print(f"\nCPU:       {cpu}%")
    print(f"Memória:   {memoria}%")
    print(f"Disco:     {disco}%")


def exibir_status(alertas):
    if alertas:
        print("\nStatus: Alerta! Uso elevado.")

    else:
        print("\nStatus: Sistema normal.")


def exibir_rodape():
    print("=" * 35)
    print("\nAtualizando a cada 2 segundos...")
    print("=" * 35)