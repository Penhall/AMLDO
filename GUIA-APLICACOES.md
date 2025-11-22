# Guia das Aplicações AMLDO

Este documento descreve as três interfaces disponíveis no AMLDO, cada uma com identidade visual única e casos de uso específicos.

---

## Visão Geral

| Aplicação | Porta | Tema | Inspiração | Ideal Para |
|-----------|-------|------|------------|------------|
| **FastAPI** | 8000 | NextChat (Dark/Azul) | NextChat UI | Desenvolvedores, integrações API |
| **Streamlit** | 8501 | Chat ONN (Light/Roxo) | Chat ONN UI | Usuários finais, análises |
| **Google ADK** | 8080 | MedCare (Dark/Navy) | MedCare Dashboard | Chatbot conversacional |

---

## 1. FastAPI REST API

### Identidade Visual - Tema NextChat
- **Estilo**: Dark mode profissional
- **Fundo**: Azul escuro (#1a1a2e, #16162a)
- **Acentos**: Azul/Ciano (#5b8def)
- **Cards**: Bordas sutis, sombras suaves
- **Inspiração**: Interface NextChat

![NextChat Theme](https://via.placeholder.com/800x400/1a1a2e/5b8def?text=FastAPI+NextChat+Theme)

### Como Executar

```bash
# Via script (recomendado)
python scripts/run.py --api

# Via comando direto
amldo-api

# Com configurações customizadas
API_HOST=0.0.0.0 API_PORT=8000 amldo-api
```

### URLs Disponíveis

| URL | Descrição |
|-----|-----------|
| http://localhost:8000 | Interface web principal |
| http://localhost:8000/consulta | Chat RAG interativo |
| http://localhost:8000/processamento | Upload e processamento de PDFs |
| http://localhost:8000/docs | Documentação Swagger/OpenAPI |
| http://localhost:8000/redoc | Documentação ReDoc |
| http://localhost:8000/health | Health check |

### Endpoints da API

```bash
# Consulta RAG
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "O que é pregão eletrônico?", "rag_version": "v2"}'

# Upload de PDF
curl -X POST http://localhost:8000/api/upload \
  -F "files=@documento.pdf"

# Processar documentos
curl -X POST http://localhost:8000/api/process

# Obter métricas
curl http://localhost:8000/api/metrics/stats
```

### Características do Tema NextChat

- Fundo escuro elegante com gradientes sutis
- Mensagens de chat com bordas arredondadas
- Code blocks com syntax highlighting
- Botões com gradiente azul
- Scrollbar minimalista
- Animações suaves de entrada

### Quando Usar

- Integrações com outros sistemas
- Automação de consultas
- Desenvolvimento de aplicações cliente
- Testes de API
- Ambiente de desenvolvimento

---

## 2. Streamlit Web App

### Identidade Visual - Tema Chat ONN
- **Estilo**: Light mode clean
- **Fundo**: Cinza claro (#f8f9fc)
- **Sidebar**: Roxo gradiente (#6c5ce7 → #5b4cdb)
- **Acentos**: Roxo/Violeta (#6c5ce7, #a29bfe)
- **Inspiração**: Interface Chat ONN

![Chat ONN Theme](https://via.placeholder.com/800x400/f8f9fc/6c5ce7?text=Streamlit+Chat+ONN+Theme)

### Como Executar

```bash
# Via script (recomendado)
python scripts/run.py --streamlit

# Via comando direto
streamlit run src/amldo/interfaces/streamlit/app.py
```

### URL

- http://localhost:8501

### Páginas Disponíveis

| Página | Descrição |
|--------|-----------|
| **Home** | Visão geral do sistema, métricas e status |
| **Pipeline** | Upload e processamento de documentos (3 etapas) |
| **RAG Query** | Interface de consultas com seleção de versão RAG |

### Características do Tema Chat ONN

- Sidebar com gradiente roxo vibrante
- Cards brancos com sombras suaves
- Botões com gradiente roxo
- Métricas destacadas em roxo
- File uploader com borda tracejada roxa
- Inputs com foco em roxo
- Alertas com gradientes suaves
- Design limpo e acolhedor

### Funcionalidades

**Pipeline de Processamento:**
1. **Ingestão**: Upload de PDF/TXT → extração de texto
2. **Estruturação**: Divisão automática em artigos (regex)
3. **Indexação**: Geração de embeddings e índice FAISS

**Consultas RAG:**
- Seleção entre RAG v1 e v2
- Configuração de parâmetros (k, search type)
- Histórico de consultas na sessão
- Exemplos de perguntas

### Quando Usar

- Usuários não-técnicos
- Análise exploratória de documentos
- Processamento de novos documentos com feedback visual
- Demonstrações e apresentações
- Treinamento de usuários

---

## 3. Google ADK Interface

### Identidade Visual - Tema MedCare
- **Estilo**: Dark mode elegante (interface nativa ADK)
- **Fundo**: Azul marinho escuro
- **Acentos**: Roxo/Rosa
- **Inspiração**: MedCare Dashboard

### Como Executar

```bash
# Via script (recomendado)
python scripts/run.py --adk

# Via comando direto
adk web --port 8080
```

**⚠️ IMPORTANTE**: O ADK pode levar 30-60 segundos para carregar devido aos pacotes Google Cloud/VertexAI. Aguarde a mensagem "Running on http://..." antes de acessar.

### URL

- http://localhost:8080

### Agentes Disponíveis

| Agente | Descrição | Recomendação |
|--------|-----------|--------------|
| **rag_v1** | RAG básico com MMR search | Consultas simples |
| **rag_v2** | RAG avançado com contexto hierárquico | **Recomendado** |
| **rag_v3** | RAG experimental com similarity search | Testes |

### Características

- Interface conversacional nativa do Google ADK
- Histórico de conversas persistente
- Múltiplos agentes selecionáveis
- Integração direta com Gemini API
- Design escuro profissional

### Quando Usar

- Interação conversacional natural
- Testes de agentes RAG
- Desenvolvimento de novos agentes
- Prototipagem rápida

---

## Executando Múltiplas Aplicações

### Todas Simultaneamente

```bash
# Inicia todas as 3 aplicações com logs separados
python scripts/run.py --all
```

Os logs ficam em:
- `logs/api.log` - FastAPI
- `logs/streamlit.log` - Streamlit
- `logs/adk.log` - Google ADK

### Menu Interativo

```bash
# Abre menu para escolher qual aplicação iniciar
python scripts/run.py
```

### Liberando Portas Ocupadas

```bash
# Mata processos nas portas 8000, 8501, 8080
python scripts/run.py --kill
```

---

## Docker (Recomendado para Produção)

O AMLDO pode ser executado em containers Docker para facilitar o deploy e garantir consistência entre ambientes.

### Pré-requisitos Docker

- Docker Engine 20.10+
- Docker Compose V2
- Arquivo `.env` configurado com `GOOGLE_API_KEY`

### Comandos Rápidos

```bash
# Via script Python (menu interativo)
python scripts/run.py --docker

# Ou comandos diretos do Docker Compose
docker-compose build                    # Build das imagens
docker-compose up -d                    # Iniciar todos os serviços
docker-compose up -d fastapi            # Apenas FastAPI
docker-compose up -d streamlit          # Apenas Streamlit
docker-compose up -d adk                # Apenas ADK
docker-compose logs -f                  # Ver logs
docker-compose down                     # Parar todos
```

### Build das Imagens

```bash
# Build de todas as imagens
docker-compose build

# Build específico por serviço
docker-compose build fastapi
docker-compose build streamlit
docker-compose build adk

# Build sem cache (forçar rebuild completo)
docker-compose build --no-cache
```

### Iniciar Serviços

```bash
# Todos os serviços principais
docker-compose up -d fastapi streamlit adk

# Apenas um serviço
docker-compose up -d fastapi    # FastAPI em http://localhost:8000
docker-compose up -d streamlit  # Streamlit em http://localhost:8501
docker-compose up -d adk        # ADK em http://localhost:8080

# Em modo desenvolvimento (com volumes montados)
docker-compose --profile dev up -d dev
```

### Monitoramento

```bash
# Status dos containers
docker-compose ps

# Logs em tempo real
docker-compose logs -f

# Logs de um serviço específico
docker-compose logs -f fastapi
docker-compose logs -f streamlit
docker-compose logs -f adk

# Acessar shell do container
docker-compose exec fastapi bash
```

### Parar Serviços

```bash
# Parar todos os containers
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Parar um serviço específico
docker-compose stop fastapi
```

### Configuração do Docker

| Arquivo | Descrição |
|---------|-----------|
| `Dockerfile` | Multi-stage build com targets: fastapi, streamlit, adk, dev |
| `docker-compose.yml` | Orquestração dos serviços |
| `.dockerignore` | Arquivos a excluir do build |

### Portas e URLs (Docker)

| Serviço | Porta | URL |
|---------|-------|-----|
| FastAPI | 8000 | http://localhost:8000 |
| Streamlit | 8501 | http://localhost:8501 |
| ADK | 8080 | http://localhost:8080 |

### Variáveis de Ambiente (Docker)

O Docker Compose lê automaticamente do arquivo `.env`. Configure:

```env
GOOGLE_API_KEY=sua_chave_aqui
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Troubleshooting Docker

**Container não inicia:**
```bash
# Ver logs detalhados
docker-compose logs fastapi

# Verificar se imagem foi buildada
docker images | grep amldo
```

**Porta em uso:**
```bash
# Liberar portas antes de iniciar Docker
python scripts/run.py --kill

# Ou verificar processos
docker ps -a
```

**Rebuild após mudanças:**
```bash
docker-compose build --no-cache
docker-compose up -d --force-recreate
```

---

## Comparação Visual dos Temas

| Aspecto | FastAPI (NextChat) | Streamlit (Chat ONN) | ADK (MedCare) |
|---------|-------------------|---------------------|---------------|
| **Modo** | Dark | Light | Dark |
| **Cor principal** | Azul (#5b8def) | Roxo (#6c5ce7) | Azul Navy |
| **Fundo** | #1a1a2e | #f8f9fc | Dark Navy |
| **Cards** | Dark com borda | Branco com sombra | Nativo ADK |
| **Botões** | Gradiente azul | Gradiente roxo | Nativo ADK |
| **Sidebar** | Dark | Roxo gradiente | Nativo ADK |

---

## Comparação de Recursos

| Recurso | FastAPI | Streamlit | ADK |
|---------|---------|-----------|-----|
| Consulta RAG | API + Web | Web | Chatbot |
| Upload de PDFs | Sim | Sim | Não |
| Processamento | Sim | Sim (3 etapas) | Não |
| Swagger Docs | Sim | Não | Não |
| Histórico | Não | Sessão | Sim |
| Métricas | Endpoint | Visual | Não |
| RAG v1 | Sim | Sim | Sim |
| RAG v2 | Sim | Sim | Sim |
| RAG v3 | Sim | Não | Sim |

---

## Requisitos

### Ambiente

```bash
# Python 3.11+
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instalar dependências
pip install -e ".[adk,streamlit,dev]"
```

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz:

```env
GOOGLE_API_KEY=sua_chave_aqui
```

---

## Troubleshooting

### Porta já em uso

```bash
# Liberar todas as portas do AMLDO
python scripts/run.py --kill
```

### ModuleNotFoundError

```bash
# Reinstalar em modo editável
pip install -e .
```

### ADK demora para carregar

Isso é normal! O ADK carrega pacotes pesados do Google Cloud. Aguarde 30-60 segundos até ver a mensagem "Running on http://...".

### Streamlit não carrega tema

O tema é aplicado via CSS inline. Se não carregar:
1. Limpe o cache do navegador (Ctrl+Shift+R)
2. Reinicie o Streamlit
3. Verifique se `theme.py` existe em `src/amldo/interfaces/streamlit/`

### FastAPI com visual antigo

Limpe o cache do navegador ou acesse em aba anônima para ver o novo tema NextChat.

---

## Arquivos de Interface

```
src/amldo/interfaces/
├── api/                          # FastAPI - Tema NextChat
│   ├── main.py                   # Aplicação principal
│   ├── routers/                  # Endpoints
│   ├── templates/                # HTML (Jinja2)
│   │   ├── index.html           # Home
│   │   ├── chat.html            # Consulta RAG
│   │   └── process.html         # Processamento
│   └── static/css/style.css     # Tema NextChat (Dark/Azul)
│
├── streamlit/                    # Streamlit - Tema Chat ONN
│   ├── app.py                   # Home + tema
│   ├── theme.py                 # CSS Chat ONN (Light/Roxo)
│   └── pages/
│       ├── 01_Pipeline.py       # Processamento
│       └── 02_RAG_Query.py      # Consultas
│
└── adk/                         # Google ADK - Tema MedCare
    └── __init__.py              # Configuração
```

---

## Versão

**AMLDO v0.3.0**

- FastAPI: Tema NextChat (Dark/Azul)
- Streamlit: Tema Chat ONN (Light/Roxo)
- ADK: Interface nativa (Dark/Navy)

---

*Documentação gerada para o projeto AMLDO - Sistema RAG para Legislação de Licitações*
