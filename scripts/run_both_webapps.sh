#!/bin/bash
# ============================================================================
# Script para executar AMBAS WEBAPPS SIMULTANEAMENTE
# ============================================================================
# Projeto 1 (Antigo): AMLDO_W/AMLDO/webapp → Porta 8001
# Projeto 2 (Novo):   src/amldo/            → Porta 8000
# ============================================================================

set -e  # Exit on error

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# Arquivo PID
PID_FILE="/tmp/amldo_webapps.pid"

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         EXECUTANDO AMBAS WEBAPPS SIMULTANEAMENTE             ║
║                                                               ║
║  Webapp Antiga (8001) + Webapp Nova v0.3.0 (8000)           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# ============================================================================
# Função para parar projetos
# ============================================================================
stop_webapps() {
    echo -e "${YELLOW}⏹️  Parando webapps...${NC}"

    if [ -f "$PID_FILE" ]; then
        while IFS= read -r pid; do
            if ps -p "$pid" > /dev/null 2>&1; then
                echo -e "${BLUE}Parando processo PID: $pid${NC}"
                kill "$pid" 2>/dev/null || true
            fi
        done < "$PID_FILE"

        rm -f "$PID_FILE"
        echo -e "${GREEN}✅ Webapps paradas${NC}"
    else
        echo -e "${YELLOW}⚠️  Nenhum processo em execução${NC}"
    fi

    exit 0
}

# Se argumento for "stop", parar projetos
if [ "$1" = "stop" ]; then
    stop_webapps
fi

# ============================================================================
# Verificar se já está rodando
# ============================================================================
if [ -f "$PID_FILE" ]; then
    echo -e "${YELLOW}⚠️  Webapps parecem já estar rodando!${NC}"
    echo -e "${BLUE}Use './scripts/run_both_webapps.sh stop' para parar primeiro${NC}"
    exit 1
fi

# Limpar arquivo PID
> "$PID_FILE"

# Diretórios
PROJECT_ROOT="/mnt/d/PYTHON/AMLDO"
WEBAPP_OLD_DIR="$PROJECT_ROOT/AMLDO_W/AMLDO"
WEBAPP_NEW_DIR="$PROJECT_ROOT"

# ============================================================================
# Verificar configurações
# ============================================================================

echo -e "${BLUE}🔍 Verificando configurações...${NC}"
echo ""

# Verificar webapp antiga
if [ ! -d "$WEBAPP_OLD_DIR" ]; then
    echo -e "${RED}❌ WebApp antiga não encontrada em $WEBAPP_OLD_DIR${NC}"
    exit 1
fi

if [ ! -f "$WEBAPP_OLD_DIR/.env" ]; then
    echo -e "${YELLOW}⚠️  WebApp antiga: .env não encontrado${NC}"
    echo -e "${BLUE}Crie $WEBAPP_OLD_DIR/.env${NC}"
    exit 1
fi

# Verificar webapp nova
if [ ! -f "$WEBAPP_NEW_DIR/.env" ]; then
    echo -e "${RED}❌ WebApp nova: .env não encontrado${NC}"
    echo -e "${BLUE}Execute: cp .env.example .env e configure GOOGLE_API_KEY${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Configurações OK${NC}"
echo ""

# Ativar venv (compartilhado)
if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
    echo -e "${GREEN}✓ Virtual environment ativado${NC}"
fi

# ============================================================================
# Iniciar WebApp ANTIGA (Porta 8001)
# ============================================================================

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🚀 Iniciando WebApp ANTIGA (Original)${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

cd "$WEBAPP_OLD_DIR" || exit 1

# Instalar dependências se necessário
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}Instalando dependências da webapp antiga...${NC}"
    pip install -q -r requirements.txt
fi

echo -e "${BLUE}Iniciando webapp antiga em background...${NC}"
cd webapp
nohup uvicorn main:app --reload --port 8001 --host 0.0.0.0 > /tmp/webapp_old.log 2>&1 &
WEBAPP_OLD_PID=$!
echo $WEBAPP_OLD_PID >> "$PID_FILE"

echo -e "${GREEN}✓ WebApp Antiga iniciada (PID: $WEBAPP_OLD_PID)${NC}"
echo -e "${BLUE}  URL: http://localhost:8001${NC}"
echo -e "${BLUE}  Logs: tail -f /tmp/webapp_old.log${NC}"

sleep 3
echo ""

# ============================================================================
# Iniciar WebApp NOVA (Porta 8000)
# ============================================================================

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🚀 Iniciando WebApp NOVA (v0.3.0)${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

cd "$WEBAPP_NEW_DIR" || exit 1

echo -e "${BLUE}Iniciando webapp nova em background...${NC}"
nohup amldo-api > /tmp/webapp_new.log 2>&1 &
WEBAPP_NEW_PID=$!
echo $WEBAPP_NEW_PID >> "$PID_FILE"

echo -e "${GREEN}✓ WebApp Nova iniciada (PID: $WEBAPP_NEW_PID)${NC}"
echo -e "${BLUE}  URL: http://localhost:8000${NC}"
echo -e "${BLUE}  Docs: http://localhost:8000/docs${NC}"
echo -e "${BLUE}  Interface: http://localhost:8000/consulta${NC}"
echo -e "${BLUE}  Logs: tail -f /tmp/webapp_new.log${NC}"

sleep 3
echo ""

# ============================================================================
# Resumo Final
# ============================================================================

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                               ║${NC}"
echo -e "${CYAN}║              ✅ AMBAS WEBAPPS INICIADAS                       ║${NC}"
echo -e "${CYAN}║                                                               ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}📊 Status das WebApps:${NC}"
echo ""

echo -e "${BLUE}WebApp ANTIGA (Original):${NC}"
echo -e "  • URL:      http://localhost:8001"
echo -e "  • Logs:     tail -f /tmp/webapp_old.log"
echo -e "  • Código:   AMLDO_W/AMLDO/webapp/"
echo ""

echo -e "${BLUE}WebApp NOVA (v0.3.0):${NC}"
echo -e "  • URL:      http://localhost:8000"
echo -e "  • Docs:     http://localhost:8000/docs"
echo -e "  • Chat:     http://localhost:8000/consulta"
echo -e "  • Processo: http://localhost:8000/processamento"
echo -e "  • Métricas: http://localhost:8000/metricas"
echo -e "  • Logs:     tail -f /tmp/webapp_new.log"
echo -e "  • Código:   src/amldo/interfaces/api/"
echo ""

echo -e "${YELLOW}📝 Comandos úteis:${NC}"
echo -e "  • Ver logs antiga:  ${CYAN}tail -f /tmp/webapp_old.log${NC}"
echo -e "  • Ver logs nova:    ${CYAN}tail -f /tmp/webapp_new.log${NC}"
echo -e "  • Parar ambas:      ${CYAN}./scripts/run_both_webapps.sh stop${NC}"
echo ""

echo -e "${YELLOW}🔍 Diferenças entre as webapps:${NC}"
echo -e "  • Antiga: Webapp original simples (FastAPI básico)"
echo -e "  • Nova:   Sistema completo v0.3.0 (RAG v1/v2/v3, Métricas, UI)"
echo ""

echo -e "${GREEN}✨ Tudo pronto! Compare as duas versões!${NC}"
