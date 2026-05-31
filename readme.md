# Junior Automation Dev Assignment

Automação para conciliação de cobranças médicas, processamento de laudos PDF, geração de relatório Excel e envio automático por e-mail.

## Visão Geral

O projeto consolida dados de faturamento a partir de uma planilha Excel interna, um arquivo CSV do convênio e laudos médicos em PDF.

O pipeline executa as seguintes etapas:

- Leitura dos arquivos de entrada
- Normalização de nomes, valores e registros ANS
- Consolidação das cobranças entre Excel e CSV
- Identificação de divergências de faturamento
- Extração de informações dos PDFs
- Associação segura dos laudos aos registros de cobrança
- Renomeação automática dos PDFs aprovados
- Validação dos PDFs renomeados
- Geração de relatório Excel consolidado
- Envio automático do relatório por e-mail
- Registro de logs da execução

## Tecnologias Utilizadas

- Python 3.12+
- pandas
- openpyxl
- RapidFuzz
- Unidecode
- pypdf
- python-dotenv
- Shell Script

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
└── email_sender.py

output/
├── laudos_renomeados/
└── relatorios/

logs/
run_pipeline.sh
requirements.txt
.env.example
```

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

No Windows, caso o comando `python` não esteja configurado, use:

```bash
py -m pip install -r requirements.txt
```

## Configuração do E-mail

Crie um arquivo `.env` a partir do `.env.example`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=sua_app_password

EMAIL_FROM=seu_email@gmail.com
EMAIL_TO=destinatario@email.com
```

Para testes, pode ser usado Gmail com App Password ou um serviço como Mailtrap.

## Execução Manual

Execute o pipeline diretamente:

```bash
py src/main.py
```

Ou pelo script de automação:

```bash
bash run_pipeline.sh
```

## Execução Automatizada

O agendamento solicitado no desafio está documentado no topo do arquivo `run_pipeline.sh`.

Exemplo de cron para executar toda segunda-feira às 06:30:

```cron
30 6 * * 1 /caminho/do/projeto/run_pipeline.sh
```

No Windows, o mesmo fluxo pode ser configurado no Agendador de Tarefas usando:

```text
Programa: C:\Windows\System32\bash.exe
Argumentos: run_pipeline.sh
Iniciar em: D:\junior-automation-dev-assignment
Frequência: semanal, segunda-feira, 06:30
```

## Arquivos Gerados

### PDFs Renomeados

Os PDFs aprovados são copiados para:

```text
output/laudos_renomeados/
```

Formato do nome:

```text
CPF-PACIENTE-COBRANCA-MMAAAA.pdf
```

Exemplo:

```text
34567890122-ANALIMA-COB029-112024.pdf
```

### Relatório Excel

O relatório é gerado em:

```text
output/relatorios/
```

Ele contém três abas:

- `Resumo`: indicadores gerais do processamento
- `Detalhamento`: registros consolidados com dados do Excel e CSV
- `Alertas`: registros com divergências ou inconsistências

## Estratégia de Associação dos PDFs

O sistema prioriza associações seguras:

1. Extrai o número da guia do PDF.
2. Busca a guia nos registros consolidados.
3. Extrai o nome do paciente do PDF.
4. Compara o paciente do PDF com o paciente do registro usando similaridade textual.
5. Aprova automaticamente apenas casos com confiança suficiente.
6. Encaminha divergências para revisão manual.

Essa abordagem reduz o risco de associar um laudo ao paciente errado.

## Resultado do Processamento

Com os arquivos fornecidos no desafio, o pipeline processou:

- 324 PDFs
- 165 PDFs renomeados automaticamente
- 138 PDFs enviados para revisão manual
- 3 alertas de validação nos PDFs renomeados

Os alertas de validação são registrados no log para análise posterior.

## Melhorias Futuras

- Gerar um arquivo CSV com os casos de revisão manual
- Adicionar testes automatizados
- Criar pipeline de CI com GitHub Actions
- Persistir histórico em PostgreSQL
- Adicionar suporte a arquivos XML
- Melhorar monitoramento e alertas operacionais
