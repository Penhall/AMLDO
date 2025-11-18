#!/bin/bash
# ============================================================================
# Script para ATIVAR o Virtual Environment do AMLDO
# ============================================================================
# Uso: source activate_venv.sh
#      OU
#      . activate_venv.sh
# ============================================================================

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🐍 Ativando Virtual Environment...${NC}"

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment não encontrado!${NC}"
    echo -e "${BLUE}Criando novo virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment criado${NC}"
fi

# Ativar venv
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment ativado!${NC}"
    echo -e "${BLUE}Python: $(which python)${NC}"
    echo -e "${BLUE}Versão: $(python --version)${NC}"
    echo ""
    echo -e "${GREEN}Para desativar: ${NC}deactivate"
else
    echo -e "${RED}❌ Erro: venv/bin/activate não encontrado${NC}"
    exit 1
fi
