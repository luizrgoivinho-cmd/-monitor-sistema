
import os
import time
import psutil
from datetime import datetime

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

    if cpu > 80:
        alertas.append(f"CPU elevada: {cpu}%")

    if memoria.percent > 80:
        alertas.append(f"Memória RAM elevada: {memoria.percent}%")

    if alertas:
        print("\nStatus: Alerta! Uso elevado.")

        with open("alerta.log", "a") as arquivo:
            for alerta in alertas:
                horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                mensagem = f"{horario} - {alerta}"
                print(mensagem)
                arquivo.write(mensagem + "\n")
    else:
        print("\nStatus: Sistema normal.")

    print("\nAtualizando a cada 2 segundos...")
    print("=" * 35)

    time.sleep(1)

