# Roadmap de Implementação
## LicitaFit - Sistema de Análise de Aderência a Editais

**Versão:** 1.0
**Data:** Novembro/2024

---

## 1. Visão Geral do Roadmap

### 1.1 Fases do Projeto

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              ROADMAP DO PROJETO                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  FASE 0          FASE 1          FASE 2          FASE 3          FASE 4           │
│  Discovery       MVP             Beta            Launch          Evolução          │
│                                                                                     │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │         │    │         │    │         │    │         │    │         │         │
│  │Documen- │───▶│  Core   │───▶│  Beta   │───▶│ Versão  │───▶│Melhorias│         │
│  │ tação   │    │Features │    │ Testing │    │  1.0    │    │Contínuas│         │
│  │         │    │         │    │         │    │         │    │         │         │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘         │
│                                                                                     │
│  ▪ PRD          ▪ UI Base      ▪ 10-20        ▪ Instalador   ▪ Novas             │
│  ▪ Arquitetura  ▪ Cadastros    │ usuários    ▪ Docs usuário│ features          │
│  ▪ Protótipos   ▪ Importação   ▪ Feedback    ▪ Marketing    ▪ Integrações       │
│  ▪ Validação    ▪ Análise      ▪ Bug fixes   ▪ Suporte      ▪ Otimizações       │
│                 ▪ Relatórios                                                       │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Fase 0: Discovery (Atual)

### 2.1 Entregáveis Concluídos

| # | Entregável | Status | Documento |
|---|------------|--------|-----------|
| 1 | PRD - Requisitos do Produto | Concluído | 01-prd-requisitos-produto.md |
| 2 | Análise de Mercado | Concluído | 02-analise-mercado.md |
| 3 | Arquitetura Técnica | Concluído | 03-arquitetura-tecnica.md |
| 4 | Modelo de Dados | Concluído | 04-modelo-dados.md |
| 5 | Casos de Uso | Concluído | 05-casos-de-uso.md |
| 6 | Regras de Negócio | Concluído | 06-regras-negocio.md |
| 7 | Especificação de Interface | Concluído | 07-especificacao-interface.md |
| 8 | Guia de Estilo | Concluído | 08-guia-estilo.md |
| 9 | Stack Tecnológica | Concluído | 09-stack-tecnologica.md |
| 10 | Roadmap | Concluído | 10-roadmap-implementacao.md |
| 11 | Diagramas | Concluído | diagramas/ |

### 2.2 Próximos Passos (Fase 0)

- [ ] Revisão da documentação por stakeholders
- [ ] Aprovação do PRD
- [ ] Criação de protótipo navegável (Figma/Adobe XD)
- [ ] Validação do protótipo com usuários potenciais
- [ ] Decisão de Go/No-Go para desenvolvimento

---

## 3. Fase 1: MVP

### 3.1 Escopo do MVP

**Funcionalidades Core:**

| # | Feature | Prioridade | Complexidade |
|---|---------|------------|--------------|
| 1 | Setup do projeto e estrutura | Alta | Média |
| 2 | Tela principal e navegação | Alta | Média |
| 3 | Cadastro de empresa (CRUD) | Alta | Baixa |
| 4 | Cadastro de capacidades | Alta | Baixa |
| 5 | Gerenciamento de documentos | Alta | Média |
| 6 | Importação de edital (PDF) | Alta | Alta |
| 7 | Extração de requisitos (RAG) | Alta | Alta |
| 8 | Análise de aderência | Alta | Alta |
| 9 | Visualização de score/gaps | Alta | Média |
| 10 | Geração de relatório PDF | Alta | Média |

**Funcionalidades Fora do MVP:**

| Feature | Motivo | Fase Planejada |
|---------|--------|----------------|
| Multi-empresa | Complexidade | v1.5 |
| Sincronização cloud | Infraestrutura | v2.0 |
| OCR para PDFs escaneados | Complexidade | v1.5 |
| Dashboard com gráficos | Nice-to-have | v1.2 |
| Backup automático | Nice-to-have | v1.1 |

