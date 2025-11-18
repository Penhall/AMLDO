#!/bin/bash
# ============================================================================
# Script para executar AMLDO (Projeto 1)
# ============================================================================
# Uso: ./scripts/run_amldo.sh [interface]
#
# Interfaces disponíveis:
#   api       - FastAPI REST API (padrão)
#   streamlit - Interface web Streamlit
#   adk       - Google ADK CLI
#   all       - Todos via Docker Compose
# ============================================================================

set -e  # Exit on error

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${GREEN}"
cat << "EOF"
    ___    __  _____    ____  ____
   /   |  /  |/  / /   / __ \/ __ \
  / /| | / /|_/ / /   / / / / / / /
 / ___ |/ /  / / /___/ /_/ / /_/ /
/_/  |_/_/  /_/_____/_____/\____/

Projeto 1 - AMLDO v0.3.0
EOF
echo -e "${NC}"

# Variáveis
PROJECT_DIR="/mnt/d/PYTHON/AMLDO"
INTERFACE="${1:-api}"

# Mudar para diretório do projeto
cd "$PROJECT_DIR" || {
    echo -e "${RED}❌ Erro: Diretório $PROJECT_DIR não encontrado${NC}"
    exit 1
}

echo -e "${BLUE}📂 Diretório: $PROJECT_DIR${NC}"
echo -e "${BLUE}🚀 Interface: $INTERFACE${NC}"
echo ""

# Verificar .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env não encontrado!${NC}"
    echo -e "${BLUE}Criando .env a partir de .env.example...${NC}"
    cp .env.example .env
    echo -e "${RED}⚠️  IMPORTANTE: Configure GOOGLE_API_KEY no arquivo .env${NC}"
    echo -e "${BLUE}Execute: nano .env${NC}"
    exit 1
fi

# Verificar se GOOGLE_API_KEY está configurada
if grep -q "GOOGLE_API_KEY=sua_chave_aqui" .env || ! grep -q "GOOGLE_API_KEY=" .env; then
    echo -e "${RED}❌ GOOGLE_API_KEY não configurada em .env${NC}"
    echo -e "${BLUE}Execute: nano .env${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Configuração OK${NC}"
echo ""

# Executar de acordo com a interface escolhida
case "$INTERFACE" in
    api)
        echo -e "${GREEN}🚀 Iniciando FastAPI...${NC}"
        echo -e "${BLUE}URL: http://localhost:8000${NC}"
        echo -e "${BLUE}Docs: http://localhost:8000/docs${NC}"
        echo ""

        # Verificar se virtual env existe
        if [ -d "venv" ]; then
            echo -e "${BLUE}Ativando virtual environment...${NC}"
            source venv/bin/activate
        fi

        # Executar API
        amldo-api
        ;;

    streamlit)
        echo -e "${GREEN}🚀 Iniciando Streamlit...${NC}"
        echo -e "${BLUE}URL: http://localhost:8501${NC}"
        echo ""

        if [ -d "venv" ]; then
            source venv/bin/activate
        fi

        streamlit run src/amldo/interfaces/streamlit/app.py
        ;;

    adk)
        echo -e "${GREEN}🚀 Iniciando Google ADK...${NC}"
        echo -e "${BLUE}URL: http://localhost:8080${NC}"
        echo ""

        if [ -d "venv" ]; then
            source venv/bin/activate
        fi

        adk web
        ;;

    all|docker)
        echo -e "${GREEN}🐳 Iniciando com Docker Compose...${NC}"
        echo -e "${BLUE}API: http://localhost:8000${NC}"
        echo -e "${BLUE}Streamlit: http://localhost:8501${NC}"
        echo -e "${BLUE}ADK: http://localhost:8080${NC}"
        echo ""

        # Verificar se Docker está disponível
        if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
            echo -e "${RED}❌ Docker Compose não encontrado${NC}"
            exit 1
        fi

        docker-compose up -d

        echo ""
        echo -e "${GREEN}✅ Serviços iniciados!${NC}"
        echo ""
        echo -e "${BLUE}Ver logs:${NC} docker-compose logs -f"
        echo -e "${BLUE}Parar:${NC} docker-compose down"
        ;;

    *)
        echo -e "${RED}❌ Interface desconhecida: $INTERFACE${NC}"
        echo ""
        echo "Interfaces disponíveis:"
        echo "  api       - FastAPI REST API"
        echo "  streamlit - Interface web Streamlit"
        echo "  adk       - Google ADK CLI"
        echo "  all       - Todos via Docker Compose"
        echo ""
        echo "Uso: ./scripts/run_amldo.sh [interface]"
        exit 1
        ;;
esac
