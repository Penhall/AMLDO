# Documentação do AMLDO

## 📚 Bem-vindo à Documentação Completa

Esta é a documentação técnica completa do **AMLDO** - Sistema RAG especializado em legislação brasileira de licitações, compliance e governança.

## 🗺️ Guia de Navegação

### Para Começar

👉 **Novo no projeto?** Comece por aqui:

1. **[Visão Geral](00-visao-geral.md)** - Entenda o que é o AMLDO, objetivos e contexto
2. **[Guia do Desenvolvedor](04-guia-desenvolvedor.md)** - Setup do ambiente e primeiros passos
3. **[Casos de Uso](07-casos-de-uso.md)** - Exemplos práticos de utilização

### Documentação Técnica

📖 **Quer entender a fundo?** Explore a arquitetura:

- **[Arquitetura Técnica](01-arquitetura-tecnica.md)** - Componentes, camadas e decisões arquiteturais
- **[Pipeline RAG](02-pipeline-rag.md)** - Como funciona o RAG internamente (v1 e v2)
- **[Estrutura de Dados](03-estrutura-dados.md)** - Organização de dados e metadados

### Guias Práticos

🛠️ **Precisa fazer algo específico?**

- **[Comandos e Fluxos](05-comandos-fluxos.md)** - Comandos úteis e fluxos de trabalho
- **[Estado Atual](06-estado-atual.md)** - O que funciona, limitações e métricas
- **[Melhorias e Roadmap](08-melhorias-roadmap.md)** - Próximos passos e visão de futuro

## 📖 Índice Completo

### 00. [Visão Geral do Projeto](00-visao-geral.md)

**O que você vai encontrar:**
- Introdução ao AMLDO
- Objetivo e contexto de negócio
- Principais funcionalidades
- Tecnologias utilizadas
- Estrutura do projeto

**Ideal para:** Todos (iniciantes e avançados)

**Tempo de leitura:** ~10 minutos

---

### 01. [Arquitetura Técnica](01-arquitetura-tecnica.md)

**O que você vai encontrar:**
- Visão arquitetural (camadas)
- Componentes principais (agentes, ferramentas, RAG)
- Fluxo de dados completo
- Decisões arquiteturais justificadas
- Diagramas de arquitetura

**Ideal para:** Desenvolvedores, arquitetos

**Tempo de leitura:** ~20 minutos

---

### 02. [Pipeline RAG Detalhado](02-pipeline-rag.md)

**O que você vai encontrar:**
- Introdução ao RAG (Retrieval-Augmented Generation)
- Pipeline v1 (básico) passo a passo
- Pipeline v2 (aprimorado) com pós-processamento
- Embeddings e similaridade
- Estratégias de busca (Similarity vs MMR)
- Construção de prompts
- Otimizações e tuning

**Ideal para:** Desenvolvedores, data scientists

**Tempo de leitura:** ~25 minutos

---

### 03. [Estrutura de Dados](03-estrutura-dados.md)

**O que você vai encontrar:**
- Estrutura de diretórios completa
- Documentos brutos (raw/)
- Documentos divididos (split_docs/)
- Dados processados (processed/)
- Banco vetorial FAISS (vector_db/)
- Formato de metadados
- Fluxo de transformação de dados
- Estatísticas dos dados

**Ideal para:** Desenvolvedores, data engineers

**Tempo de leitura:** ~15 minutos

---

### 04. [Guia do Desenvolvedor](04-guia-desenvolvedor.md)

**O que você vai encontrar:**
- Setup completo do ambiente (passo a passo)
- Primeiros passos (rodar sistema, testar)
- Estrutura do código
- Pontos de extensão (adicionar features)
- Desenvolvimento local (workflow, hot reload)
- Debugging e testes
- Boas práticas de desenvolvimento
- Troubleshooting (erros comuns e soluções)

**Ideal para:** Novos desenvolvedores no projeto

**Tempo de leitura:** ~30 minutos

---

### 05. [Comandos e Fluxos](05-comandos-fluxos.md)

**O que você vai encontrar:**
- Comandos principais (venv, pip, adk, jupyter)
- Fluxos de execução (primeiro uso, adicionar doc, modificar código)
- Notebooks de processamento detalhados
- Operações de manutenção (backup, reindexar, limpar cache)
- Scripts úteis (verificação, testes, benchmark)

**Ideal para:** Desenvolvedores, DevOps

**Tempo de leitura:** ~20 minutos

---

### 06. [Estado Atual do Sistema](06-estado-atual.md)

**O que você vai encontrar:**
- Status do projeto (o que está funcionando)
- Funcionalidades implementadas
- Limitações conhecidas (críticas, importantes, menores)
- Métricas de qualidade (performance, precisão)
- Pendências e TODOs priorizados
- Histórico de versões

**Ideal para:** Gestores de produto, desenvolvedores

**Tempo de leitura:** ~15 minutos

---