### 3.2 Sprints do MVP

#### Sprint 1: Fundação

**Objetivo:** Estrutura base do projeto funcionando

| Task | Descrição | Estimativa |
|------|-----------|------------|
| 1.1 | Setup do projeto Python | Pequeno |
| 1.2 | Configuração PyQt6 | Pequeno |
| 1.3 | Estrutura de diretórios | Pequeno |
| 1.4 | Configuração SQLite/SQLAlchemy | Pequeno |
| 1.5 | Janela principal (MainWindow) | Médio |
| 1.6 | Sistema de navegação (sidebar) | Médio |
| 1.7 | Tema claro/escuro básico | Pequeno |
| 1.8 | Sistema de configurações | Pequeno |

**Critérios de Aceite:**
- Aplicação abre sem erros
- Navegação entre seções funciona
- Banco de dados é criado automaticamente

---

#### Sprint 2: Gestão de Empresa

**Objetivo:** Cadastro completo de perfil da empresa

| Task | Descrição | Estimativa |
|------|-----------|------------|
| 2.1 | Tela de listagem de empresas | Médio |
| 2.2 | Dialog de cadastro de empresa | Médio |
| 2.3 | Validação de CNPJ | Pequeno |
| 2.4 | CRUD completo de empresa | Médio |
| 2.5 | Tela de perfil da empresa | Grande |
| 2.6 | Abas: Capacidades, Certificações, Documentos | Grande |
| 2.7 | CRUD de capacidades | Médio |
| 2.8 | CRUD de certificações | Médio |
| 2.9 | Upload e gestão de documentos | Grande |
| 2.10 | Sistema de categorias universais | Médio |

**Critérios de Aceite:**
- Cadastro de empresa com validação
- Adicionar/editar/remover capacidades
- Upload de documentos com validação de formato
- Categorização funcionando

---

#### Sprint 3: Importação de Editais

**Objetivo:** Importar e processar editais em PDF

| Task | Descrição | Estimativa |
|------|-----------|------------|
| 3.1 | Tela de listagem de editais | Médio |
| 3.2 | Dialog de importação de edital | Grande |
| 3.3 | Upload de PDF com drag-and-drop | Médio |
| 3.4 | Extração de texto (PyMuPDF) | Grande |
| 3.5 | Identificação de seções do edital | Grande |
| 3.6 | Integração com AMLDO RAG | Grande |
| 3.7 | Extração de requisitos | Grande |
| 3.8 | Categorização automática | Grande |
| 3.9 | Tela de revisão de requisitos | Grande |
| 3.10 | Edição manual de requisitos | Médio |

**Critérios de Aceite:**
- Upload de PDF funciona
- Texto é extraído corretamente
- Requisitos são identificados (>80% precisão)
- Usuário pode editar requisitos

---

#### Sprint 4: Análise de Aderência

**Objetivo:** Motor de análise funcionando

| Task | Descrição | Estimativa |
|------|-----------|------------|
| 4.1 | Motor de matching | Grande |
| 4.2 | Algoritmo de score | Grande |
| 4.3 | Identificação de gaps | Grande |
| 4.4 | Classificação de severidade | Médio |
| 4.5 | Geração de recomendações | Grande |
| 4.6 | Tela de resultado da análise | Grande |
| 4.7 | Visualização de score | Médio |
| 4.8 | Lista de requisitos com status | Médio |
| 4.9 | Detalhes de gaps | Médio |
| 4.10 | Filtros e ordenação | Pequeno |

**Critérios de Aceite:**
- Score calculado corretamente
- Gaps identificados com severidade
- Recomendação gerada automaticamente
- Interface clara e intuitiva

---

#### Sprint 5: Relatórios e Polimento

