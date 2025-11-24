# PRD - Product Requirements Document
## LicitaFit - Sistema de Análise de Aderência a Editais

**Versão:** 1.0
**Data:** Novembro/2024
**Status:** Draft

---

## 1. Visão do Produto

### 1.1 Declaração de Visão

> **LicitaFit** é uma aplicação desktop que permite a empresas licitantes analisar automaticamente sua aderência a editais de licitação, identificando gaps, gerando relatórios de conformidade e auxiliando na tomada de decisão sobre participação em processos licitatórios.

### 1.2 Problema a Resolver

Empresas que participam de licitações enfrentam os seguintes desafios:

1. **Análise Manual de Editais**: Editais extensos (50-200 páginas) requerem horas de leitura
2. **Identificação de Requisitos**: Requisitos estão dispersos em múltiplas seções
3. **Verificação de Aderência**: Comparar requisitos com capacidades da empresa é trabalhoso
4. **Gestão de Documentos**: Certidões, atestados e declarações têm prazos de validade
5. **Decisão de Participação**: Avaliar se vale a pena participar é subjetivo

### 1.3 Solução Proposta

Sistema desktop que:
- Extrai requisitos automaticamente de editais em PDF
- Cadastra e organiza o perfil/capacidades da empresa
- Calcula score de aderência automaticamente
- Identifica gaps e sugere ações
- Gera relatórios executivos para decisão

---

## 2. Objetivos e Métricas de Sucesso

### 2.1 Objetivos de Negócio

| Objetivo | Descrição | Meta |
|----------|-----------|------|
| OBJ-01 | Reduzir tempo de análise de editais | 80% de redução |
| OBJ-02 | Aumentar taxa de assertividade em licitações | +30% em aprovação |
| OBJ-03 | Minimizar desistências por falta de documentação | -50% de desistências |
| OBJ-04 | Democratizar acesso a análise profissional | Custo acessível |

### 2.2 KPIs (Key Performance Indicators)

| KPI | Métrica | Target |
|-----|---------|--------|
| Tempo médio de análise | Minutos por edital | < 15 min |
| Precisão de extração | % requisitos identificados | > 90% |
| Score de aderência | Correlação com resultado real | > 85% |
| Satisfação do usuário | NPS | > 50 |
| Adoção | Usuários ativos mensais | +20% MoM |

### 2.3 Critérios de Sucesso MVP

1. Extração automática de pelo menos 80% dos requisitos de editais padrão
2. Cálculo de score de aderência com margem de erro < 15%
3. Tempo de análise completa < 10 minutos por edital
4. Interface intuitiva sem necessidade de treinamento
5. Funcionamento 100% offline após instalação

---

## 3. Público-Alvo

### 3.1 Personas Principais

#### Persona 1: Gestor de Licitações (Maria)

```
Nome: Maria Silva
Cargo: Gerente de Licitações
Empresa: Empresa de médio porte (50-200 funcionários)
Experiência: 8 anos em licitações

Desafios:
- Analisa 10-20 editais por mês
- Equipe pequena (2-3 pessoas)
- Precisa priorizar quais editais disputar
- Perde tempo com editais incompatíveis

Necessidades:
- Ferramenta que acelere triagem inicial
- Relatórios para apresentar à diretoria
- Gestão centralizada de documentos

Comportamento:
- Prefere ferramentas desktop (segurança de dados)
- Avessa a sistemas complexos
- Valoriza suporte técnico local
```

#### Persona 2: Analista de Licitações (Carlos)

```
Nome: Carlos Santos
Cargo: Analista de Licitações
Empresa: Microempresa (< 10 funcionários)
Experiência: 3 anos em licitações

Desafios:
- Trabalha sozinho
- Não tem tempo para análise detalhada
- Já perdeu licitações por documentação faltante
- Dificuldade em interpretar requisitos legais

Necessidades:
- Ferramenta simples e direta
- Checklist de documentos
- Alertas de validade de certidões
- Preço acessível

Comportamento:
- Usa planilhas Excel atualmente
- Busca tutoriais no YouTube
- Participa de grupos de WhatsApp sobre licitações
```

#### Persona 3: Consultor de Licitações (Roberto)

