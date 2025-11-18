#!/bin/bash
# Script para executar FastAPI REST API
# Porta padrão: 8000

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🚀 Iniciando AMLDO FastAPI REST API${NC}"
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
    echo "Execute: python3.11 -m venv venv && source venv/bin/activate && pip install -e ."
    exit 1
fi

# Ativar virtual environment
echo -e "${BLUE}📦 Ativando virtual environment...${NC}"
source venv/bin/activate

# Verificar se o pacote está instalado
if ! python -c "import amldo" 2>/dev/null; then
    echo -e "${RED}❌ Erro: Pacote 'amldo' não instalado${NC}"
    echo "Execute: pip install -e ."
    exit 1
fi

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo -e "${RED}⚠️  Aviso: Arquivo .env não encontrado${NC}"
    echo "Crie um arquivo .env baseado em .env.example"
fi

# Configurar porta (padrão: 8000)
API_PORT=${API_PORT:-8000}
API_HOST=${API_HOST:-127.0.0.1}

echo -e "${GREEN}✅ Configuração:${NC}"
echo -e "   Host: ${API_HOST}"
echo -e "   Porta: ${API_PORT}"
echo ""
echo -e "${BLUE}📊 Acessos disponíveis:${NC}"
echo -e "   Interface Web: http://${API_HOST}:${API_PORT}"
echo -e "   Swagger Docs:  http://${API_HOST}:${API_PORT}/docs"
echo -e "   ReDoc:         http://${API_HOST}:${API_PORT}/redoc"
echo -e "   Health Check:  http://${API_HOST}:${API_PORT}/health"
echo ""
echo -e "${GREEN}🔍 Endpoints principais:${NC}"
echo -e "   POST /api/ask       - Consultas RAG"
echo -e "   POST /api/upload    - Upload de PDFs"
echo -e "   POST /api/process   - Processar documentos"
echo -e "   GET  /api/metrics/stats - Estatísticas"
echo ""
echo -e "${BLUE}────────────────────────────────────────────────────────────${NC}"
echo -e "${GREEN}Pressione Ctrl+C para parar o servidor${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Executar API
export API_HOST API_PORT
amldo-api
