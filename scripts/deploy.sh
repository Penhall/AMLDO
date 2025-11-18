#!/bin/bash
# ============================================================================
# Script de Deploy para AMLDO v0.3.0
# ============================================================================
# Uso:
#   ./scripts/deploy.sh [environment] [options]
#
# Ambientes:
#   dev        - Desenvolvimento (padrão)
#   staging    - Homologação
#   production - Produção
#
# Opções:
#   --build    - Forçar rebuild de imagens Docker
#   --migrate  - Executar migrações de dados
#   --backup   - Fazer backup antes do deploy
# ============================================================================

set -e  # Exit on error

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de log
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Banner
echo -e "${GREEN}"
cat << "EOF"
    ___    __  _____    ____  ____
   /   |  /  |/  / /   / __ \/ __ \
  / /| | / /|_/ / /   / / / / / / /
 / ___ |/ /  / / /___/ /_/ / /_/ /
/_/  |_/_/  /_/_____/_____/\____/

Deploy Script v0.3.0
EOF
echo -e "${NC}"

# Variáveis padrão
ENVIRONMENT="${1:-dev}"
BUILD_FLAG=""
MIGRATE_FLAG=false
BACKUP_FLAG=false

# Parse argumentos
for arg in "$@"; do
    case $arg in
        --build)
            BUILD_FLAG="--build"
            ;;
        --migrate)
            MIGRATE_FLAG=true
            ;;
        --backup)
            BACKUP_FLAG=true
            ;;
    esac
done

log_info "Environment: $ENVIRONMENT"

# Verificar se ambiente é válido
case "$ENVIRONMENT" in
    dev|development)
        ENV_FILE=".env"
        COMPOSE_FILE="docker-compose.yml"
        ;;
    staging)
        ENV_FILE=".env.staging"
        COMPOSE_FILE="docker-compose.yml"
        ;;
    production|prod)
        ENV_FILE=".env.production"
        COMPOSE_FILE="docker-compose.yml"
        ;;
    *)
        log_error "Ambiente inválido: $ENVIRONMENT"
        echo "Ambientes válidos: dev, staging, production"
        exit 1
        ;;
esac

# Verificar se arquivo .env existe
if [ ! -f "$ENV_FILE" ]; then
    log_error "Arquivo de ambiente não encontrado: $ENV_FILE"
    log_info "Crie o arquivo a partir de .env.example"
    exit 1
fi

log_success "Usando configuração: $ENV_FILE"

# Verificar se GOOGLE_API_KEY está definida
if ! grep -q "GOOGLE_API_KEY=" "$ENV_FILE" || grep -q "GOOGLE_API_KEY=sua_chave_aqui" "$ENV_FILE"; then
    log_error "GOOGLE_API_KEY não configurada em $ENV_FILE"
    exit 1
fi

# Backup (se solicitado)
if [ "$BACKUP_FLAG" = true ]; then
    log_info "Criando backup..."
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"

    # Backup do banco de métricas
    if [ -f "data/metrics/metrics.db" ]; then
        cp data/metrics/metrics.db "$BACKUP_DIR/"
        log_success "Backup do banco de métricas criado"
    fi

    # Backup de configs
    cp -r data/processed "$BACKUP_DIR/" 2>/dev/null || true
    log_success "Backup criado em: $BACKUP_DIR"
fi

# Pre-flight checks
log_info "Verificando pré-requisitos..."

# Docker
if ! command -v docker &> /dev/null; then
    log_error "Docker não encontrado. Instale: https://docs.docker.com/get-docker/"
    exit 1
fi

# Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    log_error "Docker Compose não encontrado"
    exit 1
fi

log_success "Pré-requisitos OK"

# Criar diretórios necessários
log_info "Criando diretórios..."
mkdir -p data/raw data/processed data/vector_db data/metrics logs
log_success "Diretórios criados"

# Migrações (se solicitado)
if [ "$MIGRATE_FLAG" = true ]; then
    log_info "Executando migrações..."
    # Adicione comandos de migração aqui se necessário
    log_success "Migrações concluídas"
fi

# Deploy
log_info "Iniciando deploy..."

case "$ENVIRONMENT" in
    dev|development)
        log_info "Deploy em modo desenvolvimento..."
        docker-compose --env-file "$ENV_FILE" up -d $BUILD_FLAG api streamlit
        ;;

    staging)
        log_info "Deploy em staging..."
        docker-compose --env-file "$ENV_FILE" up -d $BUILD_FLAG
        ;;

    production|prod)
        log_warning "Deploy em PRODUÇÃO!"
        read -p "Tem certeza? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            log_info "Deploy cancelado"
            exit 0
        fi

        log_info "Fazendo pull das imagens..."
        docker-compose --env-file "$ENV_FILE" pull

        log_info "Iniciando serviços..."
        docker-compose --env-file "$ENV_FILE" --profile production up -d $BUILD_FLAG
        ;;
esac

# Aguardar serviços ficarem healthy
log_info "Aguardando serviços iniciarem..."
sleep 5

# Health check
log_info "Verificando health da API..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_success "API está saudável!"
        break
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -n "."
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    log_error "API não respondeu ao health check"
    log_info "Verificando logs..."
    docker-compose --env-file "$ENV_FILE" logs api
    exit 1
fi

# Mostrar status
log_info "Status dos serviços:"
docker-compose --env-file "$ENV_FILE" ps

# Mostrar URLs
echo ""
log_success "Deploy concluído! 🚀"
echo ""
echo -e "${BLUE}URLs disponíveis:${NC}"
echo "  • API:       http://localhost:8000"
echo "  • Docs:      http://localhost:8000/docs"
echo "  • Streamlit: http://localhost:8501"
echo "  • ADK:       http://localhost:8080"
echo ""
echo -e "${BLUE}Comandos úteis:${NC}"
echo "  • Logs:      docker-compose --env-file $ENV_FILE logs -f"
echo "  • Parar:     docker-compose --env-file $ENV_FILE down"
echo "  • Restart:   docker-compose --env-file $ENV_FILE restart"
echo "  • Shell:     docker-compose --env-file $ENV_FILE exec api bash"
echo ""
log_success "Deploy bem-sucedido! ✨"
