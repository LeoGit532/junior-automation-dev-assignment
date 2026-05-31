#!/bin/bash

# Cron para executar toda segunda-feira às 06h30:
# 30 6 * * 1 /caminho/do/projeto/run_pipeline.sh

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_DIR="logs"
LOG_FILE="$LOG_DIR/pipeline_$TIMESTAMP.log"

mkdir -p "$LOG_DIR"

echo "[$(date)] Iniciando pipeline..." >> "$LOG_FILE"

PYTHONIOENCODING=utf-8 py src/main.py >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "[$(date)] Pipeline finalizado com erro." >> "$LOG_FILE"
    exit 1
fi

echo "[$(date)] Pipeline finalizado com sucesso." >> "$LOG_FILE"
exit 0