```
Nome: Roberto Mendes
Cargo: Consultor Autônomo
Empresa: Autônomo
Experiência: 15 anos em licitações

Desafios:
- Atende múltiplos clientes
- Cada cliente tem perfil diferente
- Precisa gerar relatórios profissionais
- Tempo é dinheiro

Necessidades:
- Gestão de múltiplos perfis de empresa
- Relatórios customizáveis com logo do cliente
- Histórico de análises
- Licença que permita uso comercial

Comportamento:
- Early adopter de tecnologia
- Disposto a pagar por ferramentas que agregam valor
- Influenciador em sua rede de contatos
```

### 3.2 Segmentação de Mercado

| Segmento | Tamanho Empresa | Volume Licitações | Disposição de Pagar |
|----------|-----------------|-------------------|---------------------|
| Micro | 1-10 func. | 1-5/mês | R$ 50-100/mês |
| Pequena | 11-50 func. | 5-15/mês | R$ 100-300/mês |
| Média | 51-200 func. | 15-50/mês | R$ 300-800/mês |
| Consultor | 1 pessoa | 10-30/mês | R$ 200-500/mês |

---

## 4. Escopo do Produto

### 4.1 Funcionalidades Incluídas (In Scope)

#### Módulo 1: Gestão de Perfil da Empresa

| ID | Funcionalidade | Prioridade | MVP |
|----|----------------|------------|-----|
| F1.1 | Cadastro de dados da empresa | Alta | Sim |
| F1.2 | Cadastro de capacidades técnicas | Alta | Sim |
| F1.3 | Cadastro de certificações/atestados | Alta | Sim |
| F1.4 | Upload de documentos digitalizados | Alta | Sim |
| F1.5 | Controle de validade de documentos | Alta | Sim |
| F1.6 | Alertas de vencimento | Média | Sim |
| F1.7 | Histórico de participações | Média | Não |
| F1.8 | Multi-empresa (consultores) | Baixa | Não |

#### Módulo 2: Análise de Editais

| ID | Funcionalidade | Prioridade | MVP |
|----|----------------|------------|-----|
| F2.1 | Upload de edital (PDF) | Alta | Sim |
| F2.2 | Extração automática de texto | Alta | Sim |
| F2.3 | Identificação de requisitos via RAG | Alta | Sim |
| F2.4 | Categorização de requisitos | Alta | Sim |
| F2.5 | Marcação obrigatório/desejável | Alta | Sim |
| F2.6 | Edição manual de requisitos | Média | Sim |
| F2.7 | Importação de editais de portais | Baixa | Não |
| F2.8 | OCR para editais escaneados | Baixa | Não |

#### Módulo 3: Análise de Aderência

| ID | Funcionalidade | Prioridade | MVP |
|----|----------------|------------|-----|
| F3.1 | Comparação perfil x requisitos | Alta | Sim |
| F3.2 | Score de aderência global | Alta | Sim |
| F3.3 | Score por categoria de requisito | Alta | Sim |
| F3.4 | Identificação de gaps | Alta | Sim |
| F3.5 | Recomendações de ação | Média | Sim |
| F3.6 | Estimativa de custo de adequação | Baixa | Não |
| F3.7 | Comparação entre editais | Baixa | Não |

#### Módulo 4: Relatórios

| ID | Funcionalidade | Prioridade | MVP |
|----|----------------|------------|-----|
| F4.1 | Relatório de aderência | Alta | Sim |
| F4.2 | Checklist de documentos | Alta | Sim |
| F4.3 | Exportação PDF | Alta | Sim |
| F4.4 | Exportação Excel | Média | Sim |
| F4.5 | Relatório executivo | Média | Não |
| F4.6 | Dashboard com métricas | Baixa | Não |
| F4.7 | Personalização de relatórios | Baixa | Não |

### 4.2 Funcionalidades Excluídas (Out of Scope)

| Funcionalidade | Motivo da Exclusão |
|----------------|-------------------|
| Submissão eletrônica de propostas | Requer integração com portais governamentais |
| Precificação de propostas | Escopo diferente, complexidade alta |
| Monitoramento de editais (crawling) | Requer infraestrutura cloud |
| Chat com IA para tirar dúvidas | Já existe no AMLDO |
| Gestão de equipe/permissões | Complexidade alta para MVP |
| Sincronização cloud | MVP é 100% offline |

### 4.3 Requisitos Não-Funcionais

#### Performance

| Requisito | Especificação |
|-----------|---------------|
| RNF-01 | Tempo de inicialização < 5 segundos |
| RNF-02 | Análise de edital 100 páginas < 2 minutos |
| RNF-03 | Busca em perfil < 500ms |
| RNF-04 | Geração de relatório < 10 segundos |