### 07. [Casos de Uso](07-casos-de-uso.md)

**O que você vai encontrar:**
- Personas (gestor público, advogado, auditor, desenvolvedor)
- Casos de uso detalhados para cada persona
- Fluxos de interação (usuário e sistema)
- Exemplos reais de perguntas e respostas
- Perguntas frequentes (FAQs)

**Ideal para:** Todos (entender valor e aplicabilidade)

**Tempo de leitura:** ~25 minutos

---

### 08. [Melhorias e Roadmap](08-melhorias-roadmap.md)

**O que você vai encontrar:**
- Visão de produto (onde estamos → onde queremos chegar)
- Melhorias propostas (alta, média, baixa prioridade)
- Roadmap trimestral (Q1-Q4 2025)
- Ideias futuras (visão de longo prazo)
- Critérios de priorização (framework RICE)

**Ideal para:** Gestores de produto, stakeholders

**Tempo de leitura:** ~20 minutos

---

## 🎯 Guias Rápidos

### Quero...

**...rodar o sistema pela primeira vez**
→ [Guia do Desenvolvedor - Setup](04-guia-desenvolvedor.md#setup-do-ambiente)

**...adicionar um novo documento PDF**
→ [Comandos e Fluxos - Adicionar Documento](05-comandos-fluxos.md#fluxo-2-adicionar-novo-documento)

**...entender como funciona o RAG**
→ [Pipeline RAG](02-pipeline-rag.md)

**...modificar o prompt do agente**
→ [Guia do Desenvolvedor - Customizar Prompt](04-guia-desenvolvedor.md#3-customizar-prompt)

**...saber quais são as limitações atuais**
→ [Estado Atual - Limitações](06-estado-atual.md#limitações-conhecidas)

**...ver exemplos de perguntas e respostas**
→ [Casos de Uso - Exemplos Reais](07-casos-de-uso.md#exemplos-reais)

**...contribuir com o projeto**
→ [Melhorias e Roadmap](08-melhorias-roadmap.md)

## 📊 Resumo Executivo

### O que é o AMLDO?

Sistema RAG (Retrieval-Augmented Generation) especializado em legislação brasileira de licitações, compliance e governança. Permite consultas em linguagem natural com respostas fundamentadas em documentos legais indexados.

### Tecnologias Principais

- **Python 3.11** + LangChain
- **FAISS** (banco vetorial)
- **Sentence Transformers** (embeddings multilíngues)
- **Gemini 2.5 Flash** (LLM)
- **Google ADK** (framework de agentes)

### Status

✅ **Funcional** em desenvolvimento
⚠️ **Não pronto** para produção (faltam testes, auth, monitoring)

### Cobertura Atual

4 documentos legais (~445 artigos, ~4000 chunks):
- Lei 14.133/2021 (Licitações)
- Lei 13.709/2018 (LGPD)
- LCP 123/2006 (ME/EPP)
- Decreto 10.024/2019 (Pregão Eletrônico)

### Performance

- ⚡ Latência: 2-5 segundos
- 📊 Precisão: >90% (avaliação subjetiva)
- 🎯 Sem alucinações (respostas fundamentadas)

## 🤝 Como Contribuir

Veja oportunidades de contribuição em:
- **[Estado Atual - Pendências](06-estado-atual.md#pendências-e-todos)**
- **[Melhorias e Roadmap](08-melhorias-roadmap.md#melhorias-propostas)**

## 📝 Notas de Versão

**Versão da Documentação:** 1.0
**Última Atualização:** 2025-10-30
**Autores:** Equipe AMLDO + Claude Code

## 🔗 Links Úteis

- **CLAUDE.md** - [Guia para desenvolvimento com Claude Code](../CLAUDE.md)
- **README.md** - [Setup rápido do ambiente](../README.md)
- **requirements.txt** - [Dependências do projeto](../requirements.txt)

---

## 📖 Convenções desta Documentação

### Ícones

- 🔴 Prioridade Alta / Crítico
- 🟡 Prioridade Média / Importante
- 🟢 Prioridade Baixa / Nice to Have
- ✅ Implementado / Funcionando
- ⚠️ Limitação / Atenção
- ❌ Não Implementado
- 💡 Ideia Futura
- 🎯 Objetivo / Meta
- ⚡ Performance
- 🔒 Segurança
- 📊 Métricas / Dados

### Formatação de Código

**Python:**
```python
def exemplo():
    pass
```

**Bash/Shell:**
```bash
comando --opcao
```

**Estrutura de Arquivos:**
```
diretorio/
├── arquivo1.py
└── arquivo2.txt
```

### Referências Internas

Links entre documentos usam formato Markdown relativo:
```markdown
[Texto do Link](arquivo.md#seção)
```

---

**Boa leitura e bom desenvolvimento! 🚀**

Se encontrar erros ou tiver sugestões de melhoria para esta documentação, abra uma issue no repositório.
