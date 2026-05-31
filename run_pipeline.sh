#!/bin/bash

# Agendamento solicitado no desafio:
# Executar toda segunda-feira as 06:30.
#
# Exemplo no cron Linux:
# 30 6 * * 1 /caminho/do/projeto/run_pipeline.sh
#
# Exemplo no Agendador de Tarefas do Windows:
# Programa: C:\Windows\System32\bash.exe
# Argumentos: D:\junior-automation-dev-assignment\run_pipeline.sh
# Iniciar em: D:\junior-automation-dev-assignment
# Frequencia: semanal, segunda-feira, 06:30

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_DIR="logs"
LOG_FILE="$LOG_DIR/pipeline_$TIMESTAMP.log"

mkdir -p "$LOG_DIR"

echo "[$(date)] Iniciando pipeline..." >> "$LOG_FILE"

PYTHON_CMD="py.exe"

if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
    PYTHON_CMD="python.exe"
fi

PYTHONUTF8=1 PYTHONIOENCODING=utf-8 "$PYTHON_CMD" -X utf8 src/main.py >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "[$(date)] Pipeline finalizado com erro." >> "$LOG_FILE"
    exit 1
fi

echo "[$(date)] Pipeline finalizado com sucesso." >> "$LOG_FILE"
exit 0
