#!/bin/bash
# ============================================================================
# Script para executar AMLDO (Projeto 1) E Projeto 2 SIMULTANEAMENTE
# ============================================================================
# Este script inicia os dois projetos em paralelo usando processos em background
#
# Uso: ./scripts/run_both.sh
#
# Para parar os projetos:
#   ./scripts/run_both.sh stop
# ============================================================================

set -e  # Exit on error

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Arquivo PID para controlar processos
PID_FILE="/tmp/amldo_both_projects.pid"

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║       EXECUTANDO PROJETOS 1 E 2 SIMULTANEAMENTE              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# ============================================================================
# Função para parar projetos
# ============================================================================
stop_projects() {
    echo -e "${YELLOW}⏹️  Parando projetos...${NC}"

    if [ -f "$PID_FILE" ]; then
        while IFS= read -r pid; do
            if ps -p "$pid" > /dev/null 2>&1; then
                echo -e "${BLUE}Parando processo PID: $pid${NC}"
                kill "$pid" 2>/dev/null || true
            fi
        done < "$PID_FILE"

        rm -f "$PID_FILE"
        echo -e "${GREEN}✅ Projetos parados${NC}"
    else
        echo -e "${YELLOW}⚠️  Nenhum processo em execução${NC}"
    fi

    # Também parar Docker Compose do AMLDO se estiver rodando
    if docker-compose -f /mnt/d/PYTHON/AMLDO/docker-compose.yml ps 2>/dev/null | grep -q "Up"; then
        echo -e "${BLUE}Parando Docker Compose do AMLDO...${NC}"
        cd /mnt/d/PYTHON/AMLDO
        docker-compose down
    fi

    exit 0
}

# Se argumento for "stop", parar projetos
if [ "$1" = "stop" ]; then
    stop_projects
fi

# ============================================================================
# Verificar se projetos já estão rodando
# ============================================================================
if [ -f "$PID_FILE" ]; then
    echo -e "${YELLOW}⚠️  Projetos parecem já estar rodando!${NC}"
    echo -e "${BLUE}Use './scripts/run_both.sh stop' para parar primeiro${NC}"
    exit 1
fi

# Limpar arquivo PID
> "$PID_FILE"

# ============================================================================
# Configuração dos Projetos
# ============================================================================

# Projeto 1 - AMLDO
PROJECT1_DIR="/mnt/d/PYTHON/AMLDO"
PROJECT1_NAME="AMLDO"
PROJECT1_PORT="8000"
PROJECT1_INTERFACE="api"  # Pode ser: api, streamlit, adk, all

# Projeto 2 - PERSONALIZE AQUI
PROJECT2_DIR="/mnt/d/PYTHON/SEU_PROJETO_AQUI"
PROJECT2_NAME="Projeto 2"
PROJECT2_PORT="5000"  # Ajuste a porta
PROJECT2_COMMAND="python main.py"  # Ajuste o comando

# ============================================================================
# Iniciar Projeto 1 (AMLDO)
# ============================================================================

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🚀 Iniciando Projeto 1: $PROJECT1_NAME${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

cd "$PROJECT1_DIR" || {
    echo -e "${RED}❌ Erro: Diretório $PROJECT1_DIR não encontrado${NC}"
    exit 1
}

# Verificar configuração AMLDO
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ AMLDO: .env não encontrado${NC}"
    echo -e "${BLUE}Execute: cp .env.example .env e configure GOOGLE_API_KEY${NC}"
    exit 1
fi

# Escolher como iniciar AMLDO
if [ "$PROJECT1_INTERFACE" = "all" ]; then
    # Docker Compose (em background)
    echo -e "${BLUE}Iniciando AMLDO via Docker Compose...${NC}"
    docker-compose up -d

    echo -e "${GREEN}✓ AMLDO iniciado via Docker${NC}"
    echo -e "${BLUE}  API: http://localhost:8000${NC}"
    echo -e "${BLUE}  Streamlit: http://localhost:8501${NC}"
    echo -e "${BLUE}  ADK: http://localhost:8080${NC}"

else
    # Python direto (em background)
    echo -e "${BLUE}Iniciando AMLDO ($PROJECT1_INTERFACE)...${NC}"

    if [ -d "venv" ]; then
        source venv/bin/activate
    fi

    case "$PROJECT1_INTERFACE" in
        api)
            nohup amldo-api > /tmp/amldo_api.log 2>&1 &
            echo $! >> "$PID_FILE"
            echo -e "${GREEN}✓ AMLDO API iniciada (PID: $!)${NC}"
            echo -e "${BLUE}  URL: http://localhost:$PROJECT1_PORT${NC}"
            echo -e "${BLUE}  Logs: tail -f /tmp/amldo_api.log${NC}"
            ;;
        streamlit)
            nohup streamlit run src/amldo/interfaces/streamlit/app.py > /tmp/amldo_streamlit.log 2>&1 &
            echo $! >> "$PID_FILE"
            echo -e "${GREEN}✓ AMLDO Streamlit iniciado (PID: $!)${NC}"
            echo -e "${BLUE}  URL: http://localhost:8501${NC}"
            echo -e "${BLUE}  Logs: tail -f /tmp/amldo_streamlit.log${NC}"
            ;;
        adk)
            nohup adk web > /tmp/amldo_adk.log 2>&1 &
            echo $! >> "$PID_FILE"
            echo -e "${GREEN}✓ AMLDO ADK iniciado (PID: $!)${NC}"
            echo -e "${BLUE}  URL: http://localhost:8080${NC}"
            echo -e "${BLUE}  Logs: tail -f /tmp/amldo_adk.log${NC}"
            ;;
    esac
