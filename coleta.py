import psutil

def coletar_cpu():
    cpu = psutil.cpu_percent(interval=1)
    return cpu

def coletar_memoria():
    memoria = psutil.virtual_memory()
    return memoria

def coletar_disco():
    disco = psutil.disk_usage("/")
    return disco