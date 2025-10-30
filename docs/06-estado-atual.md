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

**Última Atualização:** 2025-10-30

| Aspecto | Estado | Comentário |
|---------|--------|------------|
| **Ambiente** | ✅ Configurado | Python 3.11, venv, dependências |
| **Dados** | ✅ Processados | 4 leis indexadas (~500 artigos) |
| **RAG v1** | ✅ Funcional | Pipeline básico operacional |
| **RAG v2** | ✅ Funcional | Pipeline aprimorado operacional |
| **Interface** | ✅ Funcional | ADK Web rodando localmente |
| **Testes** | ⚠️ Ausentes | Sem testes automatizados |
| **Deploy** | ❌ Não implementado | Apenas desenvolvimento local |
| **Documentação** | ✅ Completa | Docs técnicas e guias |
| **Monitoramento** | ❌ Não implementado | Sem logs estruturados |

### Versões Ativas

| Componente | Versão | Notas |
|------------|--------|-------|
| **Python** | 3.11 | Obrigatório |
| **LangChain** | 1.0.2 | Estável |
| **FAISS** | 1.12.0 | CPU version |
| **Sentence Transformers** | 5.1.2 | Com PyTorch |
| **Google ADK** | 1.14.1 | Agente framework |
| **Gemini** | 2.5-flash | LLM via API |

## Funcionalidades Implementadas

### ✅ Pipeline RAG (v1 e v2)

**Status:** Completamente funcional

**Capacidades:**
- ✅ Busca semântica em documentos legais
- ✅ MMR (Maximal Marginal Relevance) para diversidade
- ✅ Similarity search para máxima relevância
- ✅ Respostas fundamentadas exclusivamente em documentos
- ✅ Suporte a perguntas em português brasileiro
- ✅ Contexto organizado hierarquicamente (v2)
- ✅ Injeção de artigos introdutórios (v2)

**Testado com:**
- ✅ Perguntas sobre limites de dispensa
- ✅ Consultas sobre procedimentos licitatórios
- ✅ Dúvidas sobre LGPD
- ✅ Questões sobre tratamento de ME/EPP
- ✅ Pregão eletrônico

### ✅ Interface Conversacional

**Status:** Funcional via ADK Web

**Capacidades:**
- ✅ Chat em tempo real
- ✅ Histórico de sessão
- ✅ Seleção de agente (v1 ou v2)
- ✅ Formatação de respostas
- ✅ Feedback visual (loading states)

**Limitações:**
- ⚠️ Apenas local (localhost)
- ⚠️ Sem autenticação
- ⚠️ Sem persistência de histórico entre sessões
- ⚠️ Sem multi-usuário

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

## Limitações Conhecidas

### 🔴 Críticas (Impedem uso em produção)

#### 1. Sem Autenticação/Autorização

**Problema:** Qualquer pessoa com acesso ao servidor pode usar o sistema

**Impacto:** 🔴 Alto
- Dados sensíveis podem ser expostos
- Não há controle de acesso
- Não é possível rastrear usuários

**Solução Futura:** Implementar autenticação (OAuth, JWT, etc.)

#### 2. Sem Testes Automatizados

**Problema:** Nenhum teste unitário, integração ou E2E

**Impacto:** 🔴 Alto
- Difícil garantir qualidade
- Refatorações são arriscadas
- Regressões podem passar despercebidas

**Solução Futura:** Criar suite de testes (pytest)

#### 3. Sem Monitoramento/Logs

**Problema:** Não há logs estruturados ou métricas

**Impacto:** 🔴 Médio
- Difícil debugar problemas em produção
- Não há visibilidade de performance
- Não é possível detectar anomalias

**Solução Futura:** Implementar logging (ELK, Datadog, etc.)

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

| Métrica | v1 (Básico) | v2 (Aprimorado) | Target |
|---------|-------------|-----------------|--------|
| **Latência média** | ~2-3s | ~3-5s | <5s |
| **Latência p95** | ~4s | ~6s | <8s |
| **Throughput** | ~1 req/s | ~1 req/s | 5 req/s |
| **Uso de memória** | ~500 MB | ~600 MB | <1 GB |

**Nota:** Métricas estimadas, não há medição formal

### Qualidade das Respostas

**Avaliação subjetiva** (baseada em testes manuais):

| Critério | v1 | v2 | Notas |
|----------|----|----|-------|
| **Relevância** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | v2 melhor com contexto estruturado |
| **Precisão** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Ambos citam artigos corretamente |
| **Completude** | ⭐⭐⭐ | ⭐⭐⭐⭐ | v2 inclui mais contexto |
| **Clareza** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Similar |
| **Sem alucinações** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Ambos muito bons |

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

- [ ] **Implementar testes automatizados**
  - [ ] Testes unitários (tools.py, agent.py)
  - [ ] Testes de integração (pipeline RAG completo)
  - [ ] Testes de regressão (perguntas gold com respostas esperadas)

- [ ] **Adicionar logging estruturado**
  - [ ] Logs de queries e respostas
  - [ ] Logs de performance (latência, tokens)
  - [ ] Logs de erros com stack trace

- [ ] **Implementar autenticação básica**
  - [ ] Login simples (usuário/senha)
  - [ ] Sessões isoladas

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
  - [ ] UI moderna (React, Vue)
  - [ ] Formatação de respostas (Markdown, highlight)
  - [ ] Histórico persistido

- [ ] **Sistema de feedback**
  - [ ] Botões 👍/👎
  - [ ] Comentários do usuário
  - [ ] Analytics de qualidade

- [ ] **Exportação de conversas**
  - [ ] Export para PDF
  - [ ] Export para DOCX
  - [ ] Share link

- [ ] **Múltiplos idiomas**
  - [ ] Interface em inglês
  - [ ] Perguntas em inglês (busca em PT)

## Histórico de Versões

### v1.0 (Atual) - 2025-10-30

**Adicionado:**
- ✅ Pipeline RAG básico (v1)
- ✅ Pipeline RAG aprimorado (v2)
- ✅ Interface ADK Web
- ✅ Processamento de 4 leis
- ✅ Índice FAISS com ~4k chunks
- ✅ Documentação completa

**Conhecido:**
- ⚠️ Sem testes
- ⚠️ Sem autenticação
- ⚠️ Apenas desenvolvimento local

### v0.1 (Beta) - Data desconhecida

**Adicionado:**
- Pipeline RAG básico (v1)
- Extração de documentos
- Índice FAISS inicial

**Notas:** Versão experimental

---

## Próximos Passos Recomendados

### Curto Prazo (1-2 semanas)

1. **Criar testes básicos** para rag_v1 e rag_v2
2. **Adicionar logging** (pelo menos print statements estruturados)
3. **Documentar bugs conhecidos** em GitHub Issues

### Médio Prazo (1-2 meses)

1. **Implementar autenticação simples**
2. **Adicionar cache de respostas** (Redis ou in-memory)
3. **Otimizar performance** (profiling, bottlenecks)
4. **Adicionar mais 5-10 documentos legais**

### Longo Prazo (3-6 meses)

1. **Deploy em produção** (servidor, domínio, HTTPS)
2. **Frontend customizado** com UX melhorada
3. **Sistema de feedback e analytics**
4. **Integração com outras fontes** (jurisprudência, pareceres)

---

**Próximo:** [Casos de Uso](07-casos-de-uso.md)