fi

sleep 2
echo ""

# ============================================================================
# Iniciar Projeto 2
# ============================================================================

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🚀 Iniciando Projeto 2: $PROJECT2_NAME${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

cd "$PROJECT2_DIR" || {
    echo -e "${YELLOW}⚠️  AVISO: Diretório $PROJECT2_DIR não encontrado${NC}"
    echo -e "${YELLOW}⚠️  Configure PROJECT2_DIR no script${NC}"
    echo -e "${BLUE}Apenas Projeto 1 (AMLDO) foi iniciado${NC}"
    echo ""
    echo -e "${CYAN}Para parar: ./scripts/run_both.sh stop${NC}"
    exit 0
}

# Verificar .env se existir
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Projeto 2: .env não encontrado${NC}"
    cp .env.example .env 2>/dev/null || true
fi

# Ativar venv se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Iniciar Projeto 2 em background
echo -e "${BLUE}Iniciando $PROJECT2_NAME...${NC}"
nohup $PROJECT2_COMMAND > /tmp/projeto2.log 2>&1 &
PROJECT2_PID=$!
echo $PROJECT2_PID >> "$PID_FILE"

echo -e "${GREEN}✓ $PROJECT2_NAME iniciado (PID: $PROJECT2_PID)${NC}"
echo -e "${BLUE}  URL: http://localhost:$PROJECT2_PORT${NC}"
echo -e "${BLUE}  Logs: tail -f /tmp/projeto2.log${NC}"

sleep 2
echo ""

# ============================================================================
# Resumo Final
# ============================================================================

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                               ║${NC}"
echo -e "${CYAN}║               ✅ AMBOS OS PROJETOS INICIADOS                  ║${NC}"
echo -e "${CYAN}║                                                               ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}📊 Status dos Projetos:${NC}"
echo ""

echo -e "${BLUE}Projeto 1 - $PROJECT1_NAME:${NC}"
if [ "$PROJECT1_INTERFACE" = "all" ]; then
    echo -e "  • API:       http://localhost:8000"
    echo -e "  • Docs:      http://localhost:8000/docs"
    echo -e "  • Streamlit: http://localhost:8501"
    echo -e "  • ADK:       http://localhost:8080"
    echo -e "  • Status:    ${GREEN}docker-compose ps${NC}"
else
    echo -e "  • URL:       http://localhost:$PROJECT1_PORT"
fi
echo ""

echo -e "${BLUE}Projeto 2 - $PROJECT2_NAME:${NC}"
echo -e "  • URL:       http://localhost:$PROJECT2_PORT"
echo -e "  • Logs:      tail -f /tmp/projeto2.log"
echo ""

echo -e "${YELLOW}📝 Comandos úteis:${NC}"
echo -e "  • Ver logs projeto 1:  ${CYAN}tail -f /tmp/amldo_*.log${NC}"
echo -e "  • Ver logs projeto 2:  ${CYAN}tail -f /tmp/projeto2.log${NC}"
echo -e "  • Parar tudo:          ${CYAN}./scripts/run_both.sh stop${NC}"
echo -e "  • Status Docker:       ${CYAN}docker-compose ps${NC}"
echo ""

echo -e "${GREEN}✨ Tudo pronto! Bom trabalho!${NC}"
