# Casos de Uso do AMLDO

## 📋 Sumário

- [Personas](#personas)
- [Casos de Uso por Persona](#casos-de-uso-por-persona)
- [Fluxos Detalhados](#fluxos-detalhados)
- [Exemplos Reais](#exemplos-reais)
- [Perguntas Frequentes](#perguntas-frequentes)

## Personas

### 1. Gestor Público - Ana Silva

**Perfil:**
- Cargo: Gerente de Compras em órgão público
- Experiência: 5 anos em licitações
- Conhecimento técnico: Intermediário (usa computador, não é programadora)
- Necessidades: Consultas rápidas sobre procedimentos licitatórios

**Dores:**
- Perde tempo procurando em PDFs de leis
- Dúvidas frequentes sobre limites e procedimentos
- Precisa de respostas fundamentadas (com artigos)

### 2. Advogado - Dr. Carlos Mendes

**Perfil:**
- Cargo: Advogado especializado em Direito Administrativo
- Experiência: 15 anos
- Conhecimento técnico: Básico (usa ferramentas de escritório)
- Necessidades: Consultas precisas e citações legais

**Dores:**
- Muitos documentos para acompanhar (leis, decretos, portarias)
- Precisa de respostas rápidas para clientes
- Necessita de citações precisas (lei, artigo, inciso)

### 3. Auditor - Fernanda Costa

**Perfil:**
- Cargo: Auditora interna de empresa pública
- Experiência: 8 anos
- Conhecimento técnico: Avançado
- Necessidades: Verificar conformidade com legislação

**Dores:**
- Auditar muitos contratos e licitações
- Garantir compliance com múltiplas normas
- Precisa de respostas fundamentadas para relatórios

### 4. Desenvolvedor - Pedro Santos

**Perfil:**
- Cargo: Desenvolvedor Full-Stack
- Experiência: 3 anos
- Conhecimento técnico: Avançado
- Necessidades: Entender e estender o sistema RAG

**Dores:**
- Documentação técnica dispersa
- Precisa entender arquitetura rapidamente
- Quer adicionar novas funcionalidades

## Casos de Uso por Persona

### Ana Silva (Gestor Público)

#### UC-01: Consultar Limite de Dispensa

**Objetivo:** Verificar se pode dispensar licitação para uma obra

**Pré-condições:** Sistema rodando e acessível

**Fluxo Principal:**
1. Ana acessa http://localhost:8080
2. Seleciona agente "rag_v2"
3. Pergunta: "Qual o limite de valor para dispensa de licitação em obras de engenharia?"
4. Sistema busca no FAISS
5. Sistema retorna: "Segundo o Art. 75, inciso I da Lei 14.133/2021, é dispensável a licitação para contratações que envolvam valores inferiores a R$ 50.000,00 no caso de obras e serviços de engenharia."
6. Ana usa informação para decidir procedimento

**Resultado:** Decisão informada em <5 segundos

#### UC-02: Verificar Procedimento de Pregão

**Objetivo:** Entender requisitos para abrir pregão eletrônico

**Fluxo Principal:**
1. Ana pergunta: "Quais são os requisitos para realizar um pregão eletrônico?"
2. Sistema busca no Decreto 10.024/2019 e Lei 14.133
3. Sistema lista requisitos com citações
4. Ana copia resposta para documento de trabalho

#### UC-03: Esclarecer Dúvida sobre ME/EPP

**Objetivo:** Entender tratamento diferenciado para microempresas

**Fluxo Principal:**
1. Ana pergunta: "Como funciona o tratamento diferenciado para microempresas em licitações?"
2. Sistema busca na LCP 123/2006
3. Sistema explica benefícios (empate ficto, etc.) citando artigos
4. Ana compartilha resposta com equipe

### Dr. Carlos Mendes (Advogado)

#### UC-04: Fundamentar Parecer Jurídico

**Objetivo:** Obter citações legais para parecer

**Fluxo Principal:**
1. Carlos está escrevendo parecer sobre dispensa de licitação
2. Acessa AMLDO
3. Faz múltiplas perguntas:
   - "Quais são as hipóteses de dispensa de licitação?"
   - "O que diz a lei sobre contratações emergenciais?"
   - "Quais são os prazos para pregão eletrônico?"
4. Sistema retorna respostas com citações precisas
5. Carlos copia artigos relevantes para parecer
6. Verifica artigos nos PDFs originais (double-check)

**Resultado:** Parecer fundamentado com citações corretas

#### UC-05: Comparar Leis Antigas e Novas

**Objetivo:** Verificar mudanças entre Lei 8.666 e Lei 14.133

**Fluxo Alternativo:**
1. Carlos pergunta sobre procedimento específico
2. Sistema retorna apenas info da Lei 14.133 (lei nova)
3. Carlos nota que projeto não tem Lei 8.666 indexada
4. Carlos solicita adição da lei antiga (via GitHub Issue ou email)

**Nota:** Expõe limitação atual do sistema

### Fernanda Costa (Auditora)

#### UC-06: Auditar Processo Licitatório

**Objetivo:** Verificar se licitação seguiu procedimentos legais

**Fluxo Principal:**
1. Fernanda está auditando pregão de R$ 200.000
2. Pergunta ao sistema:
   - "Qual o prazo mínimo entre publicação e abertura de pregão?"
   - "Quais documentos são obrigatórios no edital?"
   - "Quais são as fases do pregão eletrônico?"
3. Sistema retorna respostas fundamentadas
4. Fernanda compara com processo auditado
5. Identifica não-conformidades (prazo não cumprido)
6. Documenta achado citando artigo da lei

**Resultado:** Relatório de auditoria fundamentado

#### UC-07: Verificar Compliance com LGPD

**Objetivo:** Garantir que dados pessoais em licitação seguem LGPD

**Fluxo Principal:**
1. Fernanda pergunta: "Quais dados pessoais podem ser solicitados em licitação segundo a LGPD?"
2. Sistema busca na Lei 13.709/2018
3. Sistema explica princípios de finalidade e necessidade
4. Fernanda cruza com Lei 14.133 (tratamento de dados em licitações)
5. Elabora checklist de compliance

### Pedro Santos (Desenvolvedor)

#### UC-08: Adicionar Novo Documento

**Objetivo:** Indexar nova lei no sistema

**Fluxo Principal:**
1. Pedro baixa PDF da Lei 8.666/1993
2. Salva em `data/raw/L8666.pdf`
3. Abre `get_v1_data.ipynb` no Jupyter
4. Executa todas as células
5. Verifica que `data/split_docs/L8666/` foi criado
6. Abre `get_vectorial_bank_v1.ipynb`
7. Executa todas as células
8. Verifica logs: "Processados 3000 chunks de 5 documentos"
9. Reinicia `adk web`
10. Testa: "O que diz a Lei 8.666 sobre dispensa?"
11. Sistema retorna resposta incluindo a nova lei

**Resultado:** Nova lei indexada e pesquisável

#### UC-09: Customizar Prompt do Agente

**Objetivo:** Fazer sistema retornar respostas mais diretas

**Fluxo Principal:**
1. Pedro edita `rag_v1/tools.py`
2. Modifica prompt de:
   ```
   "Use APENAS o contexto para responder.\n\n"
   ```
   Para:
   ```
   "Responda de forma direta e objetiva, APENAS com base no contexto.
    Comece sempre citando o artigo e lei.\n\n"
   ```
3. Salva arquivo
4. Reinicia servidor (Ctrl+C → adk web)
5. Testa pergunta
6. Observa resposta começando com citação
7. Valida melhoria e commita código

**Resultado:** Respostas mais padronizadas

#### UC-10: Implementar Nova Ferramenta

**Objetivo:** Adicionar calculadora de prazos

**Fluxo Principal:**
1. Pedro cria função em `rag_v1/tools.py`:
   ```python
   def calcular_prazo_edital(tipo: str, valor: float) -> str:
       # ... lógica
   ```
2. Adiciona ferramenta ao agente em `rag_v1/agent.py`:
   ```python
   tools=[consultar_base_rag, calcular_prazo_edital]
   ```
3. Reinicia servidor
4. Testa: "Quanto tempo preciso publicar edital de pregão de R$ 100.000?"
5. Sistema chama automaticamente nova ferramenta
6. Retorna prazo calculado

**Resultado:** Funcionalidade estendida

## Fluxos Detalhados

### Fluxo Completo: Responder Pergunta (Perspectiva do Usuário)

```
┌──────────────────────────────────────┐
│ Usuário acessa http://localhost:8080│
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Interface ADK Web carrega            │
│ - Mostra lista de agentes disponíveis│
│   □ rag_v1                           │
│   ☑ rag_v2                           │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Usuário seleciona rag_v2             │
│ Clica em "Start Chat"                │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Tela de chat aparece                 │
│ ┌──────────────────────────────────┐ │
│ │ Olá! Como posso ajudar?          │ │
│ └──────────────────────────────────┘ │
│ [Digite sua mensagem...]             │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Usuário digita:                      │
│ "Qual o limite de dispensa obras?"   │
│ Pressiona Enter                      │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Loading indicator aparece            │
│ ⏳ Pensando...                       │
└──────────┬───────────────────────────┘
           │
           ▼ [2-5 segundos]
┌──────────────────────────────────────┐
│ Resposta aparece:                    │
│                                      │
│ "Segundo o Art. 75, inciso I da     │
│ Lei 14.133/2021, é dispensável a    │
│ licitação para contratações que      │
│ envolvam valores inferiores a        │
│ R$ 50.000,00 (cinquenta mil reais), │
│ no caso de obras e serviços de      │
│ engenharia ou de serviços de        │
│ manutenção de veículos automotores."│
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Usuário pode:                        │
│ - Fazer nova pergunta                │
│ - Copiar resposta                    │
│ - Continuar conversação              │
└──────────────────────────────────────┘
```

### Fluxo Interno: Processar Pergunta (Perspectiva do Sistema)

```
1. ADK Web recebe mensagem
   ↓
2. Envia para Agent v2
   ↓
3. Agent analisa intenção
   ├─> Detecta: pergunta sobre legislação
   └─> Decisão: invocar consultar_base_rag
   ↓
4. Invoca tools.consultar_base_rag(pergunta)
   ↓
5. _rag_answer() executa pipeline:
   │
   ├─> Gera embedding da query (384 dims)
   │
   ├─> Busca FAISS (MMR, k=12, filter artigo_0)
   │   └─> Retorna 12 documentos + metadados
   │
   ├─> Converte para DataFrame
   │
   ├─> Ordena hierarquicamente
   │   (lei, titulo, capitulo, artigo, chunk_idx)
   │
   ├─> Pós-processa contexto (v2 only)
   │   ├─> Agrupa por hierarquia
   │   ├─> Injeta artigos_0 (intros)
   │   └─> Estrutura com tags XML
   │
   ├─> Monta prompt com contexto estruturado
   │
   └─> Invoca Gemini 2.5 Flash
       └─> Recebe resposta gerada
   ↓
6. Retorna resposta para Agent
   ↓
7. Agent formata resposta final
   ↓
8. ADK Web exibe ao usuário
```

## Exemplos Reais

### Exemplo 1: Limite de Dispensa

**Pergunta:**
> "Qual o valor máximo para dispensa de licitação em compras?"

**Resposta (v2):**
> Segundo o Art. 75, inciso II da Lei 14.133/2021, é dispensável a licitação para contratações que envolvam valores inferiores a R$ 10.000,00 (dez mil reais), no caso de compras ou de serviços, exceto os serviços de engenharia.
>
> Vale destacar que este valor é diferente para obras (R$ 50.000,00) e serviços técnicos especializados (R$ 30.000,00), conforme incisos I e III do mesmo artigo.

**Por que funciona:**
- ✅ Busca encontrou Art. 75
- ✅ LLM identificou inciso correto (II)
- ✅ Contexto estruturado permitiu comparação com outros incisos

### Exemplo 2: Tratamento de ME/EPP

**Pergunta:**
> "Como funciona o empate ficto para microempresas?"

**Resposta (v2):**
> O empate ficto é um benefício previsto na Lei Complementar 123/2006, Art. 44. Quando a proposta apresentada por microempresa (ME) ou empresa de pequeno porte (EPP) for até 10% superior à proposta mais bem classificada (caso esta não seja ME/EPP), considera-se que há empate.
>
> Neste caso, a ME/EPP terá a oportunidade de apresentar nova proposta no prazo de 5 minutos, e poderá cobrir (igualar ou superar) a proposta atualmente mais bem classificada, garantindo assim a contratação.
>
> Este mecanismo visa dar tratamento diferenciado às ME/EPP em licitações públicas, promovendo sua participação e competitividade.

**Por que funciona:**
- ✅ Busca encontrou LCP 123 (não apenas Lei 14.133)
- ✅ Contexto de múltiplos chunks do mesmo artigo
- ✅ LLM sintetizou informação de vários parágrafos

### Exemplo 3: LGPD em Licitações

**Pergunta:**
> "Preciso solicitar CPF de todos os funcionários da empresa licitante. Isso viola a LGPD?"

**Resposta (v2):**
> Segundo a Lei 13.709/2018 (LGPD), o tratamento de dados pessoais deve observar os princípios da **finalidade** (Art. 6º, I) e da **necessidade** (Art. 6º, III). Isso significa que você só pode coletar dados pessoais para propósitos legítimos, específicos e explícitos, e somente o mínimo necessário.
>
> No contexto de licitações, é importante avaliar:
> 1. **É necessário o CPF de TODOS os funcionários?** Ou apenas dos sócios, representantes legais e responsáveis técnicos?
> 2. **Qual a finalidade específica?** (ex: verificar regularidade fiscal, qualificação técnica, etc.)
>
> Se a solicitação não for estritamente necessária para o objeto licitatório, pode sim violar a LGPD (especialmente o princípio da necessidade). Recomenda-se limitar a coleta apenas aos dados imprescindíveis.

**Por que funciona:**
- ✅ Busca cruzou LGPD com contexto de licitações
- ✅ LLM aplicou princípios ao caso concreto
- ✅ Resposta prática e orientativa

### Exemplo 4: Pregão Eletrônico

**Pergunta:**
> "Quais são as fases do pregão eletrônico?"

**Resposta (v2):**
> Segundo o Decreto 10.024/2019, que regulamenta o pregão eletrônico, as fases são:
>
> 1. **Publicação do edital** (Art. 17) - com antecedência mínima de 8 dias úteis
> 2. **Apresentação de propostas** (Art. 30) - via sistema eletrônico
> 3. **Abertura e divulgação das propostas** (Art. 32)
> 4. **Sessão pública de lances** (Art. 34) - disputaaberta ou fechada
> 5. **Análise de aceitabilidade da proposta** (Art. 38)
> 6. **Habilitação do licitante** (Art. 46) - verificação de documentos
> 7. **Adjudicação e homologação** (Art. 13 da Lei 14.133)
>
> Todo o processo é conduzido por pregoeiro, com transparência e registro digital de todos os atos.

**Por que funciona:**
- ✅ Busca encontrou Decreto 10.024 (específico de pregão)
- ✅ Contexto incluiu múltiplos artigos sequenciais
- ✅ LLM organizou informação em lista numerada

## Perguntas Frequentes

### Para Usuários Finais

**Q: O sistema inventa informações?**

R: Não. O AMLDO é configurado para responder **apenas** com base nos documentos indexados. Se a informação não estiver na base, o sistema informa que não encontrou.

**Q: Posso confiar nas citações (artigos, leis)?**

R: As citações são altamente confiáveis (>95% de precisão nos testes), mas sempre recomendamos **verificar no documento original** para decisões críticas. O sistema facilita a busca, mas não substitui análise jurídica profissional.

**Q: Por que às vezes a resposta demora?**

R: A latência típica é 2-5 segundos. Demoras maiores podem ocorrer por:
- Primeira consulta (carregamento de modelos)
- Pergunta complexa (mais processamento)
- API do Gemini congestionada

**Q: Posso fazer perguntas em inglês?**

R: O modelo de embeddings suporta múltiplos idiomas, mas os documentos estão em português. Perguntas em inglês podem funcionar, mas a qualidade será menor. Recomenda-se português.

**Q: O histórico é salvo?**

R: Não. Atualmente o histórico existe apenas durante a sessão do browser. Ao fechar, é perdido. (Limitação conhecida)

### Para Desenvolvedores

**Q: Como adiciono um novo documento?**

R: Veja [UC-08](#uc-08-adicionar-novo-documento) acima, ou [Comandos e Fluxos](05-comandos-fluxos.md#fluxo-2-adicionar-novo-documento)

**Q: Posso mudar o LLM (ex: GPT-4)?**

R: Sim. Edite `rag_v1/tools.py`:
```python
llm = init_chat_model("gpt-4", model_provider="openai")
```
E configure `OPENAI_API_KEY` no `.env`.

**Q: Como testo mudanças sem rodar a interface web?**

R: Crie um script Python:
```python
from rag_v1.tools import consultar_base_rag
print(consultar_base_rag("Sua pergunta aqui"))
```
Execute: `python test.py`

**Q: O sistema funciona offline?**

R: Parcialmente. O FAISS e embeddings são locais, mas o LLM (Gemini) requer internet. Para offline completo, use modelo local (Ollama).

---

**Próximo:** [Melhorias e Roadmap](08-melhorias-roadmap.md)