**Objetivo:** Geração de relatórios e refinamentos

| Task | Descrição | Estimativa |
|------|-----------|------------|
| 5.1 | Template de relatório executivo | Grande |
| 5.2 | Template de relatório detalhado | Grande |
| 5.3 | Geração de PDF (ReportLab) | Grande |
| 5.4 | Exportação para Excel | Médio |
| 5.5 | Geração de checklist | Médio |
| 5.6 | Sistema de alertas básico | Médio |
| 5.7 | Refinamentos de UI | Médio |
| 5.8 | Correção de bugs | Variável |
| 5.9 | Testes de integração | Grande |
| 5.10 | Documentação técnica | Médio |

**Critérios de Aceite:**
- Relatório PDF gerado corretamente
- Exportação Excel funciona
- Alertas de vencimento funcionam
- Aplicação estável

---

#### Sprint 6: Empacotamento e Distribuição

**Objetivo:** Aplicação pronta para distribuição

| Task | Descrição | Estimativa |
|------|-----------|------------|
| 6.1 | Configuração PyInstaller | Grande |
| 6.2 | Build do executável | Médio |
| 6.3 | Testes em máquina limpa | Grande |
| 6.4 | Criação do instalador (Inno Setup) | Grande |
| 6.5 | Documentação do usuário | Grande |
| 6.6 | Manual de instalação | Médio |
| 6.7 | FAQ inicial | Pequeno |
| 6.8 | Vídeo tutorial (opcional) | Grande |
| 6.9 | Testes finais | Grande |
| 6.10 | Preparação para beta | Médio |

**Critérios de Aceite:**
- Instalador funciona em Windows 10/11
- Documentação completa
- Zero bugs críticos
- Pronto para beta testing

---

## 4. Fase 2: Beta Testing

### 4.1 Estratégia de Beta

| Aspecto | Plano |
|---------|-------|
| **Quantidade** | 10-20 usuários piloto |
| **Perfil** | Mix de analistas, gestores e consultores |
| **Recrutamento** | Rede de contatos, LinkedIn, grupos de licitação |
| **Incentivo** | Licença gratuita vitalícia para participantes |

### 4.2 Coleta de Feedback

| Método | Frequência | Objetivo |
|--------|------------|----------|
| Formulário in-app | Contínuo | Bugs e sugestões |
| Entrevistas 1:1 | Semanal | Feedback qualitativo |
| Analytics | Contínuo | Uso e comportamento |
| Grupo WhatsApp | Contínuo | Suporte e discussão |

### 4.3 Critérios para Launch

- [ ] NPS >= 30
- [ ] Taxa de conclusão de tarefa >= 80%
- [ ] Zero bugs críticos
- [ ] Precisão de extração >= 80%
- [ ] Tempo médio de análise <= 15 minutos

---

## 5. Fase 3: Launch (v1.0)

### 5.1 Checklist de Lançamento

| Categoria | Item | Status |
|-----------|------|--------|
| **Produto** | Versão 1.0 estável | Pendente |
| **Produto** | Instalador Windows | Pendente |
| **Docs** | Manual do usuário | Pendente |
| **Docs** | FAQ | Pendente |
| **Docs** | Vídeos tutoriais | Pendente |
| **Marketing** | Landing page | Pendente |
| **Marketing** | Material de vendas | Pendente |
| **Suporte** | Canal de suporte | Pendente |
| **Legal** | Termos de uso | Pendente |
| **Legal** | Política de privacidade | Pendente |

### 5.2 Estratégia de Preços (Sugestão)

| Plano | Preço | Inclui |
|-------|-------|--------|
| Starter | R$ 297 (único) | 1 empresa, updates 1 ano |
| Profissional | R$ 597 (único) | 3 empresas, updates 2 anos |
| Consultor | R$ 997 (único) | Ilimitado, updates vitalício |

---

## 6. Fase 4: Evolução (v1.x, v2.x)

