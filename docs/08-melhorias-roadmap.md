# Melhorias e Roadmap do AMLDO

## 📋 Sumário

- [Visão de Produto](#visão-de-produto)
- [Melhorias Propostas](#melhorias-propostas)
- [Roadmap](#roadmap)
- [Ideias Futuras](#ideias-futuras)
- [Critérios de Priorização](#critérios-de-priorização)

## Visão de Produto

### Onde Estamos (v1.0)

✅ Sistema RAG funcional para consultas sobre legislação
✅ Interface web básica
✅ 4 documentos legais indexados
✅ Respostas fundamentadas e precisas

### Onde Queremos Chegar (v2.0)

🎯 **Visão:** Ser a ferramenta de referência para profissionais de licitações e compliance consultarem legislação brasileira.

**Objetivos:**
- 🔹 **Cobertura:** 50+ documentos legais (leis, decretos, INs, jurisprudência)
- 🔹 **Qualidade:** >95% de precisão nas respostas
- 🔹 **Performance:** <2s de latência média
- 🔹 **Usabilidade:** Interface intuitiva e rápida
- 🔹 **Confiabilidade:** 99.9% uptime em produção
- 🔹 **Segurança:** Autenticação, auditoria, LGPD compliance

### Proposta de Valor

| Stakeholder | Valor Entregue |
|-------------|----------------|
| **Gestores Públicos** | Economia de 80% do tempo em consultas legais |
| **Advogados** | Citações precisas e rápidas para pareceres |
| **Auditores** | Fundamentação sólida para relatórios |
| **Consultorias** | Ferramenta diferenciada para clientes |
| **Órgãos Públicos** | Redução de riscos e melhor compliance |

## Melhorias Propostas

### 🔴 Prioridade Alta (Críticas)

#### 1. Implementar Testes Automatizados

**Problema:** Sem testes, não há garantia de qualidade

**Proposta:**
- **Testes Unitários** (rag_v1, rag_v2)
  ```python
  def test_consultar_base_rag():
      resposta = consultar_base_rag("Qual o limite de dispensa?")
      assert "50.000" in resposta or "cinquenta mil" in resposta.lower()
  ```

- **Testes de Integração** (pipeline completo)
  ```python
  def test_pipeline_completo():
      # Query → Retrieval → LLM → Response
      assert pipeline_funciona()
  ```

- **Testes de Regressão** (gold dataset)
  ```python
  # 50 perguntas com respostas esperadas
  # Comparar saída atual vs. esperada
  # Alertar se accuracy < 90%
  ```

**Estimativa:** 2-3 semanas
**Impacto:** 🔴 Crítico (reduz bugs, facilita refatoração)

#### 2. Adicionar Logging Estruturado

**Problema:** Sem logs, impossível debugar produção

**Proposta:**
```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Uso
logger.info("Query recebida", extra={
    "query": query,
    "user_id": user_id,
    "timestamp": time.time()
})

logger.info("Resposta gerada", extra={
    "query": query,
    "latency_ms": latency,
    "num_docs_retrieved": len(docs),
    "llm_tokens": tokens
})
```

**Campos importantes:**
- Query texto
- User ID
- Timestamp
- Latência
- Documentos recuperados
- Tokens usados (custo)
- Erros (se houver)

**Estimativa:** 1 semana
**Impacto:** 🔴 Crítico (visibilidade, debugging)

#### 3. Implementar Autenticação

**Problema:** Sistema aberto, sem controle de acesso

**Proposta (MVP):**
- **Autenticação básica** (usuário/senha)
- **Sessões isoladas** por usuário
- **Rate limiting** (ex: 100 queries/dia por usuário)

**Opções:**
- **Simples:** HTTP Basic Auth
- **Intermediário:** JWT tokens
- **Avançado:** OAuth 2.0 (Google, Microsoft)

**Implementação exemplo (FastAPI):**
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

users = {
    "ana.silva": "senha123",  # Usar hash em produção!
    "carlos.mendes": "senha456"
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username not in users:
        raise HTTPException(status_code=401)
    if users[credentials.username] != credentials.password:
        raise HTTPException(status_code=401)
    return credentials.username

@app.post("/query")
def query(text: str, user: str = Depends(authenticate)):
    # user está autenticado
    resposta = consultar_base_rag(text)
    return {"resposta": resposta}
```

**Estimativa:** 1-2 semanas
**Impacto:** 🔴 Crítico (segurança)

### 🟡 Prioridade Média (Importantes)

#### 4. Adicionar Cache de Respostas

**Problema:** Mesma pergunta = nova chamada ao LLM (caro e lento)

**Proposta:**
```python
import hashlib
import redis

# Conectar ao Redis
cache = redis.Redis(host='localhost', port=6379, db=0)

def consultar_base_rag_com_cache(pergunta: str) -> str:
    # Hash da pergunta
    query_hash = hashlib.md5(pergunta.encode()).hexdigest()

    # Verificar cache
    cached = cache.get(query_hash)
    if cached:
        logger.info("Cache hit", extra={"query_hash": query_hash})
        return cached.decode()

    # Cache miss, executar RAG
    resposta = _rag_answer(pergunta)

    # Salvar no cache (TTL: 24h)
    cache.setex(query_hash, 86400, resposta)

    return resposta
```

**Benefícios:**
- ⚡ Latência: ~5s → ~0.1s (50x mais rápido)
- 💰 Custo: $0.01/query → $0.00 (cache hit)

**Trade-off:**
- Infraestrutura adicional (Redis)
- Cache pode ficar stale (solução: TTL curto)

**Estimativa:** 1 semana
**Impacto:** 🟡 Médio (performance, custo)

#### 5. Expandir Base de Documentos

**Problema:** Apenas 4 leis, cobertura limitada

**Proposta:**

**Fase 1 - Leis Fundamentais** (prioritário):
- [ ] Lei 8.666/1993 (lei antiga de licitações)
- [ ] Lei 12.527/2011 (Lei de Acesso à Informação)
- [ ] Lei 12.846/2013 (Lei Anticorrupção)
- [ ] Decreto 9.507/2018 (Terceirização)

**Fase 2 - Instruções Normativas**:
- [ ] IN SEGES 01/2019 (Contratações de TI)
- [ ] IN SEGES 05/2017 (Gerenciamento de contratos)
- [ ] IN SLTI 01/2010 (Sustentabilidade)

**Fase 3 - Jurisprudência**:
- [ ] Súmulas do TCU
- [ ] Acórdãos relevantes do TCU
- [ ] Decisões do STF sobre licitações

**Processo:**
1. Coletar PDFs oficiais
2. Processar com `get_v1_data.ipynb`
3. Reindexar com `get_vectorial_bank_v1.ipynb`
4. Testar qualidade das respostas
5. Documentar no README

**Estimativa:** 1-2 semanas por fase
**Impacto:** 🟡 Alto (cobertura)

#### 6. Melhorar Tratamento de Erros

**Problema:** Erros não são tratados gracefully

**Proposta:**
```python
from functools import wraps
import traceback

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error("Validation error", extra={"error": str(e)})
            return {"error": "Pergunta inválida", "details": str(e)}
        except Exception as e:
            logger.error("Unexpected error", extra={
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return {"error": "Erro interno do servidor", "support_id": generate_support_id()}
    return wrapper

@handle_errors
def consultar_base_rag(pergunta: str) -> str:
    if not pergunta or len(pergunta) < 5:
        raise ValueError("Pergunta muito curta")

    # ... resto do código
```

**Mensagens amigáveis:**
- ❌ "Exception: object of type 'NoneType' has no len()"
- ✅ "Por favor, forneça uma pergunta com pelo menos 5 caracteres."

**Estimativa:** 1 semana
**Impacto:** 🟡 Médio (UX, manutenibilidade)

#### 7. Otimizar Performance

**Proposta:**

**A. Cache de Embeddings** (query repetidas)
```python
embedding_cache = {}

def embed_query_cached(query: str):
    if query in embedding_cache:
        return embedding_cache[query]

    embedding = modelo_embedding.embed_query(query)
    embedding_cache[query] = embedding
    return embedding
```

**B. Batch Processing** (múltiplas queries)
```python
def process_batch(queries: List[str]) -> List[str]:
    # Processar todas embeddings de uma vez
    embeddings = modelo_embedding.embed_documents(queries)

    # Buscar FAISS em paralelo
    results = [vector_db.similarity_search(emb, k=12) for emb in embeddings]

    # Invocar LLM em paralelo (async)
    respostas = await asyncio.gather(*[
        llm.ainvoke(prompt) for prompt in prompts
    ])

    return respostas
```

**C. GPU para Embeddings** (se disponível)
```python
# Usar faiss-gpu ao invés de faiss-cpu
pip uninstall faiss-cpu
pip install faiss-gpu

# Modelo de embeddings na GPU
modelo_embedding = HuggingFaceEmbeddings(
    model_name="...",
    model_kwargs={'device': 'cuda'}
)
```

**Ganhos esperados:**
- Cache embeddings: 20-30% mais rápido
- Batch: 2-3x throughput
- GPU: 5-10x mais rápido (embeddings)

**Estimativa:** 1-2 semanas
**Impacto:** 🟡 Médio (performance)

### 🟢 Prioridade Baixa (Nice to Have)

#### 8. Frontend Customizado

**Problema:** ADK Web é básico, pouco customizável

**Proposta:**
- **Framework:** React ou Streamlit
- **Features:**
  - Chat interface melhorada
  - Formatação de respostas (Markdown, highlight)
  - Histórico persistido (banco de dados)
  - Export de conversas (PDF, DOCX)
  - Feedback (👍/👎)
  - Analytics (dashboard de uso)

**Mockup (conceitual):**
```
┌──────────────────────────────────────────────┐
│ AMLDO - Assistente de Licitações            │
│ ┌──────────────────────────────────────────┐ │
│ │ 🔍 Pesquisar legislação...               │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│ ┌──────────────────────────────────────────┐ │
│ │ 👤 Você:                                 │ │
│ │ Qual o limite de dispensa para obras?    │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│ ┌──────────────────────────────────────────┐ │
│ │ 🤖 AMLDO:                                │ │
│ │ Segundo o **Art. 75, I da Lei 14.133**:  │ │
│ │ R$ 50.000,00                             │ │
│ │                                          │ │
│ │ [Ver fonte] [Copiar] [👍] [👎]          │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│ ┌──────────────────────────────────────────┐ │
│ │ Digite sua pergunta...         [Enviar] │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│ [Histórico] [Configurações] [Exportar]      │
└──────────────────────────────────────────────┘
```

**Estimativa:** 3-4 semanas
**Impacto:** 🟢 Médio (UX)

#### 9. Sistema de Feedback

**Proposta:**
- Botões 👍/👎 em cada resposta
- Campo de comentário opcional
- Armazenar em banco de dados
- Dashboard de analytics

**Uso:**
- Identificar perguntas com baixa satisfação
- Melhorar prompts/retrieval
- Monitorar qualidade ao longo do tempo

**Implementação:**
```python
# Banco de dados (SQLite)
import sqlite3

conn = sqlite3.connect('feedback.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY,
    query TEXT,
    response TEXT,
    rating INTEGER,  -- 1 (👍) ou -1 (👎)
    comment TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

def salvar_feedback(query, response, rating, comment=None):
    cursor.execute(
        'INSERT INTO feedback (query, response, rating, comment) VALUES (?, ?, ?, ?)',
        (query, response, rating, comment)
    )
    conn.commit()
```

**Estimativa:** 1 semana
**Impacto:** 🟢 Médio (dados para melhoria)

#### 10. Múltiplos Idiomas

**Proposta:**
- Interface em inglês
- Perguntas em inglês (busca mantém em PT)
- Respostas em inglês (tradução automática)

**Desafios:**
- Embeddings multilíngues já suportam inglês
- Mas documentos estão em português
- Tradução de respostas pode perder precisão legal

**Abordagem:**
1. Usuário pergunta em inglês
2. Sistema traduz para português (Google Translate API)
3. Busca no FAISS (em português)
4. LLM responde em português
5. Sistema traduz resposta para inglês

**Estimativa:** 2 semanas
**Impacto:** 🟢 Baixo (mercado internacional limitado)

## Roadmap

### Q1 2025 (Jan-Mar) - Fundações

**Objetivo:** Preparar para produção

- [x] ✅ Documentação completa (você está aqui!)
- [ ] 🔴 Implementar testes automatizados
- [ ] 🔴 Adicionar logging estruturado
- [ ] 🔴 Implementar autenticação básica
- [ ] 🟡 Adicionar 10 novos documentos (leis fundamentais)
- [ ] 🟡 Deploy em servidor (staging)

**Entregável:** Sistema testado e seguro em staging

### Q2 2025 (Abr-Jun) - Otimização

**Objetivo:** Melhorar performance e qualidade

- [ ] 🟡 Cache de respostas (Redis)
- [ ] 🟡 Otimizações de performance (GPU, batch)
- [ ] 🟡 Expandir documentos (instruções normativas)
- [ ] 🟢 Frontend customizado (MVP)
- [ ] 🟢 Sistema de feedback
- [ ] 🔴 Deploy em produção

**Entregável:** Sistema em produção com >100 usuários

### Q3 2025 (Jul-Set) - Expansão

**Objetivo:** Agregar novas fontes e funcionalidades

- [ ] 🟡 Jurisprudência (TCU, STF)
- [ ] 🟢 Analytics e dashboard
- [ ] 🟢 Export de conversas
- [ ] 🟡 API pública (para integrações)
- [ ] 🟡 Melhorias baseadas em feedback de usuários

**Entregável:** Plataforma completa com 50+ documentos

### Q4 2025 (Out-Dez) - Inteligência

**Objetivo:** Features avançadas de IA

- [ ] 💡 RAG multi-hop (perguntas complexas em múltiplas etapas)
- [ ] 💡 Summarização de documentos
- [ ] 💡 Comparação automática de leis (o que mudou?)
- [ ] 💡 Alertas de atualizações legais
- [ ] 💡 Fine-tuning de LLM específico do domínio

**Entregável:** Sistema inteligente com features diferenciadas

## Ideias Futuras

### 💡 Visão de Longo Prazo (2026+)

#### 1. AMLDO Mobile

**Conceito:** App iOS/Android para consultas em mobilidade

**Use Case:** Gestor em reunião precisa consultar lei rapidamente

#### 2. Integração com Sistemas de Licitação

**Conceito:** Plugin para sistemas como Comprasnet, Licita Já

**Fluxo:**
- Usuário editando edital no sistema
- Clica em "Consultar AMLDO"
- Pergunta sobre dúvida específica
- Recebe resposta sem sair do sistema

#### 3. Assistente Proativo

**Conceito:** Sistema analisa edital e sugere melhorias

**Fluxo:**
- Usuário faz upload de edital (PDF)
- AMLDO analisa e identifica:
  - Cláusulas que podem violar a lei
  - Prazos incorretos
  - Requisitos faltantes
- Sugere correções com fundamentação legal

#### 4. RAG Multi-Modal

**Conceito:** Incluir imagens, gráficos, fluxogramas

**Exemplo:**
- Usuário pergunta: "Como é o fluxo de pregão eletrônico?"
- Sistema retorna: Texto + Fluxograma visual

#### 5. Comunidade e Crowdsourcing

**Conceito:** Usuários podem:
- Sugerir novos documentos
- Avaliar qualidade de respostas
- Adicionar comentários/anotações
- Compartilhar interpretações

#### 6. AMLDO Tutor (E-learning)

**Conceito:** Modo de ensino interativo

**Fluxo:**
- Usuário: "Quero aprender sobre pregão eletrônico"
- AMLDO: "Ótimo! Vamos começar pelo básico. O que é um pregão?"
- Usuário responde
- AMLDO valida e explica
- Quizzes e exercícios práticos

## Critérios de Priorização

### Framework: RICE Score

Cada feature é avaliada em 4 dimensões:

**R - Reach (Alcance)**: Quantos usuários impacta?
- 1 = <10%, 2 = 10-50%, 3 = >50%

**I - Impact (Impacto)**: Qual o valor gerado?
- 1 = baixo, 2 = médio, 3 = alto

**C - Confidence (Confiança)**: Quão certos estamos?
- 1 = <50%, 2 = 50-80%, 3 = >80%

**E - Effort (Esforço)**: Quanto tempo/recursos?
- 1 = <1 semana, 2 = 1-4 semanas, 3 = >1 mês

**Score = (R × I × C) / E**

Quanto maior o score, maior a prioridade.

### Exemplos de Score:

| Feature | R | I | C | E | Score | Prioridade |
|---------|---|---|---|---|-------|------------|
| Testes automatizados | 3 | 3 | 3 | 2 | **13.5** | 🔴 Alta |
| Logging estruturado | 3 | 3 | 3 | 1 | **27** | 🔴 Alta |
| Autenticação | 3 | 3 | 3 | 2 | **13.5** | 🔴 Alta |
| Cache de respostas | 2 | 2 | 3 | 1 | **12** | 🟡 Média |
| Expandir docs | 3 | 3 | 3 | 2 | **13.5** | 🟡 Média |
| Frontend custom | 2 | 2 | 2 | 3 | **2.7** | 🟢 Baixa |
| Múltiplos idiomas | 1 | 1 | 2 | 2 | **1** | 🟢 Baixa |

---

**Conclusão:** Documentação completa! 🎉

**Próximo:** [Voltar ao Índice](README.md)
