#!/bin/bash
# Script para executar Streamlit Web App
# Porta padrão: 8501

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎨 Iniciando AMLDO Streamlit Web App${NC}"
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
    echo "Execute: python3.11 -m venv venv && source venv/bin/activate && pip install -e .[streamlit]"
    exit 1
fi

# Ativar virtual environment
echo -e "${BLUE}📦 Ativando virtual environment...${NC}"
source venv/bin/activate

# Verificar se o pacote está instalado
if ! python -c "import amldo" 2>/dev/null; then
    echo -e "${RED}❌ Erro: Pacote 'amldo' não instalado${NC}"
    echo "Execute: pip install -e .[streamlit]"
    exit 1
fi

# Verificar se Streamlit está instalado
if ! command -v streamlit &> /dev/null; then
    echo -e "${RED}❌ Erro: Streamlit não instalado${NC}"
    echo "Execute: pip install -e .[streamlit]"
    exit 1
fi

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo -e "${RED}⚠️  Aviso: Arquivo .env não encontrado${NC}"
    echo "Crie um arquivo .env baseado em .env.example"
fi

# Configurar porta (padrão: 8501)
STREAMLIT_PORT=${STREAMLIT_PORT:-8501}

echo -e "${GREEN}✅ Configuração:${NC}"
echo -e "   Porta: ${STREAMLIT_PORT}"
echo ""
echo -e "${BLUE}📊 Interface disponível em:${NC}"
echo -e "   http://localhost:${STREAMLIT_PORT}"
echo ""
echo -e "${GREEN}📄 Páginas disponíveis:${NC}"
echo -e "   • Home        - Visão geral do sistema"
echo -e "   • Pipeline    - Processamento de documentos"
echo -e "   • RAG Query   - Consultas à base de conhecimento"
echo ""
echo -e "${BLUE}────────────────────────────────────────────────────────────${NC}"
echo -e "${GREEN}Pressione Ctrl+C para parar o servidor${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Executar Streamlit
streamlit run src/amldo/interfaces/streamlit/app.py --server.port=${STREAMLIT_PORT}
