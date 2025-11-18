#!/bin/bash
# Script para executar todas as aplicações simultaneamente
# FastAPI (8000) + Streamlit (8501) + Google ADK (8080)

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🚀 Iniciando TODAS as aplicações AMLDO${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Verificar se está no diretório correto
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Erro: Execute este script do diretório raiz do projeto${NC}"
    exit 1
fi

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Erro: Virtual environment não encontrado${NC}"
    echo "Execute: python3.11 -m venv venv && source venv/bin/activate && pip install -e .[adk,streamlit,dev]"
    exit 1
fi

# Ativar virtual environment
echo -e "${BLUE}📦 Ativando virtual environment...${NC}"
source venv/bin/activate

# Verificar se o pacote está instalado
if ! python -c "import amldo" 2>/dev/null; then
    echo -e "${RED}❌ Erro: Pacote 'amldo' não instalado${NC}"
    echo "Execute: pip install -e .[adk,streamlit,dev]"
    exit 1
fi

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo -e "${RED}⚠️  Aviso: Arquivo .env não encontrado${NC}"
    echo "Crie um arquivo .env baseado em .env.example"
    echo ""
fi

# Carregar .env se existir
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Array para armazenar PIDs dos processos
declare -a PIDS

# Função para cleanup quando script for terminado
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Encerrando todas as aplicações...${NC}"
    for pid in "${PIDS[@]}"; do
        if kill -0 $pid 2>/dev/null; then
            kill $pid 2>/dev/null || true
        fi
    done
    echo -e "${GREEN}✅ Todas as aplicações foram encerradas${NC}"
    exit 0
}

# Configurar trap para capturar Ctrl+C
trap cleanup SIGINT SIGTERM

echo -e "${GREEN}🚀 Iniciando aplicações em background...${NC}"
echo ""

# Criar diretório para logs
mkdir -p logs

# 1. Iniciar FastAPI REST API (porta 8000)
echo -e "${BLUE}[1/3]${NC} Iniciando FastAPI REST API..."
export API_HOST=127.0.0.1
export API_PORT=8000
nohup amldo-api > logs/api.log 2>&1 &
API_PID=$!
PIDS+=($API_PID)
echo -e "${GREEN}      ✅ FastAPI iniciada (PID: $API_PID)${NC}"
sleep 2

# 2. Iniciar Streamlit (porta 8501)
echo -e "${BLUE}[2/3]${NC} Iniciando Streamlit Web App..."
export STREAMLIT_PORT=8501
nohup streamlit run src/amldo/interfaces/streamlit/app.py --server.port=${STREAMLIT_PORT} --server.headless=true > logs/streamlit.log 2>&1 &
STREAMLIT_PID=$!
PIDS+=($STREAMLIT_PID)
echo -e "${GREEN}      ✅ Streamlit iniciado (PID: $STREAMLIT_PID)${NC}"
sleep 2

# 3. Iniciar Google ADK (porta 8080)
echo -e "${BLUE}[3/3]${NC} Iniciando Google ADK Interface..."
nohup adk web > logs/adk.log 2>&1 &
ADK_PID=$!
PIDS+=($ADK_PID)
echo -e "${GREEN}      ✅ Google ADK iniciado (PID: $ADK_PID)${NC}"
sleep 2

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Todas as aplicações foram iniciadas com sucesso!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}📊 Interfaces disponíveis:${NC}"
echo ""
echo -e "${BLUE}🔹 FastAPI REST API:${NC}"
echo -e "   Interface Web: http://127.0.0.1:8000"
echo -e "   Swagger Docs:  http://127.0.0.1:8000/docs"
echo -e "   ReDoc:         http://127.0.0.1:8000/redoc"
echo -e "   Health Check:  http://127.0.0.1:8000/health"
echo ""
echo -e "${BLUE}🔹 Streamlit Web App:${NC}"
echo -e "   Interface:     http://localhost:8501"
echo ""
echo -e "${BLUE}🔹 Google ADK:${NC}"
echo -e "   Interface:     http://localhost:8080"
echo ""
echo -e "${YELLOW}📝 Logs disponíveis em:${NC}"
echo -e "   FastAPI:    logs/api.log"
echo -e "   Streamlit:  logs/streamlit.log"
echo -e "   Google ADK: logs/adk.log"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Pressione Ctrl+C para parar todas as aplicações${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Aguardar indefinidamente (até Ctrl+C)
while true; do
    # Verificar se todos os processos ainda estão rodando
    for pid in "${PIDS[@]}"; do
        if ! kill -0 $pid 2>/dev/null; then
            echo -e "${RED}⚠️  Processo $pid terminou inesperadamente${NC}"
            cleanup
        fi
    done
    sleep 5
done
