#!/bin/bash
# ============================================================================
# Script para executar Projeto 2
# ============================================================================
# PERSONALIZE ESTE SCRIPT COM AS INFORMAÇÕES DO SEU PROJETO 2
#
# Exemplo: Se seu Projeto 2 é MatchIt, ajuste:
#   PROJECT_DIR="/mnt/d/PYTHON/MatchIt"
#   PROJECT_NAME="MatchIt"
#   COMMAND="python app.py"  # ou o comando correto
# ============================================================================

set -e  # Exit on error

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ============================================================================
# ⚙️ CONFIGURAÇÃO - EDITE AQUI
# ============================================================================

# Diretório do Projeto 2
PROJECT_DIR="/mnt/d/PYTHON/SEU_PROJETO_AQUI"

# Nome do projeto (para display)
PROJECT_NAME="Projeto 2"

# Comando para executar o projeto (exemplos):
# - "python app.py"
# - "streamlit run app.py"
# - "uvicorn main:app --reload"
# - "flask run"
# - "docker-compose up -d"
RUN_COMMAND="python main.py"

# Porta do projeto (para display)
PORT="8000"

# Arquivo .env necessário? (true/false)
NEEDS_ENV=true

# Virtual environment existe? (true/false)
HAS_VENV=true

# ============================================================================
# SCRIPT (NÃO EDITE ABAIXO DESTA LINHA, A MENOS QUE SAIBA O QUE ESTÁ FAZENDO)
# ============================================================================

echo -e "${GREEN}"
cat << EOF
╔═══════════════════════════════════════╗
║                                       ║
║      $PROJECT_NAME
║                                       ║
╚═══════════════════════════════════════╝
EOF
echo -e "${NC}"

# Mudar para diretório do projeto
cd "$PROJECT_DIR" || {
    echo -e "${RED}❌ Erro: Diretório $PROJECT_DIR não encontrado${NC}"
    echo -e "${YELLOW}⚠️  EDITE O SCRIPT e configure PROJECT_DIR corretamente${NC}"
    exit 1
}

echo -e "${BLUE}📂 Diretório: $PROJECT_DIR${NC}"
echo ""

# Verificar .env se necessário
if [ "$NEEDS_ENV" = true ]; then
    if [ ! -f ".env" ] && [ -f ".env.example" ]; then
        echo -e "${YELLOW}⚠️  Arquivo .env não encontrado!${NC}"
        echo -e "${BLUE}Criando .env a partir de .env.example...${NC}"
        cp .env.example .env
        echo -e "${RED}⚠️  IMPORTANTE: Configure as variáveis no arquivo .env${NC}"
        echo -e "${BLUE}Execute: nano .env${NC}"
        exit 1
    fi
fi

# Ativar virtual environment se existir
if [ "$HAS_VENV" = true ] && [ -d "venv" ]; then
    echo -e "${BLUE}Ativando virtual environment...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment ativado${NC}"
fi

echo -e "${GREEN}✓ Configuração OK${NC}"
echo ""

# Executar projeto
echo -e "${GREEN}🚀 Iniciando $PROJECT_NAME...${NC}"
if [ -n "$PORT" ]; then
    echo -e "${BLUE}URL: http://localhost:$PORT${NC}"
fi
echo ""

eval "$RUN_COMMAND"
