# ============================================================================
# Multi-stage Dockerfile for AMLDO v0.3.0
# ============================================================================

# ----------------------------------------------------------------------------
# Stage 1: Builder - Instalar dependências
# ----------------------------------------------------------------------------
FROM python:3.11-slim as builder

LABEL maintainer="AMLDO Team"
LABEL version="0.3.0"
LABEL description="Sistema RAG para licitações públicas e compliance"

# Variáveis de build
ARG DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /build

# Copiar arquivos de dependências
COPY pyproject.toml README.md ./
COPY requirements/ ./requirements/

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/base.txt

# ----------------------------------------------------------------------------
# Stage 2: Runtime - Imagem final
# ----------------------------------------------------------------------------
FROM python:3.11-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    ENVIRONMENT=production \
    LOG_LEVEL=INFO

# Instalar dependências mínimas do sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN useradd -m -u 1000 amldo && \
    mkdir -p /app /data && \
    chown -R amldo:amldo /app /data

# Definir diretório de trabalho
WORKDIR /app

# Copiar dependências do builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código da aplicação
COPY --chown=amldo:amldo . .

# Instalar aplicação em modo editable
RUN pip install --no-cache-dir -e .

# Criar diretórios necessários
RUN mkdir -p \
    data/raw \
    data/processed \
    data/vector_db \
    data/metrics \
    logs && \
    chown -R amldo:amldo data/ logs/

# Trocar para usuário não-root
USER amldo

# Expor portas
EXPOSE 8000  # FastAPI
EXPOSE 8080  # Google ADK
EXPOSE 8501  # Streamlit

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando padrão (FastAPI)
CMD ["amldo-api"]

# ----------------------------------------------------------------------------
# Build instructions:
# docker build -t amldo:latest .
# docker build -t amldo:0.3.0 .
#
# Run:
# docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key amldo:latest
# ----------------------------------------------------------------------------
