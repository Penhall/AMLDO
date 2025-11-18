#!/bin/bash
# ============================================================================
# Script para executar WEBAPP NOVA (src/amldo v0.3.0)
# ============================================================================
# Este é o projeto moderno v0.3.0
# Localizado em: src/amldo/interfaces/api/
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
    ___    __  _____    ____  ____
   /   |  /  |/  / /   / __ \/ __ \
  / /| | / /|_/ / /   / / / / / / /
 / ___ |/ /  / / /___/ /_/ / /_/ /
/_/  |_/_/  /_/_____/_____/\____/

AMLDO v0.3.0 - WebApp NOVA
src/amldo/interfaces/api/
EOF
echo -e "${NC}"

# Diretório
PROJECT_DIR="/mnt/d/PYTHON/AMLDO"

echo -e "${BLUE}📂 Projeto: AMLDO v0.3.0 (Novo)${NC}"
echo -e "${BLUE}📂 Diretório: $PROJECT_DIR${NC}"
echo ""

cd "$PROJECT_DIR" || {
    echo -e "${RED}❌ Erro: Diretório $PROJECT_DIR não encontrado${NC}"
    exit 1
}

# Verificar .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env não encontrado!${NC}"
    echo -e "${BLUE}Criando .env a partir de .env.example...${NC}"
    cp .env.example .env
    echo -e "${RED}⚠️  IMPORTANTE: Configure GOOGLE_API_KEY no arquivo .env${NC}"
    exit 1
fi

# Verificar GOOGLE_API_KEY
if grep -q "GOOGLE_API_KEY=sua_chave_aqui" .env || ! grep -q "GOOGLE_API_KEY=" .env; then
    echo -e "${RED}❌ GOOGLE_API_KEY não configurada em .env${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Configuração OK${NC}"
echo ""

# Ativar venv
if [ -d "venv" ]; then
    echo -e "${BLUE}Ativando virtual environment...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✓ venv ativado${NC}"
fi

echo ""
echo -e "${GREEN}🚀 Iniciando WebApp Nova (v0.3.0)...${NC}"
echo -e "${BLUE}URL: http://localhost:8000${NC}"
echo -e "${BLUE}Docs: http://localhost:8000/docs${NC}"
echo -e "${BLUE}Interface: http://localhost:8000/consulta${NC}"
echo ""

# Executar API nova
amldo-api
