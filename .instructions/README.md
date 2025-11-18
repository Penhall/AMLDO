# Instruções e Guias AMLDO

Documentação auxiliar para setup, troubleshooting e uso do sistema AMLDO.

## 📚 Índice de Documentos

### 🚀 Setup e Instalação

#### [`SETUP_VENV_RAPIDO.md`](SETUP_VENV_RAPIDO.md)
Guia rápido para configurar o virtual environment e instalar dependências.

**Quando usar:** Primeira instalação do projeto em Linux/Mac

**Conteúdo:**
- Criação de venv
- Instalação de dependências
- Verificação da instalação
- Ativação do ambiente

---

#### [`SETUP_WINDOWS_RAPIDO.md`](SETUP_WINDOWS_RAPIDO.md)
Guia completo para configurar o projeto no Windows.

**Quando usar:** Primeira instalação do projeto no Windows

**Conteúdo:**
- Pré-requisitos do Windows
- Instalação do Python 3.11
- Configuração do WSL (opcional)
- Setup de venv no Windows
- Configuração de variáveis de ambiente

---

### 🔧 Troubleshooting

#### [`TROUBLESHOOTING_WINDOWS.md`](TROUBLESHOOTING_WINDOWS.md)
Solução de problemas específicos do Windows.

**Quando usar:** Erros ao executar o projeto no Windows

**Conteúdo:**
- Erros de encoding
- Problemas com paths
- Conflitos de dependências
- Erros do LangChain/HuggingFace
- Problemas com FAISS
- Issues com Google ADK

---

#### [`FIX_LANGCHAIN_HUGGINGFACE.md`](FIX_LANGCHAIN_HUGGINGFACE.md)
Correção específica para problemas de compatibilidade LangChain + HuggingFace.

**Quando usar:** Erro `ImportError: cannot import name 'HuggingFaceEmbeddings'`

**Conteúdo:**
- Diagnóstico do problema
- Solução step-by-step
- Verificação da correção
- Alternativas

---

### 📖 Guias de Uso

#### [`QUICK_START_SCRIPTS.md`](QUICK_START_SCRIPTS.md)
Guia rápido de comandos e scripts mais usados.

**Quando usar:** Consulta rápida de comandos

**Conteúdo:**
- Scripts de execução
- Comandos CLI
- Atalhos úteis
- Workflows comuns

---

#### [`WEBAPPS_GUIDE.md`](WEBAPPS_GUIDE.md)
Guia completo sobre as aplicações web do projeto.

**Quando usar:** Entender as diferentes interfaces disponíveis

**Conteúdo:**
- FastAPI REST API
- Streamlit Web App
- Google ADK Interface
- Comparação entre interfaces
- Quando usar cada uma

---

## 🎯 Fluxo Recomendado

### Primeira Instalação

1. **Setup Inicial:**
   - Linux/Mac: Siga [`SETUP_VENV_RAPIDO.md`](SETUP_VENV_RAPIDO.md)
   - Windows: Siga [`SETUP_WINDOWS_RAPIDO.md`](SETUP_WINDOWS_RAPIDO.md)

2. **Configurar `.env`:**
   ```bash
   cp .env.example .env
   # Adicione GOOGLE_API_KEY
   ```

3. **Executar aplicações:**
   - Consulte [`WEBAPPS_GUIDE.md`](WEBAPPS_GUIDE.md)
   - Use scripts em `scripts/README.md`

### Encontrou um Problema?

1. **Windows:** Consulte [`TROUBLESHOOTING_WINDOWS.md`](TROUBLESHOOTING_WINDOWS.md)
2. **LangChain/HuggingFace:** Veja [`FIX_LANGCHAIN_HUGGINGFACE.md`](FIX_LANGCHAIN_HUGGINGFACE.md)
3. **Consulta rápida:** Use [`QUICK_START_SCRIPTS.md`](QUICK_START_SCRIPTS.md)

---

## 📁 Estrutura de Documentação

```
.instructions/          # Guias de setup e troubleshooting
├── README.md           # Este arquivo (índice)
├── SETUP_VENV_RAPIDO.md
├── SETUP_WINDOWS_RAPIDO.md
├── TROUBLESHOOTING_WINDOWS.md
├── FIX_LANGCHAIN_HUGGINGFACE.md
├── QUICK_START_SCRIPTS.md
└── WEBAPPS_GUIDE.md

docs/                   # Documentação técnica completa
├── 00-visao-geral.md
├── 01-arquitetura-tecnica.md
├── 02-pipeline-rag.md
├── ...
└── 12-ci-cd-deployment.md

scripts/                # Scripts de execução
├── README.md           # Guia dos scripts
├── run_api.sh
├── run_streamlit.sh
├── run_adk.sh
└── run_all.sh

CLAUDE.md              # Guia para desenvolvimento com Claude Code
MIGRATION.md           # Guia de migração v0.1 → v0.2+
README.md              # README principal do projeto
```

---

## 🔗 Links Úteis

- **README Principal:** `../README.md`
- **Documentação Técnica:** `../docs/`
- **Scripts de Execução:** `../scripts/README.md`
- **Guia de Desenvolvimento:** `../CLAUDE.md`
- **Guia de Migração:** `../MIGRATION.md`

---

## 💡 Dicas

- **Consulte primeiro:** `QUICK_START_SCRIPTS.md` para comandos rápidos
- **Windows:** Sempre verifique `TROUBLESHOOTING_WINDOWS.md` para problemas específicos
- **Desenvolvimento:** Use `CLAUDE.md` como referência principal
- **Documentação completa:** Acesse `docs/` para detalhes técnicos
