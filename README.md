# Monitor de Sistemas

Projeto desenvolvido em Python para monitorar o uso de recursos do computador, como CPU, memória RAM e disco, identificando situações de uso elevado e registrando alertas.

## Funcionalidades

- Monitoramento do uso da CPU.
- Monitoramento do uso da memória RAM.
- Monitoramento do uso do disco.
- Configuração de limites personalizados para CPU, memória e disco.
- Identificação de uso elevado dos recursos.
- Identificação da normalização dos recursos.
- Registro de alertas em arquivo de log (`alerta.log`).
- Prevenção de alertas repetidos enquanto um recurso permanece acima do limite.

## Tecnologias utilizadas

- Python
- psutil
- Git e GitHub
- Linux (Ubuntu)

## Requisitos

- Linux (Ubuntu ou outra distribuição).
- Python 3.10 ou superior.
- pip (gerenciador de pacotes Python).
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

## Configuração dos limites

Ao iniciar o programa, o usuário pode escolher entre utilizar os limites padrão ou personalizar os valores de uso dos recursos.

Os limites podem ser configurados individualmente para:

- CPU.
- Memória RAM.
- Disco.

O valor padrão é de 80%, mas o usuário pode definir um limite entre 0 e 100%.

Quando o uso de um recurso ultrapassa o limite configurado, o programa identifica a situação como um alerta.

## Registro de alertas

O programa registra os alertas e as normalizações dos recursos no arquivo `alerta.log`.

Cada registro contém:

- Data e horário do evento.
- Recurso monitorado.
- Percentual de utilização.
- Situação identificada.

Exemplo:

```text
2026-11-05 08:35:24 - uso do disco elevado: 77.0%
2026-11-05 08:36:10 - Disco normalizado: 48.0%
```

O arquivo permite consultar o histórico de eventos identificados pelo monitor.

## Testes automatizados

O projeto utiliza a biblioteca `unittest`, nativa do Python, para verificar o funcionamento das funções.

Os testes verificam:

- Validação dos limites de utilização.
- Escolha entre limites padrão e personalizados.
- Identificação de uso elevado da CPU, memória RAM e disco.
- Identificação de situações normais dos recursos.
- Normalização da CPU.
- Registro de alertas em arquivo.

### Executar os testes

Com o ambiente virtual ativado, execute todos os testes automaticamente:

```bash
python -m unittest discover -v
```

Também é possível executar os testes de um arquivo específico:

```bash
python -m unittest -v test_funcoes.py
```

Os testes utilizam recursos de simulação (`unittest.mock`) para verificar comportamentos sem depender de entradas manuais ou modificar o arquivo de log real.
