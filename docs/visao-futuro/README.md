# LicitaFit - Sistema de Análise de Aderência a Editais

## Visão Futura do Projeto AMLDO

Esta pasta contém a documentação completa para o projeto **LicitaFit**, uma evolução do sistema AMLDO focada em oferecer serviços de valor agregado para **Licitantes** (empresas fornecedoras em processos licitatórios).

---

## Contexto e Motivação

### Problema Identificado

O projeto AMLDO atual atende bem ao público **estudante/consultor** que deseja tirar dúvidas sobre legislação de licitações. Entretanto, identificou-se uma lacuna de mercado para serviços que agreguem valor real aos **Licitantes** - empresas que participam de processos licitatórios.

### Inspiração: StudentDataBank (ESB)

O projeto foi inspirado no sistema **StudentDataBank**, que resolve um problema análogo no mundo acadêmico:

| StudentDataBank | LicitaFit |
|-----------------|-----------|
| Universidades trocam dados de alunos | Empresas validam requisitos de editais |
| Cursos são mapeados para códigos universais | Requisitos são mapeados para capacidades da empresa |
| Disciplinas creditadas automaticamente | Requisitos atendidos automaticamente |
| Verificação de elegibilidade para diploma | Verificação de elegibilidade para licitação |

### Os 3 Públicos do AMLDO

1. **Estudante/Consultor** - Tirar dúvidas sobre legislação (AMLDO atual)
2. **Licitador (Órgão Público)** - Adquirir produtos/serviços via licitação
3. **Licitante (Empresa)** - Fornecer produtos/serviços em licitações (FOCO DO LicitaFit)

---

## Índice de Documentos

### Documentação Estratégica

| # | Documento | Descrição |
|---|-----------|-----------|
| 01 | [PRD - Product Requirements Document](01-prd-requisitos-produto.md) | Visão do produto, objetivos, escopo e métricas de sucesso |
| 02 | [Análise de Mercado](02-analise-mercado.md) | Pesquisa de mercado, concorrência e oportunidades |

### Documentação Técnica

| # | Documento | Descrição |
|---|-----------|-----------|
| 03 | [Arquitetura Técnica](03-arquitetura-tecnica.md) | Arquitetura do sistema desktop, componentes e integrações |
| 04 | [Modelo de Dados](04-modelo-dados.md) | Estrutura de dados, entidades e relacionamentos |
| 05 | [Casos de Uso](05-casos-de-uso.md) | Casos de uso detalhados com fluxos e atores |
| 06 | [Regras de Negócio](06-regras-negocio.md) | Regras de negócio e validações do sistema |

### Documentação de Interface

| # | Documento | Descrição |
|---|-----------|-----------|
| 07 | [Especificação de Interface](07-especificacao-interface.md) | Wireframes, fluxos de tela e componentes visuais |
| 08 | [Guia de Estilo](08-guia-estilo.md) | Padrões visuais, cores, tipografia e componentes |

### Documentação de Implementação

| # | Documento | Descrição |
|---|-----------|-----------|
| 09 | [Stack Tecnológica](09-stack-tecnologica.md) | Tecnologias, frameworks e ferramentas recomendadas |
| 10 | [Roadmap de Implementação](10-roadmap-implementacao.md) | Fases, sprints e entregas planejadas |

### Diagramas

| Diagrama | Descrição |
|----------|-----------|
| [diagramas/01-arquitetura-geral.md](diagramas/01-arquitetura-geral.md) | Visão geral da arquitetura |
| [diagramas/02-modelo-er.md](diagramas/02-modelo-er.md) | Modelo Entidade-Relacionamento |
| [diagramas/03-fluxo-analise.md](diagramas/03-fluxo-analise.md) | Fluxo de análise de aderência |
| [diagramas/04-casos-uso-uml.md](diagramas/04-casos-uso-uml.md) | Diagramas UML de casos de uso |
| [diagramas/05-sequencia.md](diagramas/05-sequencia.md) | Diagramas de sequência |

---

## Resumo do Projeto StudentDataBank (Inspiração)

### O que é o StudentDataBank?

