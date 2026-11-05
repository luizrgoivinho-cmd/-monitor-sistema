import os
import time
import psutil

from funcoes import (
    obter_limite,
    escolher_limite,
    normalizar_cpu,
    verificar_cpu,
    verificar_memoria,
    verificar_disco,
    registrar_alertas
)
def main():
    limite_cpu = escolher_limite("CPU")
    limite_memoria = escolher_limite("memória")
    limite_disco = escolher_limite("disco")

    cpu_em_alerta = False
    memoria_em_alerta = False
    disco_em_alerta = False


    while True:
        cpu = psutil.cpu_percent(interval=1)
        memoria = psutil.virtual_memory()
        disco = psutil.disk_usage("/").percent

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

        if alerta_cpu is not None:
            alertas.append(alerta_cpu)

            if not cpu_em_alerta:
                novos_alertas.append(alerta_cpu)

            cpu_em_alerta = True
        else:
            if cpu_em_alerta:
                novos_alertas.append(normalizar_cpu(cpu))

            cpu_em_alerta = False

        alerta_memoria = verificar_memoria(
            memoria.percent, limite_memoria
        )

        if alerta_memoria is not None:
            alertas.append(alerta_memoria)

            if not memoria_em_alerta:
                novos_alertas.append(alerta_memoria)

            memoria_em_alerta = True
        else:
            if memoria_em_alerta:
                novos_alertas.append(
                    f"Memória RAM normalizada: {memoria.percent}%"
                )

            memoria_em_alerta = False

        alerta_disco = verificar_disco(disco, limite_disco)

        if alerta_disco is not None:
            alertas.append(alerta_disco)

            if not disco_em_alerta:
                novos_alertas.append(alerta_disco)

            disco_em_alerta = True
        else:
            if disco_em_alerta:
                novos_alertas.append(
                    f"Disco normalizado: {disco}%"
                )

            disco_em_alerta = False

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