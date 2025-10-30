# AMLDO — Sistema RAG para Legislação de Licitações

> **Sistema de Retrieval-Augmented Generation (RAG)** especializado em legislação brasileira de licitações, compliance e governança.

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-1.0-green.svg)](https://langchain.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📋 Visão Geral

O **AMLDO** permite consultas em linguagem natural sobre legislação de licitações, retornando respostas precisas e fundamentadas exclusivamente nos documentos legais indexados.

### Principais Características

- ✅ **Busca Semântica Avançada** - Embeddings multilíngues + FAISS
- ✅ **Respostas Fundamentadas** - Cita artigos e leis (sem alucinações)
- ✅ **Interface Conversacional** - Chat em tempo real via Google ADK
- ✅ **2 Versões do RAG** - Básico (v1) e Aprimorado com contexto hierárquico (v2)
- ✅ **4 Documentos Indexados** - Lei 14.133, LGPD, LCP 123, Decreto 10.024

### Tecnologias

- **Python 3.11** | **LangChain** | **FAISS** | **Sentence Transformers** | **Gemini 2.5 Flash** | **Google ADK**

---

## 🚀 Quick Start

### Pré-requisitos

- Python **3.11** (obrigatório)
- API Key do Google Gemini ([Obter aqui](https://makersuite.google.com/app/apikey))

### Instalação (5 minutos)

```bash
# 1. Clonar repositório
git clone <url-do-repo>
cd AMLDO

# 2. Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
echo "GOOGLE_API_KEY=sua_chave_aqui" > .env

# 5. Rodar sistema
adk web
```

**Acesse:** http://localhost:8080

**Selecione o agente:** `rag_v2` (recomendado)

**Teste uma pergunta:**
```
Qual é o limite de valor para dispensa de licitação em obras?
```

---

## 📖 Documentação Completa

📚 **[Acesse a documentação completa em `/docs`](docs/README.md)**

### Guias Principais

| Documento | Descrição | Para Quem |
|-----------|-----------|-----------|
| **[Visão Geral](docs/00-visao-geral.md)** | Introdução, objetivos e contexto | Todos |
| **[Arquitetura Técnica](docs/01-arquitetura-tecnica.md)** | Componentes, camadas e decisões | Desenvolvedores |
| **[Pipeline RAG](docs/02-pipeline-rag.md)** | Como funciona o RAG internamente | Data Scientists |
| **[Estrutura de Dados](docs/03-estrutura-dados.md)** | Organização de dados e metadados | Data Engineers |
| **[Guia do Desenvolvedor](docs/04-guia-desenvolvedor.md)** | Setup, desenvolvimento e debugging | Desenvolvedores |
| **[Comandos e Fluxos](docs/05-comandos-fluxos.md)** | Comandos úteis e workflows | Todos |
| **[Estado Atual](docs/06-estado-atual.md)** | Funcionalidades e limitações | Gestores |
| **[Casos de Uso](docs/07-casos-de-uso.md)** | Exemplos práticos | Usuários finais |
| **[Melhorias e Roadmap](docs/08-melhorias-roadmap.md)** | Próximos passos | Stakeholders |

---

## 📁 Estrutura do Projeto

```
AMLDO/
├── data/                      # Dados do projeto
│   ├── raw/                   # PDFs originais (4 leis)
│   ├── split_docs/            # Documentos hierarquicamente divididos
│   ├── processed/             # CSVs processados
│   └── vector_db/             # Índice FAISS
│
├── rag_v1/                    # Versão 1 - RAG Básico
│   ├── agent.py               # Definição do agente
│   └── tools.py               # Pipeline RAG simples
│
├── rag_v2/                    # Versão 2 - RAG Aprimorado
│   ├── agent.py               # Definição do agente
│   └── tools.py               # Pipeline RAG com pós-processamento
│
├── docs/                      # Documentação completa
│   ├── README.md              # Índice da documentação
│   ├── 00-visao-geral.md
│   ├── 01-arquitetura-tecnica.md
│   └── ...
│
├── get_v1_data.ipynb          # Notebook: processar PDFs
├── get_vectorial_bank_v1.ipynb # Notebook: criar índice FAISS
├── order_rag_study.ipynb      # Notebook: análises
│
├── .env                       # Variáveis de ambiente (GOOGLE_API_KEY)
├── requirements.txt           # Dependências Python
├── README.md                  # Este arquivo
└── CLAUDE.md                  # Guia para Claude Code
```

---

## 🎯 Casos de Uso

### Exemplo 1: Consultar Limite de Dispensa

**Pergunta:**
> "Qual o limite de valor para dispensa em obras?"

**Resposta:**
> Segundo o Art. 75, inciso I da Lei 14.133/2021, é dispensável a licitação para contratações que envolvam valores inferiores a **R$ 50.000,00** no caso de obras e serviços de engenharia.

### Exemplo 2: LGPD em Licitações

**Pergunta:**
> "Como a LGPD se aplica a dados pessoais em licitações?"

**Resposta:**
> Segundo a Lei 13.709/2018 (LGPD), o tratamento de dados pessoais deve observar os princípios da **finalidade** e **necessidade**. Em licitações, colete apenas dados estritamente necessários para avaliar qualificação técnica e regularidade fiscal...

### Exemplo 3: Pregão Eletrônico

**Pergunta:**
> "Qual o prazo mínimo entre publicação e abertura de pregão?"

**Resposta:**
> Segundo o Art. 54 da Lei 14.133/2021, o prazo mínimo entre a publicação do edital e a abertura da sessão pública é de **8 dias úteis** para pregão eletrônico.

**[Ver mais casos de uso →](docs/07-casos-de-uso.md)**

---

## 🛠️ Desenvolvimento

### Adicionar Novo Documento

```bash
# 1. Adicionar PDF em data/raw/
cp ~/Lei99999.pdf data/raw/L99999.pdf

# 2. Processar (abrir Jupyter)
jupyter lab
# Executar get_v1_data.ipynb
# Executar get_vectorial_bank_v1.ipynb

# 3. Reiniciar servidor
adk web
```

### Modificar Pipeline RAG

```bash
# Editar código
code rag_v2/tools.py

# Salvar e reiniciar
# Ctrl+C
adk web
```

### Executar Testes

```bash
# Teste rápido
python quick_test.py

# Testes completos (quando implementados)
pytest tests/
```

**[Ver guia completo de desenvolvimento →](docs/04-guia-desenvolvedor.md)**

---

## 📊 Status do Projeto

| Aspecto | Estado |
|---------|--------|
| **Funcionalidade** | ✅ Operacional (desenvolvimento) |
| **Documentação** | ✅ Completa |
| **Testes** | ⚠️ Não implementados |
| **Autenticação** | ❌ Não implementado |
| **Deploy Produção** | ❌ Não implementado |

### Documentos Indexados

| Lei | Artigos | Status |
|-----|---------|--------|
| Lei 14.133/2021 (Licitações) | ~190 | ✅ |
| Lei 13.709/2018 (LGPD) | ~65 | ✅ |
| LCP 123/2006 (ME/EPP) | ~150 | ✅ |
| Decreto 10.024/2019 (Pregão) | ~40 | ✅ |

**[Ver estado completo do sistema →](docs/06-estado-atual.md)**

---

## 🗺️ Roadmap

### Q1 2025 - Fundações
- [ ] Testes automatizados
- [ ] Logging estruturado
- [ ] Autenticação básica
- [ ] +10 documentos
- [ ] Deploy staging

### Q2 2025 - Otimização
- [ ] Cache de respostas
- [ ] Frontend customizado
- [ ] Deploy produção

### Q3 2025 - Expansão
- [ ] Jurisprudência (TCU, STF)
- [ ] API pública
- [ ] Analytics

**[Ver roadmap completo →](docs/08-melhorias-roadmap.md)**

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja oportunidades em:

- **[Melhorias Propostas](docs/08-melhorias-roadmap.md#melhorias-propostas)**
- **[Issues no GitHub](#)** (se aplicável)

### Como Contribuir

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

---

## 🙏 Agradecimentos

- **Google** - Gemini API e ADK Framework
- **LangChain** - Framework RAG
- **Facebook AI** - FAISS
- **HuggingFace** - Sentence Transformers
- **Comunidade Open Source**

---

## 📞 Suporte

- 📚 **Documentação:** [docs/README.md](docs/README.md)
- 💬 **Dúvidas:** Abra uma issue
- 🐛 **Bugs:** Reporte via issues
- 💡 **Sugestões:** Contribua com PRs

---

**Desenvolvido com ❤️ pela equipe AMLDO**

**Última atualização:** 2025-10-30
