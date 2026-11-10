import os
import time

from coleta import (
    coletar_cpu,
    coletar_memoria,
    coletar_disco
)

from funcoes import (
    obter_limite,
    escolher_limite,
    normalizar_cpu,
    verificar_cpu,
    verificar_memoria,
    verificar_disco,
    registrar_alertas,
    controlar_alerta
)
def main():
    limite_cpu = escolher_limite("CPU")
    limite_memoria = escolher_limite("memória")
    limite_disco = escolher_limite("disco")

    cpu_em_alerta = False
    memoria_em_alerta = False
    disco_em_alerta = False

    while True:
        cpu = coletar_cpu()
        memoria = coletar_memoria()
        disco = coletar_disco().percent

        os.system("clear")

        print("=" * 35)
        print("       MONITOR DE SISTEMAS")
        print("=" * 35)

        print(f"\nCPU:       {cpu}%")
        print(f"Memória:   {memoria.percent}%")
        print(f"Disco:     {disco}%")

        alertas = []
        novos_alertas = []

        alerta_cpu = verificar_cpu(cpu, limite_cpu)

        novos, cpu_em_alerta = controlar_alerta(
            cpu_em_alerta,
            alerta_cpu,
            normalizar_cpu(cpu)
        )

        if alerta_cpu is not None:
            alertas.append(alerta_cpu)

        novos_alertas.extend(novos)

        alerta_memoria = verificar_memoria(
            memoria.percent, limite_memoria
        )

        novos, memoria_em_alerta = controlar_alerta(
            memoria_em_alerta,
            alerta_memoria,
            f"Memória RAM normalizada: {memoria.percent}%"
        )

        if alerta_memoria is not None:
            alertas.append(alerta_memoria)

        novos_alertas.extend(novos)

        alerta_disco = verificar_disco(disco, limite_disco)

        novos, disco_em_alerta = controlar_alerta(
            disco_em_alerta,
            alerta_disco,
            f"Disco normalizado: {disco}%"
        )

        if alerta_disco is not None:
            alertas.append(alerta_disco)

        novos_alertas.extend(novos)

        if alertas:
            print("\nStatus: Alerta! Uso elevado.")

        else:
            print("\nStatus: Sistema normal.")

        if novos_alertas:
            registrar_alertas(novos_alertas)

        print("=" * 35)
        print("\nAtualizando a cada 2 segundos...")
        print("=" * 35)

        time.sleep(1)

if __name__ == "__main__":
    main()