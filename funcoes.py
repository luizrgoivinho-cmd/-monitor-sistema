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

def normalizar_cpu(cpu):
    return f"CPU normalizada: {cpu}%"

def verificar_cpu(cpu, limite=80):
    if cpu > limite:
        return f"CPU elevada: {cpu}%"
    return None


def verificar_memoria(memoria, limite=80):
    if memoria > limite:
        return f"Memória RAM elevada: {memoria}%"
    return None

def verificar_disco(disco, limite=80):
    if disco > limite:
        return f'uso do disco elevado: {disco}%'
    return None


def registrar_alertas(alertas):
    with open("alerta.log", "a") as arquivo:
        for alerta in alertas:
            horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mensagem = f"{horario} - {alerta}"
            print(mensagem)
            arquivo.write(mensagem + "\n")

def controlar_alerta(estado_atual, alerta, normalizacao):
    novos_alertas = []

    if alerta is not None:
        if not estado_atual:
            novos_alertas.append(alerta)

        estado_atual = True

    else:
        if estado_atual:
            novos_alertas.append(normalizacao)

        estado_atual = False

    return novos_alertas, estado_atual