#!/bin/bash
# ============================================================================
# Script para executar MatchIt (Exemplo de Projeto 2)
# ============================================================================
# Este é um exemplo pré-configurado para o projeto MatchIt
# Copie e adapte este arquivo para seus outros projetos
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
║            MatchIt                    ║
║      Projeto de Matching              ║
║                                       ║
╚═══════════════════════════════════════╝
EOF
echo -e "${NC}"

# Configuração MatchIt
PROJECT_DIR="/mnt/d/PYTHON/MatchIt"
PROJECT_NAME="MatchIt"
PORT="8501"

# Mudar para diretório
cd "$PROJECT_DIR" || {
    echo -e "${RED}❌ Erro: Diretório $PROJECT_DIR não encontrado${NC}"
    echo -e "${YELLOW}⚠️  Ajuste PROJECT_DIR no script para o caminho correto${NC}"
    exit 1
}

echo -e "${BLUE}📂 Diretório: $PROJECT_DIR${NC}"
echo ""

# Verificar e criar .env se necessário
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo -e "${YELLOW}⚠️  .env não encontrado, criando...${NC}"
    cp .env.example .env
fi

# Ativar virtual environment se existir
if [ -d "venv" ]; then
    echo -e "${BLUE}Ativando virtual environment...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✓ venv ativado${NC}"
elif [ -d "env" ]; then
    source env/bin/activate
    echo -e "${GREEN}✓ env ativado${NC}"
fi

echo ""
echo -e "${GREEN}🚀 Iniciando MatchIt...${NC}"
echo -e "${BLUE}URL: http://localhost:$PORT${NC}"
echo ""

# Executar Streamlit (ajuste se for outro comando)
streamlit run app.py --server.port=$PORT
