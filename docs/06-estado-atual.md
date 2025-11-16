# Estado Atual do Sistema AMLDO

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Funcionalidades Implementadas](#funcionalidades-implementadas)
- [Limitações Conhecidas](#limitações-conhecidas)
- [Métricas de Qualidade](#métricas-de-qualidade)
- [Pendências e TODOs](#pendências-e-todos)
- [Histórico de Versões](#histórico-de-versões)

## Visão Geral

### Status do Projeto

🟢 **Status:** Funcional em ambiente de desenvolvimento

**Última Atualização:** 2025-11-16

| Aspecto | Estado | Comentário |
|---------|--------|------------|
| **Ambiente** | ✅ Configurado | Python 3.11, venv, dependências |
| **Dados** | ✅ Processados | 4 leis indexadas (~500 artigos) |
| **RAG v1** | ✅ Funcional | Pipeline básico operacional |
| **RAG v2** | ✅ Funcional | Pipeline aprimorado operacional |
| **RAG v3** | ✅ Funcional | Pipeline experimental (similarity search) ✨ NOVO |
| **REST API** | ✅ Funcional | FastAPI com 8+ endpoints ✨ NOVO |
| **Interface** | ✅ Funcional | ADK Web + Streamlit + FastAPI Web |
| **Testes** | ⚠️ Parcial | Testes unitários para métricas e RAG v3 ✨ NOVO |
| **Deploy** | ❌ Não implementado | Apenas desenvolvimento local |
| **Documentação** | ✅ Completa | Docs técnicas + API REST |
| **Monitoramento** | ⚠️ Parcial | Sistema de métricas SQLite ✨ NOVO |

### Versões Ativas

| Componente | Versão | Notas |
|------------|--------|-------|
| **Python** | 3.11 | Obrigatório |
| **LangChain** | 1.0.2 | Estável |
| **FAISS** | 1.12.0 | CPU version |
| **Sentence Transformers** | 5.1.2 | Com PyTorch |
| **Google ADK** | 1.14.1 | Agente framework |
| **FastAPI** | 0.110+ | REST API framework ✨ NOVO |
| **Streamlit** | Latest | Web interface |
| **Gemini** | 2.5-flash | LLM via API |

## Funcionalidades Implementadas

### ✅ Pipeline RAG (v1, v2 e v3)

**Status:** Completamente funcional

**Capacidades:**
- ✅ Busca semântica em documentos legais
- ✅ MMR (Maximal Marginal Relevance) para diversidade (v1, v2)
- ✅ Similarity search para máxima relevância (v3) ✨ NOVO
- ✅ Respostas fundamentadas exclusivamente em documentos
- ✅ Suporte a perguntas em português brasileiro
- ✅ Contexto organizado hierarquicamente (v2, v3)
- ✅ Injeção de artigos introdutórios (v2, v3)

**Testado com:**
- ✅ Perguntas sobre limites de dispensa
- ✅ Consultas sobre procedimentos licitatórios
- ✅ Dúvidas sobre LGPD
- ✅ Questões sobre tratamento de ME/EPP
- ✅ Pregão eletrônico

### ✅ Interfaces do Usuário

**Status:** Múltiplas interfaces funcionais

**1. REST API (FastAPI)** ✨ NOVO

**Capacidades:**
- ✅ 8+ endpoints RESTful (query, upload, process, metrics)
- ✅ Documentação automática OpenAPI/Swagger (`/docs`)
- ✅ Interface web interativa (chat, upload, processamento)
- ✅ CORS habilitado para integrações
- ✅ Validação robusta com Pydantic
- ✅ Suporte às 3 versões RAG (v1, v2, v3)

**2. ADK Web (Google)**

**Capacidades:**
- ✅ Chat em tempo real
- ✅ Histórico de sessão
- ✅ Seleção de agente (v1, v2 ou v3)
- ✅ Formatação de respostas
- ✅ Feedback visual (loading states)

**3. Streamlit**

**Capacidades:**
- ✅ Interface web moderna
- ✅ Upload de documentos
- ✅ Pipeline de processamento visual
- ✅ Consultas RAG

**Limitações Gerais:**
- ⚠️ Apenas local (localhost)
- ⚠️ Sem autenticação (exceto possível integração futura)
- ⚠️ Sem persistência de histórico entre sessões (FastAPI permite implementar)
- ⚠️ Sem multi-usuário real (mas FastAPI suporta)

### ✅ Processamento de Documentos

**Status:** Funcional via Notebooks

**Capacidades:**
- ✅ Extração de texto de PDFs
- ✅ Divisão hierárquica (Lei/Título/Cap/Art)
- ✅ Geração de chunks com overlap
- ✅ Embeddings multilíngues
- ✅ Indexação FAISS
- ✅ Metadados estruturados

**Documentos Processados:**

| Lei | Status | Artigos | Chunks |
|-----|--------|---------|--------|
| Lei 14.133/2021 | ✅ | ~190 | ~2000 |
| Lei 13.709/2018 (LGPD) | ✅ | ~65 | ~600 |
| LCP 123/2006 | ✅ | ~150 | ~1000 |
| Decreto 10.024/2019 | ✅ | ~40 | ~400 |
| **TOTAL** | ✅ | **~445** | **~4000** |

### ✅ Estrutura de Dados

**Status:** Organizada e documentada

**Camadas:**
- ✅ `data/raw/` - PDFs originais (4 documentos)
- ✅ `data/split_docs/` - Hierarquia de TXTs
- ✅ `data/processed/` - CSVs tabulares
- ✅ `data/vector_db/` - Índice FAISS persistido
- ✅ `data/metrics/` - Banco SQLite de métricas ✨ NOVO

### ✅ Sistema de Métricas

**Status:** Funcional com SQLite ✨ NOVO

**Capacidades:**
- ✅ Tracking de queries RAG (pergunta, versão, tempo de resposta, sucesso/erro)
- ✅ Tracking de processamento (arquivos, chunks, duração)
- ✅ Estatísticas agregadas (COUNT, AVG, MIN, MAX por versão RAG)
- ✅ Histórico completo com timestamps
- ✅ Filtros por versão RAG e período
- ✅ Limpeza automática de registros antigos
- ✅ Endpoints REST para consulta (`/api/metrics/*`)

**Dados Coletados:**
- 📊 Total de queries por versão RAG
- ⏱️ Tempos de resposta (média, mínimo, máximo)
- ✅ Taxa de sucesso/falha
- 📁 Arquivos processados e chunks indexados
- 📅 Atividade nas últimas 24 horas

**Banco de Dados:**
- `data/metrics/metrics.db` (SQLite)
- 2 tabelas: `processing_history`, `query_history`
- Índices para performance
- Singleton pattern para acesso global

## Limitações Conhecidas

### 🔴 Críticas (Impedem uso em produção)

#### 1. Sem Autenticação/Autorização

**Problema:** Qualquer pessoa com acesso ao servidor pode usar o sistema

**Impacto:** 🔴 Alto
- Dados sensíveis podem ser expostos
- Não há controle de acesso
- Não é possível rastrear usuários

**Solução Futura:** Implementar autenticação (OAuth, JWT, etc.)

#### 2. Sem Testes Completos

**Problema:** Testes parciais (apenas métricas e RAG v3), faltam integração e E2E

**Impacto:** 🔴 Alto
- Difícil garantir qualidade total
- Refatorações ainda são arriscadas
- Regressões podem passar em áreas não testadas

**Status Atual:** ⚠️ Parcialmente resolvido (testes unitários para métricas e RAG v3)

**Solução Futura:** Completar suite de testes (pytest) para toda a aplicação

#### 3. Sem Logging Estruturado

**Problema:** Não há logs estruturados (apenas métricas básicas)

**Impacto:** 🟡 Médio
- Difícil debugar problemas em produção
- Métricas SQLite ajudam mas não substituem logs completos
- Não há rastreamento de erros com stack trace

**Status Atual:** ⚠️ Parcialmente resolvido (sistema de métricas SQLite)

**Solução Futura:** Implementar logging estruturado (ELK, Datadog, etc.)

#### 4. Dependência de API Externa (Gemini)

**Problema:** Sistema para se Gemini API ficar fora

**Impacto:** 🔴 Alto
- Single point of failure
- Latência depende da Google
- Custos variáveis

**Solução Futura:** Fallback para modelo local (Ollama)

### 🟡 Importantes (Limitam funcionalidade)

#### 5. Sem Persistência de Histórico

**Problema:** Histórico de conversação perdido ao fechar browser

**Impacto:** 🟡 Médio
- Usuários não podem revisar conversas antigas
- Não há aprendizado entre sessões

**Solução Futura:** Banco de dados (SQLite, PostgreSQL)

#### 6. Sem Multi-Usuário

**Problema:** Apenas um usuário por vez (na prática)

**Impacto:** 🟡 Médio
- Não escala para equipe
- Sessões podem se misturar

**Solução Futura:** Sessões isoladas por usuário

#### 7. Sem Cache de Respostas

**Problema:** Mesma pergunta = nova consulta ao LLM

**Impacto:** 🟡 Médio
- Latência desnecessária
- Custo maior (API calls)

**Solução Futura:** Cache de respostas (Redis, Memcached)

#### 8. Contexto Limitado (k=12)

**Problema:** Recupera apenas 12 chunks, pode perder informação

**Impacto:** 🟡 Médio
- Perguntas complexas podem ter respostas incompletas
- Leis muito longas ficam fragmentadas

**Solução Futura:** Ajuste dinâmico de k, ou summarização

### 🟢 Menores (Melhorias desejáveis)

#### 9. Sem Feedback do Usuário

**Problema:** Não há como usuário avaliar resposta (👍/👎)

**Impacto:** 🟢 Baixo
- Não há dados para melhorar sistema

**Solução Futura:** Sistema de rating e feedback

#### 10. Interface Básica

**Problema:** ADK Web é funcional mas não customizada

**Impacto:** 🟢 Baixo
- UX poderia ser melhor
- Sem branding

**Solução Futura:** Frontend customizado (React, Streamlit)

#### 11. Sem Exportação de Respostas

**Problema:** Não dá para exportar conversação (PDF, DOCX)

**Impacto:** 🟢 Baixo
- Usuários não podem salvar/compartilhar facilmente

**Solução Futura:** Botão de export

## Métricas de Qualidade

### Performance

| Métrica | v1 (Básico) | v2 (Aprimorado) | v3 (Experimental) | Target |
|---------|-------------|-----------------|-------------------|--------|
| **Latência média** | ~2-3s | ~3-5s | ~2-4s | <5s |
| **Latência p95** | ~4s | ~6s | ~5s | <8s |
| **Throughput** | ~1 req/s | ~1 req/s | ~1 req/s | 5 req/s |
| **Uso de memória** | ~500 MB | ~600 MB | ~600 MB | <1 GB |

**Nota:** Métricas baseadas em sistema de tracking SQLite (v0.3.0) e observação manual

### Dados Reais do Sistema de Métricas ✨ NOVO

**Tracking ativo desde:** v0.3.0 (2025-11-16)

O sistema agora coleta métricas automáticas via SQLite:
- ✅ Tempo de resposta de cada query (ms)
- ✅ Taxa de sucesso/falha por versão RAG
- ✅ Contagem de uso por versão
- ✅ Performance de processamento de documentos

**Consultar métricas:**
```bash
curl "http://localhost:8000/api/metrics/stats"
```

### Qualidade das Respostas

**Avaliação subjetiva** (baseada em testes manuais):

| Critério | v1 | v2 | v3 | Notas |
|----------|----|----|----|----|
| **Relevância** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | v2 melhor com MMR + contexto |
| **Precisão** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Todos citam artigos corretamente |
| **Completude** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | v2/v3 com mais contexto |
| **Clareza** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Similar entre versões |
| **Sem alucinações** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Todos excelentes |

**Recomendação de uso:**
- **v2 (padrão)**: Melhor equilíbrio qualidade/performance para produção
- **v1**: Testes rápidos e prototipagem
- **v3**: Experimentação com similarity search pura

### Cobertura de Documentos

| Lei | Cobertura | Qualidade Index |
|-----|-----------|-----------------|
| Lei 14.133/2021 | 100% | ⭐⭐⭐⭐⭐ |
| Lei 13.709/2018 | 100% | ⭐⭐⭐⭐⭐ |
| LCP 123/2006 | 100% | ⭐⭐⭐⭐⭐ |
| Decreto 10.024/2019 | 100% | ⭐⭐⭐⭐⭐ |

**Cobertura:** Porcentagem de artigos indexados
**Qualidade:** Avaliação da extração de texto e chunking

## Pendências e TODOs

### 🔥 Alta Prioridade

- [ ] **Completar testes automatizados**
  - [x] Testes unitários para métricas ✅ FEITO
  - [x] Testes unitários para RAG v3 ✅ FEITO
  - [ ] Testes unitários para RAG v1 e v2
  - [ ] Testes de integração (pipeline RAG completo)
  - [ ] Testes de integração da REST API
  - [ ] Testes de regressão (perguntas gold com respostas esperadas)
  - [ ] Testes E2E

- [ ] **Adicionar logging estruturado**
  - [x] Sistema de métricas SQLite ✅ FEITO
  - [ ] Logs de debug com stack trace
  - [ ] Integração com ELK/Datadog
  - [ ] Alertas de erro

- [ ] **Implementar autenticação básica**
  - [ ] Login simples (usuário/senha)
  - [ ] Sessões isoladas por usuário
  - [ ] JWT ou OAuth para REST API

### 📋 Média Prioridade

- [ ] **Cache de respostas**
  - [ ] Hash de query → resposta
  - [ ] TTL configurável
  - [ ] Invalidation strategy

- [ ] **Melhorar tratamento de erros**
  - [ ] Validação de input
  - [ ] Mensagens de erro amigáveis
  - [ ] Retry logic para API calls

- [ ] **Adicionar mais documentos**
  - [ ] Lei 8.666/1993 (lei antiga de licitações)
  - [ ] Instruções Normativas relevantes
  - [ ] Jurisprudência (TCU, STF)

- [ ] **Otimizar performance**
  - [ ] Cache de embeddings
  - [ ] Batch processing de queries
  - [ ] Usar GPU para embeddings (se disponível)

### 💡 Baixa Prioridade

- [ ] **Frontend customizado**
  - [x] Interface FastAPI web básica ✅ FEITO
  - [x] Interface Streamlit ✅ FEITO
  - [ ] UI moderna completa (React, Vue)
  - [ ] Formatação avançada de respostas (Markdown, highlight)
  - [ ] Histórico persistido no frontend

- [ ] **Sistema de feedback**
  - [ ] Botões 👍/👎
  - [ ] Comentários do usuário
  - [ ] Analytics de qualidade
  - [ ] Integração com métricas SQLite

- [ ] **Exportação de conversas**
  - [ ] Export para PDF
  - [ ] Export para DOCX
  - [ ] Share link
  - [ ] Download de histórico via API

- [ ] **Múltiplos idiomas**
  - [ ] Interface em inglês
  - [ ] Perguntas em inglês (busca em PT)

- [ ] **Deploy e DevOps**
  - [ ] Containerização (Docker)
  - [ ] CI/CD pipeline
  - [ ] Deploy em cloud (AWS, GCP, Azure)
  - [ ] HTTPS e domínio
  - [ ] Monitoramento de produção

## Histórico de Versões

### v0.3.0 (Atual) - 2025-11-16

**Adicionado:**
- ✨ REST API completa com FastAPI (8+ endpoints)
- ✨ Sistema de métricas com SQLite (tracking automático)
- ✨ Pipeline RAG v3 (similarity search experimental)
- ✨ Interface web interativa (chat, upload, processamento)
- ✨ Testes unitários para métricas e RAG v3
- ✨ Documentação completa da API REST
- ✨ Suporte às 3 versões RAG via API
- ✨ Validação robusta com Pydantic
- ✨ CORS habilitado para integrações

**Melhorado:**
- 📊 Visibilidade de performance com métricas reais
- 📝 Documentação atualizada para v0.3.0
- 🧪 Cobertura de testes parcial (vs zero antes)

**Conhecido:**
- ⚠️ Testes incompletos (apenas métricas e RAG v3)
- ⚠️ Sem autenticação
- ⚠️ Apenas desenvolvimento local
- ⚠️ Logging estruturado parcial (métricas, mas não logs completos)

### v0.2.0 - 2025-11-14

**Adicionado:**
- 🏗️ Reestruturação completa para `src/` layout
- ⚙️ Configuração centralizada com pydantic-settings
- 🎨 Interface Streamlit
- 📦 Pipeline de processamento integrado (REAL embeddings)
- 🤖 Sistema multi-agente CrewAI
- 📚 Documentação completa (8 documentos)

### v0.1.0 - 2025-10-30

**Adicionado:**
- ✅ Pipeline RAG básico (v1)
- ✅ Pipeline RAG aprimorado (v2)
- ✅ Interface ADK Web
- ✅ Processamento de 4 leis
- ✅ Índice FAISS com ~4k chunks
- ✅ Documentação completa

**Notas:** Release inicial funcional

---

## Próximos Passos Recomendados

### Curto Prazo (1-2 semanas)

1. **Completar testes para RAG v1 e v2** (já temos v3 e métricas ✅)
2. **Testar REST API** em ambiente de produção simulado
3. **Adicionar autenticação básica** à REST API (JWT)
4. **Documentar bugs conhecidos** em GitHub Issues

### Médio Prazo (1-2 meses)

1. **Implementar logging estruturado** completo (além de métricas)
2. **Adicionar cache de respostas** (Redis ou in-memory)
3. **Otimizar performance** da REST API (profiling, bottlenecks)
4. **Containerização** (Docker + Docker Compose)
5. **Adicionar mais 5-10 documentos legais**

### Longo Prazo (3-6 meses)

1. **Deploy em produção** (servidor, domínio, HTTPS)
2. **Frontend React/Vue** customizado com UX melhorada
3. **Sistema de feedback** integrado com métricas SQLite
4. **CI/CD pipeline** completo
5. **Integração com outras fontes** (jurisprudência, pareceres)

---

**Próximo:** [Casos de Uso](07-casos-de-uso.md)
