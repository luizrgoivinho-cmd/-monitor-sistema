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
- unittest
- Git e GitHub
- Linux (Ubuntu)

## Estrutura do projeto

O projeto foi organizado em módulos para separar as responsabilidades e facilitar a manutenção do código.

| Arquivo | Responsabilidade |
|---|---|
| `monitor.py` | Executa o monitoramento e coordena os módulos. |
| `coleta.py` | Realiza a coleta dos dados de CPU, memória RAM e disco. |
| `funcoes.py` | Contém as funções de validação, identificação de alertas e registro de eventos. |
| `test_coleta.py` | Contém os testes automatizados das funções de coleta. |
| `test_funcoes.py` | Contém os testes automatizados das demais funções. |
| `requirements.txt` | Lista as dependências do projeto. |

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

Instale as dependências:

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

Atualmente, o projeto possui 23 testes automatizados, que verificam:

- Validação dos limites de utilização.
- Escolha entre limites padrão e personalizados.
- Identificação de uso elevado da CPU, memória RAM e disco.
- Identificação de situações normais dos recursos.
- Normalização da CPU.
- Controle de alertas repetidos e normalizações.
- Registro de alertas em arquivo.
- Coleta de dados da CPU, memória RAM e disco.

Os testes de coleta utilizam `unittest.mock` para simular as chamadas da biblioteca `psutil`, permitindo verificar o comportamento das funções sem depender dos valores reais do computador.

### Executar todos os testes

Com o ambiente virtual ativado, execute:

```bash
python -m unittest discover -v
```

### Executar os testes de um módulo específico

Testes das funções:

```bash
python -m unittest -v test_funcoes.py
```

Testes da coleta:

```bash
python -m unittest -v test_coleta.py
```