#### Usabilidade

| Requisito | Especificação |
|-----------|---------------|
| RNF-05 | Interface em português brasileiro |
| RNF-06 | Acessível sem treinamento prévio |
| RNF-07 | Atalhos de teclado para ações frequentes |
| RNF-08 | Suporte a temas claro/escuro |

#### Segurança

| Requisito | Especificação |
|-----------|---------------|
| RNF-09 | Dados armazenados localmente (SQLite criptografado) |
| RNF-10 | Senha de acesso ao sistema |
| RNF-11 | Backup automático configurável |
| RNF-12 | Exportação de dados em formato aberto |

#### Compatibilidade

| Requisito | Especificação |
|-----------|---------------|
| RNF-13 | Windows 10/11 (64-bit) |
| RNF-14 | Resolução mínima 1366x768 |
| RNF-15 | 4GB RAM mínimo (8GB recomendado) |
| RNF-16 | 500MB espaço em disco + dados |

---

## 5. Jornada do Usuário

### 5.1 Jornada Principal: Análise de Edital

```
┌─────────────────────────────────────────────────────────────────────┐
│                    JORNADA: ANÁLISE DE EDITAL                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. DESCOBERTA          2. PREPARAÇÃO         3. ANÁLISE            │
│  ┌───────────────┐     ┌───────────────┐     ┌───────────────┐     │
│  │ Encontra novo │     │ Cadastra      │     │ Importa       │     │
│  │ edital de     │────▶│ perfil da     │────▶│ PDF do        │     │
│  │ interesse     │     │ empresa       │     │ edital        │     │
│  └───────────────┘     └───────────────┘     └───────────────┘     │
│         │                     │                     │               │
│         ▼                     ▼                     ▼               │
│  ┌───────────────┐     ┌───────────────┐     ┌───────────────┐     │
│  │ Precisa       │     │ Adiciona      │     │ Sistema       │     │
│  │ avaliar se    │     │ capacidades e │     │ extrai        │     │
│  │ vale disputar │     │ documentos    │     │ requisitos    │     │
│  └───────────────┘     └───────────────┘     └───────────────┘     │
│                                                     │               │
│  4. RESULTADO           5. DECISÃO          6. AÇÃO                │
│  ┌───────────────┐     ┌───────────────┐     ┌───────────────┐     │
│  │ Visualiza     │     │ Score alto?   │     │ Prepara       │     │
│  │ score de      │────▶│ Decide        │────▶│ documentação  │     │
│  │ aderência     │     │ participar    │     │ usando        │     │
│  └───────────────┘     └───────────────┘     │ checklist     │     │
│         │                     │              └───────────────┘     │
│         ▼                     ▼                     │               │
│  ┌───────────────┐     ┌───────────────┐           ▼               │
│  │ Identifica    │     │ Score baixo?  │     ┌───────────────┐     │
│  │ gaps e        │     │ Descarta ou   │     │ Participa da  │     │
│  │ recomendações │     │ planeja       │     │ licitação com │     │
│  └───────────────┘     │ adequação     │     │ mais confiança│     │
│                        └───────────────┘     └───────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 Fluxo de Primeira Utilização

```
1. Instalação
   ├── Download do instalador (.exe ou .msi)
   ├── Execução do wizard de instalação
   └── Primeira execução

2. Onboarding
   ├── Tour guiado pelas funcionalidades
   ├── Cadastro de senha de acesso
   └── Importação de dados (opcional)

3. Setup Inicial
   ├── Cadastro da empresa
   │   ├── Razão social, CNPJ
   │   ├── Ramo de atividade
   │   └── Porte da empresa
   │
   ├── Cadastro de capacidades
   │   ├── Áreas de atuação
   │   ├── Certificações
   │   └── Experiências anteriores
   │
   └── Upload de documentos
       ├── Contrato social
       ├── Certidões
       └── Atestados técnicos

4. Primeira Análise
   ├── Upload de edital exemplo
   ├── Visualização de requisitos extraídos
   ├── Cálculo de score
   └── Geração de relatório