### 6.1 Roadmap de Features Futuras

```
v1.1                    v1.5                    v2.0
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│             │         │             │         │             │
│ • Backup    │         │ • Multi-    │         │ • Versão    │
│   automático│────────▶│   empresa   │────────▶│   Web       │
│ • Dashboard │         │ • OCR PDFs  │         │ • Sync      │
│ • Melhorias │         │ • Integração│         │   Cloud     │
│   UI        │         │   portais   │         │ • API       │
│             │         │             │         │             │
└─────────────┘         └─────────────┘         └─────────────┘
```

### 6.2 Features por Versão

#### v1.1 - Melhorias Incrementais
- Dashboard com estatísticas
- Backup automático configurável
- Melhorias de performance
- Correções de bugs
- Refinamentos de UI

#### v1.5 - Expansão de Funcionalidades
- Suporte a múltiplas empresas (consultores)
- OCR para PDFs escaneados
- Integração com portais de licitação
- Templates de relatório customizáveis
- Histórico de participações

#### v2.0 - Nova Arquitetura
- Versão web complementar
- Sincronização cloud opcional
- API para integrações
- App mobile companion
- Multi-usuário com permissões

---

## 7. Riscos e Mitigações

### 7.1 Riscos Identificados

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Baixa precisão RAG | Média | Alto | Edição manual, treinamento contínuo |
| Adoção lenta | Média | Alto | Marketing, programa de beta gratuito |
| Bugs em produção | Média | Alto | Testes extensivos, beta testing |
| Escopo cresce | Alta | Médio | Priorização rigorosa, MVP focado |
| Dependência AMLDO | Baixa | Alto | Modularização, fallbacks |

### 7.2 Plano de Contingência

| Cenário | Ação |
|---------|------|
| MVP atrasa | Reduzir escopo, focar em core features |
| Beta negativo | Pivotar baseado em feedback, adiar launch |
| Problemas técnicos | Consultoria externa, revisão de arquitetura |
| Falta de recursos | Buscar parceiros, simplificar produto |

---

## 8. Métricas de Sucesso

### 8.1 KPIs por Fase

| Fase | Métrica | Target |
|------|---------|--------|
| MVP | Features entregues | 100% do escopo |
| Beta | NPS | >= 30 |
| Beta | Bugs críticos | 0 |
| Launch | Downloads primeiro mês | 100+ |
| v1.x | Usuários ativos | 500+ |
| v2.0 | Receita mensal | R$ 20.000+ |

### 8.2 Dashboard de Acompanhamento

| Indicador | Meta | Atual | Status |
|-----------|------|-------|--------|
| Documentação completa | 100% | 100% | OK |
| Protótipo aprovado | Sim | Pendente | - |
| MVP funcional | Sim | Pendente | - |
| Beta concluído | Sim | Pendente | - |
| Versão 1.0 lançada | Sim | Pendente | - |

---

## 9. Próximos Passos Imediatos

### 9.1 Ações para Iniciar Desenvolvimento

1. **Revisar e aprovar documentação** - Stakeholders validam PRD e arquitetura
2. **Criar protótipo de alta fidelidade** - Figma/Adobe XD para validação de UI
3. **Validar protótipo com usuários** - 3-5 entrevistas de usabilidade
4. **Setup do ambiente de desenvolvimento** - Repositório, CI/CD, ambiente
5. **Iniciar Sprint 1** - Fundação do projeto

### 9.2 Checklist de Preparação

- [ ] Documentação revisada e aprovada
- [ ] Protótipo criado e validado
- [ ] Repositório Git criado
- [ ] Ambiente de desenvolvimento configurado
- [ ] Equipe alocada
- [ ] Ferramentas de gestão configuradas (Jira, Trello, etc.)

---

*Roadmap elaborado em Novembro/2024 como parte do planejamento do projeto LicitaFit.*
