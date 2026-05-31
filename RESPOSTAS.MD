# RESPOSTAS.md

## Parte 1 — Sobre o que foi construído

### 1.1

O pipeline consolida informações de cobranças médicas vindas de uma planilha Excel interna e de um arquivo CSV do convênio. Depois da consolidação, ele identifica divergências, relaciona laudos em PDF às cobranças correspondentes, renomeia os PDFs aprovados, gera um relatório Excel com os resultados e envia esse relatório por e-mail. Também registra logs da execução e possui um script Bash preparado para automação.

### 1.2

A etapa mais difícil foi associar os PDFs aos registros corretos de cobrança. Como os arquivos possuem nomes variados e os PDFs podem conter informações divergentes, a solução prioriza o número da guia extraído do PDF e valida o paciente antes de renomear o arquivo automaticamente. Casos com inconsistência são enviados para revisão manual.

### 1.3

**Quando o valor diverge entre as fontes, qual prevalece?**

Utilizei o valor líquido do CSV do convênio como referência principal para os indicadores financeiros do relatório, pois ele representa o valor efetivamente processado pelo convênio. A divergência continua registrada para análise.

**Cobrança presente apenas no CSV**

A cobrança é mantida na consolidação e sinalizada como `FONTE_UNICA_CSV`, pois pode indicar uma cobrança processada pelo convênio que não está registrada internamente.

**Como identifiquei pacientes com grafias diferentes**

Utilizei normalização dos nomes, removendo acentos, padronizando maiúsculas e tratando espaços. Na validação dos PDFs, também uso similaridade textual para comparar o paciente extraído do PDF com o paciente do registro consolidado.

### 1.4

Primeiro extraio informações dos PDFs, principalmente número da guia e paciente. Em seguida, busco a guia nos registros consolidados e comparo o paciente do PDF com o paciente associado à cobrança. O maior risco era associar um PDF ao paciente errado, então a automação só aprova casos com confiança suficiente e envia divergências para revisão manual.

### 1.5

Chamou atenção a quantidade de pequenas diferenças entre fontes e PDFs: nomes com variações, abreviações, guias divergentes e dados incompletos. A solução trata esses casos com validações adicionais e logs para auditoria.

---

## Parte 2 — Sobre as decisões técnicas

### 2.1

Escolhi Python por ser uma linguagem adequada para automação e processamento de dados. Usei pandas para consolidação, openpyxl para geração do Excel, pypdf para leitura dos PDFs, RapidFuzz para similaridade textual, Unidecode para normalização de nomes e python-dotenv para variáveis de ambiente.

### 2.2

Separei o projeto por responsabilidade:

- `consolidator.py`: leitura e consolidação dos dados
- `normalizer.py`: normalização de campos
- `pdf_renamer.py`: extração, validação e renomeação dos PDFs
- `report_generator.py`: geração do relatório Excel
- `email_sender.py`: envio do relatório por e-mail
- `main.py`: orquestração do pipeline
- `run_pipeline.sh`: execução automatizada e registro de logs

Essa estrutura facilita manutenção e evolução.

### 2.3

**Excel com coluna faltando**

O pipeline falha durante o processamento, evitando gerar um resultado incorreto com dados incompletos.

**CSV com valor inválido**

Os valores passam por normalização. Entradas inválidas são convertidas de forma defensiva ou aparecem como inconsistência no processamento.

**PDF com guia ou paciente divergente**

O PDF não é renomeado automaticamente. O caso é registrado no log como revisão manual.

**Execução repetida**

O pipeline evita duplicar PDFs renomeados. Quando o arquivo de destino já existe, registra `ARQUIVO_JA_EXISTE` e segue o processamento.

### 2.4

Em produção, eu adicionaria testes automatizados, validações mais robustas de entrada, persistência dos resultados em banco de dados, monitoramento centralizado de logs e métricas operacionais.

### 2.5

A lógica de associação dos PDFs ainda pode evoluir. Com mais tempo, eu criaria um sistema de pontuação com múltiplos critérios, como guia, paciente, CPF, procedimento e data, para aumentar a taxa de automação sem comprometer a segurança.

---

## Parte 3 — Visão de evolução

### 3.1

Eu utilizaria um orquestrador como Apache Airflow ou uma solução baseada no Agendador de Tarefas/cron com monitoramento externo. Isso permitiria histórico de execuções, reprocessamento, alertas automáticos e acompanhamento do pipeline.

### 3.2

Para adicionar XML, criaria um módulo específico de leitura e normalização, integrando os dados ao consolidado por identificadores como guia, CPF, procedimento ou data. O relatório passaria a incluir status da cobrança, motivo de glosa e indicadores adicionais.

### 3.3

Eu estruturaria uma aplicação com backend em Python, banco PostgreSQL para histórico dos processamentos e uma interface de consulta por período, convênio e tipo de alerta. Isso reduziria a dependência de relatórios enviados por e-mail.

### 3.4

Monitoraria:

- Falhas de execução
- Quantidade de PDFs sem associação
- Quantidade de divergências
- Falhas no envio de e-mail
- Tempo de execução

Notificaria imediatamente:

- Falha total do pipeline
- Falha no envio do relatório
- Ausência de arquivos esperados
- Aumento anormal de divergências

Não notificaria pequenas variações normais na quantidade de registros processados.

---

## Parte 4 — Uso de agentes de IA

### 4.1

Sim. Utilizei IA como apoio para discutir abordagens, revisar trechos de código, identificar problemas e validar melhorias. As decisões de arquitetura, implementação, testes, validação dos resultados e ajustes finais foram conduzidas manualmente. O agente também ajudou a verificar o funcionamento do agendamento e a revisar pontos de qualidade do projeto.

---

## Parte 5 — Contexto pessoal

### 5.1

Sim. Um exemplo foi o projeto Clean Beach, desenvolvido durante a graduação. O sistema integra diferentes fontes de dados relacionadas às praias e automatiza processos de consulta, armazenamento e exibição das informações para os usuários. Também desenvolvi funcionalidades de sincronização com banco de dados, autenticação e processamento de dados para reduzir atividades manuais.

### 5.2

Com mais tempo, eu investiria em testes automatizados, melhoria do algoritmo de associação dos PDFs, tratamento mais robusto de exceções, monitoramento detalhado e documentação adicional.

### 5.3

A parte mais ambígua foi definir as regras de reconciliação quando havia divergências entre as fontes e o grau de confiança necessário para associar PDFs às cobranças. Optei por priorizar segurança e rastreabilidade, registrando divergências e enviando casos duvidosos para revisão manual.
