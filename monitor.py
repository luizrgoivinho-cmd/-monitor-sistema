
import os
import time
import psutil
from datetime import datetime

def verificar_cpu(cpu):
    if cpu > 80:
        return f"cpu elevada: {cpu}%"
    return None

def verificar_memoria(memoria):
    if memoria > 80:
        return f"Memoria RAM elevada: {memoria}%"
    return None

def registrar_alertas(alertas):
    with open("alerta.log", "a") as arquivos:
        for alerta in alertas:
            horario = datetime.now().strfti3me("%Y-%m-%d %H:%M:%S")
            mensagem = f"{horario} - {alerta}"
            print(mensagem)
            arquivo.write(mensagem + "\n")



while True:
    cpu = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory()

    os.system("clear")

    print("=" * 35)
    print("       MONITOR DE SISTEMAS")
    print("=" * 35)

    print(f"\nCPU:       {cpu}%")
    print(f"Memória:   {memoria.percent}%")

    alertas = []

    alerta_cpu = verificar_cpu(cpu)
    if alerta_cpu is not None:
        alertas.append(alerta_cpu)

    alerta_memoria = verificar_memoria(memoria.percent)
    if alerta_memoria is not None:
        alertas.append(alerta_memoria)

    if alertas:
        print("\nStatus: Alerta! Uso elevado.")
        registrar_alertas(alertas)
    else:
        print("\nStatus: Sistema normal.")

    print("\nAtualizando a cada 2 segundos...")
    print("=" * 35)

    time.sleep(1)

