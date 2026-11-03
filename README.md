# Monitor de Sistemas

Projeto desenvolvido em Python para monitorar o uso de recursos do computador.

## Funcionalidades

- Monitoramento do uso da CPU.
- Monitoramento do uso da memória RAM.
- Configuração de limites personalizados.
- Identificação de uso elevado dos recursos.
- Registro de alertas em arquivo de log.
- Identificação da normalização dos recursos.

## Tecnologias utilizadas

- Python
- psutil
- Git e GitHub
- Linux (Ubuntu)

## Requisitos

- Python 3 instalado.
- Biblioteca psutil.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/luizrgoivinho-cmd/-monitor-sistema.git
```

Entre na pasta:

```bash
cd ./-monitor-sistema
```

Crie um ambiente virtual:

```bash
python3 -m venv .venv
```

Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Instale a dependência:

```bash
pip install -r requirements.txt
```

## Execução

Execute o programa:

```bash
python monitor.py
```
