#!/bin/bash
# ============================================================================
# Script para executar WEBAPP ANTIGA (AMLDO_W/AMLDO/webapp)
# ============================================================================
# Este é o projeto FastAPI original/antigo
# Localizado em: AMLDO_W/AMLDO/webapp/main.py
# ============================================================================

set -e  # Exit on error

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════╗
║                                       ║
║    AMLDO WebApp ANTIGA (Original)    ║
║      AMLDO_W/AMLDO/webapp            ║
║                                       ║
╚═══════════════════════════════════════╝
EOF
echo -e "${NC}"

# Diretórios
PROJECT_ROOT="/mnt/d/PYTHON/AMLDO"
WEBAPP_DIR="$PROJECT_ROOT/AMLDO_W/AMLDO"

echo -e "${BLUE}📂 Projeto: AMLDO WebApp Antiga${NC}"
echo -e "${BLUE}📂 Diretório: $WEBAPP_DIR${NC}"
echo ""

# Mudar para diretório do webapp antigo
cd "$WEBAPP_DIR" || {
    echo -e "${RED}❌ Erro: Diretório $WEBAPP_DIR não encontrado${NC}"
    exit 1
}

# Verificar .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env não encontrado em $WEBAPP_DIR${NC}"
    echo -e "${BLUE}Crie um arquivo .env com as configurações necessárias${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Configuração OK${NC}"
echo ""

# Verificar se virtual env existe (do projeto novo pode ser usado)
if [ -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${BLUE}Ativando virtual environment...${NC}"
    source "$PROJECT_ROOT/venv/bin/activate"
    echo -e "${GREEN}✓ venv ativado${NC}"
fi

# Verificar dependências
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}Verificando dependências...${NC}"
    pip install -q -r requirements.txt
fi

echo ""
echo -e "${GREEN}🚀 Iniciando WebApp Antiga...${NC}"
echo -e "${BLUE}URL: http://localhost:8001${NC}"
echo -e "${BLUE}Diretório: $WEBAPP_DIR${NC}"
echo ""

# Executar webapp antiga na porta 8001 (para não conflitar com a nova API)
cd webapp
uvicorn main:app --reload --port 8001 --host 0.0.0.0