Sistema de troca segura de registros acadêmicos entre universidades, permitindo:
- Armazenamento centralizado de histórico acadêmico
- Creditação automática de disciplinas entre instituições
- Verificação automática de requisitos para diplomas
- Mapeamento de disciplinas para "cursos universais"

### Conceitos-Chave Adaptados

```
StudentDataBank          →  LicitaFit
─────────────────────────────────────────────
EducationalInstitute     →  Empresa (Licitante)
Student                  →  Edital
Course (EICourse)        →  Requisito do Edital
UniversalCourse          →  Categoria Universal de Requisito
Program                  →  Processo Licitatório
ProgramRequiredCourse    →  Requisito Obrigatório
CourseTaken              →  Capacidade/Certificação da Empresa
CourseCredited           →  Requisito Atendido
LinkToOtherEI            →  Vínculo com Fornecedor/Parceiro
```

### Fluxo de Aderência (Analogia)

```
StudentDataBank:
  Aluno → Matricula em Programa → Sistema verifica disciplinas cursadas
       → Mapeia para cursos universais → Credita automaticamente
       → Verifica elegibilidade para diploma

LicitaFit:
  Empresa → Importa Edital → Sistema extrai requisitos
         → Mapeia para categorias universais → Verifica capacidades
         → Calcula score de aderência → Gera relatório
```

---

## Proposta de Valor do LicitaFit

### Para o Licitante (Empresa)

1. **Análise Automatizada de Editais**
   - Upload de PDF do edital
   - Extração automática de requisitos via RAG
   - Identificação de requisitos obrigatórios vs desejáveis

2. **Verificação de Aderência**
   - Cadastro do perfil da empresa (capacidades, certificações, histórico)
   - Comparação automática com requisitos do edital
   - Score de aderência percentual

3. **Relatórios Inteligentes**
   - Gap analysis (o que falta para atender)
   - Recomendações de ação
   - Estimativa de esforço para adequação

4. **Gestão de Documentos**
   - Organização de documentos por edital
   - Checklist de documentos necessários
   - Alertas de validade de certidões

### Diferenciais Competitivos

- **Integração com AMLDO**: Base de conhecimento legal já existente
- **RAG Especializado**: Extração inteligente de requisitos
- **Desktop First**: Foco em usabilidade offline e performance
- **Privacidade**: Dados sensíveis ficam locais na empresa

---

## Como Navegar esta Documentação

### Para Stakeholders/PO
1. Comece pelo [PRD](01-prd-requisitos-produto.md)
2. Revise a [Análise de Mercado](02-analise-mercado.md)
3. Acompanhe o [Roadmap](10-roadmap-implementacao.md)

### Para Arquitetos/Tech Leads
1. Leia a [Arquitetura Técnica](03-arquitetura-tecnica.md)
2. Estude o [Modelo de Dados](04-modelo-dados.md)
3. Avalie a [Stack Tecnológica](09-stack-tecnologica.md)

### Para Desenvolvedores
1. Entenda os [Casos de Uso](05-casos-de-uso.md)
2. Revise as [Regras de Negócio](06-regras-negocio.md)
3. Consulte a [Especificação de Interface](07-especificacao-interface.md)

### Para Designers
1. Leia o [Guia de Estilo](08-guia-estilo.md)
2. Revise a [Especificação de Interface](07-especificacao-interface.md)
3. Analise os [Diagramas de Fluxo](diagramas/03-fluxo-analise.md)

---

## Status do Projeto

| Fase | Status | Descrição |
|------|--------|-----------|
| Documentação | Em Andamento | Criação da documentação completa |
| Aprovação | Pendente | Revisão e aprovação dos stakeholders |
| Design | Não Iniciado | Criação de protótipos de alta fidelidade |
| Desenvolvimento | Não Iniciado | Implementação do sistema |
| Testes | Não Iniciado | QA e testes de aceitação |
| Deploy | Não Iniciado | Distribuição do aplicativo desktop |

---

## Contato e Contribuição

Este projeto faz parte da evolução do ecossistema AMLDO. Para contribuir:

1. Revise a documentação e sugira melhorias
2. Identifique requisitos adicionais
3. Proponha casos de uso não cobertos
4. Valide as regras de negócio com especialistas

---

*Documentação criada em Novembro/2024 como parte do planejamento estratégico do projeto AMLDO.*
