
import os
import time
import psutil
from datetime import datetime


def obter_limite(recurso):
    while True:
        try:
            limite = float(
                input(f"Qual o limite de {recurso} (0 a 100)? ")
            )

            if 0 <= limite <= 100:
                return limite

            print("Erro: digite um valor entre 0 e 100.")

        except ValueError:
            print("Erro: digite um número válido.")


def escolher_limite(recurso, padrao=80):
    while True:
        resposta = input(
            f"Deseja personalizar o limite de {recurso}? (s/n): "
        ).strip().lower()

        if resposta == "s":
            return obter_limite(recurso)

        if resposta == "n":
            return padrao

        print("Erro: digite 's' para sim ou 'n' para não.")


def verificar_cpu(cpu, limite=80):
    if cpu > limite:
        return f"CPU elevada: {cpu}%"
    return None


def verificar_memoria(memoria, limite=80):
    if memoria > limite:
        return f"Memória RAM elevada: {memoria}%"
    return None


def registrar_alertas(alertas):
    with open("alerta.log", "a") as arquivo:
        for alerta in alertas:
            horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mensagem = f"{horario} - {alerta}"
            print(mensagem)
            arquivo.write(mensagem + "\n")


limite_cpu = escolher_limite("CPU")
limite_memoria = escolher_limite("memória")


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

    alerta_cpu = verificar_cpu(cpu, limite_cpu)
    if alerta_cpu is not None:
        alertas.append(alerta_cpu)

    alerta_memoria = verificar_memoria(
        memoria.percent, limite_memoria
    )
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
