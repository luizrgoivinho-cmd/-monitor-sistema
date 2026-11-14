import time

from coleta import (
    coletar_cpu,
    coletar_memoria,
    coletar_disco
)

from funcoes import (
    escolher_limite,
    normalizar_cpu,
    verificar_cpu,
    verificar_memoria,
    verificar_disco,
    registrar_alertas,
    controlar_alerta
)

from interface import (
    limpar_tela,
    exibir_cabecalho,
    exibir_recursos,
    exibir_status,
    exibir_rodape
)

def executar_ciclo(
    limite_cpu,
    limite_memoria,
    limite_disco,
    estados_alerta
):
    cpu = coletar_cpu()
    memoria = coletar_memoria()
    disco = coletar_disco().percent

    limpar_tela()
    exibir_cabecalho()
    exibir_recursos(cpu, memoria.percent, disco)

    alertas = []
    novos_alertas = []

    alerta_cpu = verificar_cpu(cpu, limite_cpu)

    novos, estados_alerta["cpu"] = controlar_alerta(
        estados_alerta["cpu"],
        alerta_cpu,
        normalizar_cpu(cpu)
    )

    if alerta_cpu is not None:
        alertas.append(alerta_cpu)

    novos_alertas.extend(novos)
    alerta_memoria = verificar_memoria(
        memoria.percent, limite_memoria
    )

    novos, estados_alerta["memoria"] = controlar_alerta(
        estados_alerta["memoria"],
        alerta_memoria,
        f"Memória RAM normalizada: {memoria.percent}%"
    )

    if alerta_memoria is not None:
        alertas.append(alerta_memoria)

    novos_alertas.extend(novos)

    alerta_disco = verificar_disco(disco, limite_disco)

    novos, estados_alerta["disco"] = controlar_alerta(
        estados_alerta["disco"],
        alerta_disco,
        f"Disco normalizado: {disco}%"
    )

    if alerta_disco is not None:
        alertas.append(alerta_disco)

    novos_alertas.extend(novos)

    exibir_status(alertas)

    if novos_alertas:
        registrar_alertas(novos_alertas)

    exibir_rodape()

def main():
    limite_cpu = escolher_limite("CPU")
    limite_memoria = escolher_limite("memória")
    limite_disco = escolher_limite("disco")

    estados_alerta = {
        "cpu": False,
        "memoria": False,
        "disco": False
    }

    while True:
        executar_ciclo(
            limite_cpu,
            limite_memoria,
            limite_disco,
            estados_alerta
        )

        time.sleep(1)

if __name__ == "__main__":
    main()