#!/bin/bash
# Script para executar testes do AMLDO v0.3.0

set -e  # Exit on error

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  AMLDO v0.3.0 - Test Runner${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Verificar se venv está ativado
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment não detectado!${NC}"
    echo "Ativando venv..."
    source venv/bin/activate || {
        echo -e "${RED}❌ Erro ao ativar venv${NC}"
        exit 1
    }
fi

echo -e "${GREEN}✓ Virtual environment ativo: ${VIRTUAL_ENV}${NC}"
echo ""

# Parse argumentos
MODE="${1:-unit}"  # unit, integration, all, cov, fast

case "$MODE" in
    "unit")
        echo -e "${GREEN}📋 Executando testes unitários...${NC}"
        pytest tests/unit/ -v
        ;;

    "integration")
        echo -e "${GREEN}🔗 Executando testes de integração...${NC}"
        pytest tests/integration/ -v -m integration
        ;;

    "all")
        echo -e "${GREEN}🚀 Executando TODOS os testes...${NC}"
        pytest tests/ -v
        ;;

    "cov"|"coverage")
        echo -e "${GREEN}📊 Executando testes com cobertura...${NC}"
        pytest tests/ \
            --cov=src/amldo \
            --cov-report=html \
            --cov-report=term-missing \
            --cov-report=xml \
            -v

        echo ""
        echo -e "${GREEN}✓ Relatório de cobertura gerado!${NC}"
        echo "  - HTML: htmlcov/index.html"
        echo "  - XML: coverage.xml"
        echo ""
        ;;

    "fast")
        echo -e "${GREEN}⚡ Executando testes rápidos (sem integration/slow)...${NC}"
        pytest tests/ -v -m "not integration and not slow"
        ;;

    "watch")
        echo -e "${GREEN}👀 Modo watch (requer pytest-watch)...${NC}"
        if command -v ptw &> /dev/null; then
            ptw tests/ -- -v
        else
            echo -e "${RED}❌ pytest-watch não instalado${NC}"
            echo "Instale com: pip install pytest-watch"
            exit 1
        fi
        ;;

    "markers")
        echo -e "${GREEN}🏷️  Listando markers disponíveis...${NC}"
        pytest --markers
        ;;

    "help"|"-h"|"--help")
        echo "Uso: ./scripts/run_tests.sh [MODE]"
        echo ""
        echo "Modos disponíveis:"
        echo "  unit         - Testes unitários apenas (padrão)"
        echo "  integration  - Testes de integração apenas"
        echo "  all          - Todos os testes"
        echo "  cov          - Todos os testes com relatório de cobertura"
        echo "  fast         - Testes rápidos (exclui integration e slow)"
        echo "  watch        - Modo watch (requer pytest-watch)"
        echo "  markers      - Lista markers disponíveis"
        echo "  help         - Esta mensagem"
        echo ""
        echo "Exemplos:"
        echo "  ./scripts/run_tests.sh unit"
        echo "  ./scripts/run_tests.sh cov"
        echo "  pytest tests/unit/test_api.py -v"
        ;;

    *)
        echo -e "${RED}❌ Modo desconhecido: $MODE${NC}"
        echo "Use './scripts/run_tests.sh help' para ver opções"
        exit 1
        ;;
esac

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Testes concluídos com sucesso!${NC}"
else
    echo -e "${RED}❌ Alguns testes falharam (código: $EXIT_CODE)${NC}"
fi

exit $EXIT_CODE