```

---

## 6. Requisitos de Integração

### 6.1 Integração com AMLDO (RAG)

O LicitaFit utilizará o motor RAG do AMLDO para:

| Funcionalidade | Uso do AMLDO |
|----------------|--------------|
| Extração de requisitos | RAG identifica cláusulas relevantes |
| Categorização | RAG mapeia para categorias universais |
| Consulta legal | RAG responde dúvidas sobre legislação |
| Validação | RAG verifica conformidade com leis |

### 6.2 Formato de Dados de Entrada

| Tipo | Formato | Tamanho Máximo |
|------|---------|----------------|
| Edital | PDF | 50 MB |
| Documentos | PDF, JPG, PNG | 20 MB |
| Importação perfil | JSON, CSV | 5 MB |

### 6.3 Formato de Dados de Saída

| Tipo | Formato | Descrição |
|------|---------|-----------|
| Relatório | PDF | Relatório formatado para impressão |
| Dados | Excel (XLSX) | Planilha com requisitos e scores |
| Backup | JSON | Exportação completa para backup |

---

## 7. Restrições e Dependências

### 7.1 Restrições

| Tipo | Restrição |
|------|-----------|
| Técnica | Python 3.11+ obrigatório |
| Técnica | Dependência do modelo de embeddings local |
| Negócio | Licenciamento deve permitir uso comercial das libs |
| Legal | LGPD - dados pessoais no perfil da empresa |
| Recurso | Equipe de 1-2 desenvolvedores |

### 7.2 Dependências

| Dependência | Tipo | Status |
|-------------|------|--------|
| AMLDO (RAG engine) | Interna | Disponível |
| Sentence Transformers | Externa | Disponível |
| PyQt6 ou Tkinter | Externa | A definir |
| PyMuPDF (Fitz) | Externa | Disponível |
| SQLite | Externa | Disponível |

### 7.3 Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Baixa precisão na extração | Média | Alto | Permitir edição manual |
| Performance em editais grandes | Média | Médio | Processamento assíncrono |
| Adoção pelo mercado | Alta | Alto | MVP validado com usuários |
| Manutenção de categorias | Baixa | Médio | Sistema de atualização |

---

## 8. Cronograma de Alto Nível

### 8.1 Fases do Projeto

| Fase | Duração Estimada | Entregáveis |
|------|------------------|-------------|
| Discovery | - | Documentação completa (este documento) |
| Design | - | Wireframes, protótipo navegável |
| MVP Development | - | Versão funcional básica |
| Beta Testing | - | Feedback de usuários piloto |
| Launch | - | Versão 1.0 pública |

### 8.2 Marcos (Milestones)

| Marco | Descrição |
|-------|-----------|
| M1 | Aprovação do PRD |
| M2 | Protótipo de alta fidelidade aprovado |
| M3 | MVP funcional interno |
| M4 | Beta com 10 usuários piloto |
| M5 | Versão 1.0 lançada |
| M6 | 100 usuários ativos |

---

## 9. Critérios de Aceite do MVP

### 9.1 Funcionalidades Obrigatórias

- [ ] Cadastro completo de perfil da empresa
- [ ] Upload e processamento de edital PDF
- [ ] Extração de pelo menos 80% dos requisitos
- [ ] Cálculo de score de aderência
- [ ] Identificação de gaps
- [ ] Geração de relatório PDF
- [ ] Funcionamento 100% offline

### 9.2 Qualidade Mínima

- [ ] Sem bugs críticos ou bloqueadores
- [ ] Tempo de resposta dentro dos limites
- [ ] Interface consistente e intuitiva
- [ ] Documentação de usuário básica

### 9.3 Validação com Usuários

- [ ] Pelo menos 5 usuários piloto testaram
- [ ] NPS inicial > 30
- [ ] Taxa de conclusão de tarefa > 80%

---

## 10. Anexos

### 10.1 Glossário

| Termo | Definição |
|-------|-----------|
| Licitante | Empresa que participa de licitação como fornecedora |
| Licitador | Órgão público que realiza a licitação |
| Edital | Documento que estabelece regras e requisitos da licitação |
| Aderência | Grau de conformidade com os requisitos |
| Gap | Requisito não atendido pela empresa |
| RAG | Retrieval-Augmented Generation - técnica de IA |

### 10.2 Referências

- AMLDO Project Documentation
- StudentDataBank Architecture (inspiração)
- Lei 14.133/2021 (Nova Lei de Licitações)
- Lei 8.666/1993 (Lei de Licitações - legado)

### 10.3 Histórico de Revisões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | Nov/2024 | Claude | Versão inicial |

---

*Documento gerado como parte do planejamento estratégico do projeto LicitaFit.*
