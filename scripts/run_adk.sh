#!/bin/bash
# Script para executar Google ADK Interface
# Porta padrão: 8080

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🤖 Iniciando AMLDO Google ADK Interface${NC}"
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
    echo "Execute: python3.11 -m venv venv && source venv/bin/activate && pip install -e .[adk]"
    exit 1
fi

# Ativar virtual environment
echo -e "${BLUE}📦 Ativando virtual environment...${NC}"
source venv/bin/activate

# Verificar se o pacote está instalado
if ! python -c "import amldo" 2>/dev/null; then
    echo -e "${RED}❌ Erro: Pacote 'amldo' não instalado${NC}"
    echo "Execute: pip install -e .[adk]"
    exit 1
fi

# Verificar se ADK está instalado
if ! command -v adk &> /dev/null; then
    echo -e "${RED}❌ Erro: Google ADK não instalado${NC}"
    echo "Execute: pip install -e .[adk]"
    exit 1
fi

# Verificar se .env existe e GOOGLE_API_KEY está configurado
if [ ! -f ".env" ]; then
    echo -e "${RED}⚠️  Aviso: Arquivo .env não encontrado${NC}"
    echo "Crie um arquivo .env baseado em .env.example com GOOGLE_API_KEY"
fi

# Carregar .env se existir
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

if [ -z "$GOOGLE_API_KEY" ]; then
    echo -e "${RED}⚠️  Aviso: GOOGLE_API_KEY não configurado no .env${NC}"
fi

echo -e "${GREEN}✅ Configuração:${NC}"
echo -e "   Porta: 8080 (padrão ADK)"
echo ""
echo -e "${BLUE}📊 Interface disponível em:${NC}"
echo -e "   http://localhost:8080"
echo ""
echo -e "${GREEN}🤖 Agentes RAG disponíveis:${NC}"
echo -e "   • rag_v1 - RAG básico (MMR search)"
echo -e "   • rag_v2 - RAG avançado (contexto hierárquico + MMR)"
echo -e "   • rag_v3 - RAG experimental (similarity search)"
echo ""
echo -e "${BLUE}────────────────────────────────────────────────────────────${NC}"
echo -e "${GREEN}Pressione Ctrl+C para parar o servidor${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Executar ADK
adk web
