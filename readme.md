# Junior Automation Dev Assignment

## Visão Geral

Este projeto automatiza o processo de conciliação de cobranças médicas a partir de dados provenientes de planilhas Excel, arquivos CSV e laudos em PDF.

O pipeline realiza:

* Consolidação de dados de múltiplas fontes
* Normalização de informações
* Identificação de divergências
* Associação de laudos aos registros de cobrança
* Renomeação automática de PDFs
* Geração de relatório Excel consolidado
* Envio do relatório por e-mail
* Execução automatizada via script

---

## Funcionalidades

* Leitura de cobranças a partir de Excel e CSV
* Normalização de nomes, datas, convênios e valores
* Consolidação de registros entre fontes
* Detecção de divergências de faturamento
* Extração de informações dos laudos PDF
* Associação de laudos aos registros de cobrança
* Renomeação automática de PDFs validados
* Geração de relatório Excel com resumo, detalhamento e alertas
* Validação dos PDFs processados
* Envio automático do relatório por e-mail

---

## Tecnologias Utilizadas

* Python 3.12+
* Pandas
* OpenPyXL
* RapidFuzz
* Unidecode
* PyPDF2
* Python Dotenv

---

## Estrutura do Projeto

```text
data/
├── cobrancas_internas.xlsx
├── cobrancas_convenio.csv
└── laudos/

src/
├── main.py
├── consolidator.py
├── normalizer.py
├── pdf_renamer.py
├── report_generator.py
├── email_sender.py
└── ...

output/
├── laudos_renomeados/
├── relatorios/
└── logs/
```

---

## Instalação

Clone o repositório:

```bash
git clone <url-do-repositorio>
cd junior-automation-dev-assignment
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Configuração

Crie um arquivo `.env` a partir do `.env.example`.

Exemplo:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=sua_app_password

EMAIL_FROM=seu_email@gmail.com
EMAIL_TO=destinatario@email.com
```

Para testes, pode ser utilizado:

* Gmail com App Password
* Mailtrap

---

## Execução

Executar o pipeline manualmente:

```bash
py src/main.py
```

---

## Execução Automatizada

Executar o pipeline completo:

```bash
bash run_pipeline.sh
```

O script registra logs e retorna código de erro em caso de falha.

O comando cron para execução automática está documentado dentro do próprio script.

---

## Arquivos Gerados

### PDFs Renomeados

Diretório:

```text
output/laudos_renomeados/
```

Formato:

```text
CPF-PACIENTE-COBRANCA-MMAAAA.pdf
```

Exemplo:

```text
34567890122-ANALIMA-COB029-112024.pdf
```

### Relatório Excel

Diretório:

```text
output/relatorios/
```

O relatório contém três abas:

#### Resumo

* Total de cobranças consolidadas
* Registros presentes em ambas as fontes
* Registros exclusivos por fonte
* Valor líquido total
* Total de glosas
* PDFs processados
* PDFs renomeados
* PDFs enviados para revisão manual

#### Detalhamento

Contém todos os registros consolidados com informações enriquecidas, incluindo:

* CPF
* Convênio
* Procedimento
* Datas
* Valores
* Divergências identificadas

#### Alertas

Contém apenas registros que apresentaram inconsistências:

* Divergência de valor
* Divergência de nome
* Divergência de convênio
* Registro presente em apenas uma fonte

