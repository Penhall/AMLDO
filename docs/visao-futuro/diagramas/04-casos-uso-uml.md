# Diagrama de Casos de Uso UML
## LicitaFit - Sistema de Análise de Aderência a Editais

---

## 1. Diagrama Geral de Casos de Uso

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    DIAGRAMA DE CASOS DE USO - LICITAFIT                                         │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                 │
│                                                                                                                 │
│    ┌─────────┐                                                                              ┌─────────┐        │
│    │         │                                                                              │         │        │
│    │Analista │                        ┌──────────────────────────────────────┐              │  AMLDO  │        │
│    │   de    │                        │                                      │              │   RAG   │        │
│    │Licitação│                        │           LICITAFIT                  │              │(Sistema)│        │
│    │         │                        │                                      │              │         │        │
│    └────┬────┘                        │  ┌────────────────────────────────┐  │              └────┬────┘        │
│         │                             │  │      Gestão de Perfil         │  │                   │             │
│         │                             │  │                                │  │                   │             │
│         ├────────────────────────────▶│  │  (UC01) Cadastrar Empresa      │  │                   │             │
│         │                             │  │  (UC02) Cadastrar Capacidades  │  │                   │             │
│         │                             │  │  (UC03) Gerenciar Documentos   │  │                   │             │
│         │                             │  │  (UC04) Gerenciar Certificações│  │                   │             │
│         │                             │  │                                │  │                   │             │
│         │                             │  └────────────────────────────────┘  │                   │             │
│         │                             │                                      │                   │             │
│         │                             │  ┌────────────────────────────────┐  │                   │             │
│         │                             │  │     Análise de Editais         │  │                   │             │
│         │                             │  │                                │  │                   │             │
│         ├────────────────────────────▶│  │  (UC05) Importar Edital        │  │                   │             │
│         │                             │  │  (UC06) Extrair Requisitos ────┼──┼──────────────────▶│             │
│         │                             │  │  (UC07) Validar Requisitos     │  │                   │             │
│         │                             │  │                                │  │                   │             │
│         │                             │  └────────────────────────────────┘  │                   │             │
│         │                             │                                      │                   │             │
│         │                             │  ┌────────────────────────────────┐  │                   │             │
│         │                             │  │    Análise de Aderência        │  │                   │             │
│         │                             │  │                                │  │                   │             │
│         ├────────────────────────────▶│  │  (UC08) Executar Análise       │  │                   │             │
│         │                             │  │  (UC09) Identificar Gaps       │  │                   │             │
│         │                             │  │  (UC10) Visualizar Score       │  │                   │             │
│         │                             │  │                                │  │                   │             │
│         │                             │  └────────────────────────────────┘  │                   │             │
│    ┌────┴────┐                        │                                      │                   │             │
│    │         │                        │  ┌────────────────────────────────┐  │                   │             │
│    │ Gestor  │                        │  │       Relatórios               │  │                   │             │
│    │   de    │                        │  │                                │  │                   │             │
│    │Licitação│───────────────────────▶│  │  (UC11) Gerar Relatório        │  │                   │             │
│    │         │                        │  │  (UC12) Gerar Checklist        │  │                   │             │
│    └─────────┘                        │  │  (UC13) Exportar Dados         │  │                   │             │
│                                       │  │                                │  │                   │             │
│                                       │  └────────────────────────────────┘  │                   │             │
│                                       │                                      │                   │             │
│                                       │  ┌────────────────────────────────┐  │                   │             │
│                                       │  │       Administração            │  │                   │             │
│                                       │  │                                │  │                   │             │
│                                       │  │  (UC14) Configurar Sistema     │  │                   │             │
│                                       │  │  (UC15) Gerenciar Alertas      │  │                   │             │
│                                       │  │  (UC16) Fazer Backup           │  │                   │             │
│                                       │  │                                │  │                   │             │
│                                       │  └────────────────────────────────┘  │                   │             │
│                                       │                                      │                   │             │
│                                       └──────────────────────────────────────┘                   │             │
│                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Casos de Uso por Módulo

### 2.1 Módulo: Gestão de Perfil

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        MÓDULO: GESTÃO DE PERFIL DA EMPRESA                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│                                 ┌──────────────────────────────────────┐            │
│                                 │                                      │            │
│    ┌─────────┐                  │  ┌──────────────────────────────┐   │            │
│    │Analista │─────────────────▶│  │   UC01: Cadastrar Empresa    │   │            │
│    └─────────┘                  │  │                              │   │            │
│                                 │  │  Ator: Analista              │   │            │
│                                 │  │  Pré: Sistema instalado      │   │            │
│                                 │  │  Pós: Empresa cadastrada     │   │            │
│                                 │  └──────────────────────────────┘   │            │
│                                 │              │                       │            │
│                                 │              │ <<include>>           │            │
│                                 │              ▼                       │            │
│                                 │  ┌──────────────────────────────┐   │            │
│                                 │  │    UC02: Cadastrar           │   │            │
│                                 │  │    Capacidades               │   │            │
│                                 │  │                              │   │            │
│                                 │  │  Pré: UC01 concluído         │   │            │
│                                 │  │  Pós: Capacidades vinculadas │   │            │
│                                 │  └──────────────────────────────┘   │            │
│                                 │              │                       │            │
│                                 │              │ <<extend>>            │            │
│                                 │              ▼                       │            │
│                                 │  ┌──────────────────────────────┐   │            │
│                                 │  │    UC04: Gerenciar           │   │            │
│                                 │  │    Certificações             │   │            │
│                                 │  │                              │   │            │
│                                 │  │  Opcional: Anexar certificados│   │            │
│                                 │  └──────────────────────────────┘   │            │
│                                 │              │                       │            │
│                                 │              │ <<extend>>            │            │
│                                 │              ▼                       │            │
│                                 │  ┌──────────────────────────────┐   │            │
│                                 │  │    UC03: Gerenciar           │   │            │
│                                 │  │    Documentos                │   │            │
│                                 │  │                              │   │            │
│                                 │  │  Controle de validade        │   │            │
│                                 │  │  Alertas de vencimento       │   │            │
│                                 │  └──────────────────────────────┘   │            │
│                                 │                                      │            │
│                                 └──────────────────────────────────────┘            │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Módulo: Análise de Editais

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          MÓDULO: ANÁLISE DE EDITAIS                                 │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│                                 ┌──────────────────────────────────────┐            │
│                                 │                                      │            │
│    ┌─────────┐                  │  ┌──────────────────────────────┐   │            │
│    │Analista │─────────────────▶│  │   UC05: Importar Edital      │   │            │
│    └─────────┘                  │  │                              │   │            │
│                                 │  │  Upload de PDF               │   │            │
│                                 │  │  Extração de texto           │   │            │
│                                 │  │  Metadados do edital         │   │            │
│                                 │  └────────────┬─────────────────┘   │            │
│                                 │               │                      │            │
│                                 │               │ <<include>>          │            │
│                                 │               ▼                      │            │
│    ┌─────────┐                  │  ┌──────────────────────────────┐   │            │
│    │  AMLDO  │◀─────────────────┤  │   UC06: Extrair Requisitos   │   │            │
│    │   RAG   │                  │  │                              │   │            │
│    └─────────┘                  │  │  Usa RAG para identificar    │   │            │
│                                 │  │  e categorizar requisitos    │   │            │
│                                 │  └────────────┬─────────────────┘   │            │
│                                 │               │                      │            │
│                                 │               │ <<include>>          │            │
│                                 │               ▼                      │            │
│                                 │  ┌──────────────────────────────┐   │            │
│                                 │  │   UC07: Validar Requisitos   │   │            │
│                                 │  │                              │   │            │
│                                 │  │  Revisar extrações           │   │            │
│                                 │  │  Editar categorias           │   │            │
│                                 │  │  Adicionar/remover           │   │            │
│                                 │  └──────────────────────────────┘   │            │
│                                 │                                      │            │
│                                 └──────────────────────────────────────┘            │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Módulo: Análise de Aderência

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         MÓDULO: ANÁLISE DE ADERÊNCIA                                │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│                                 ┌──────────────────────────────────────┐            │
│                                 │                                      │            │
│    ┌─────────┐                  │  ┌──────────────────────────────┐   │            │
│    │Analista │─────────────────▶│  │   UC08: Executar Análise     │   │            │
│    └─────────┘                  │  │                              │   │            │
│         │                       │  │  Compara perfil × requisitos │   │            │
│         │                       │  │  Calcula score de aderência  │   │            │
│         │                       │  └────────────┬─────────────────┘   │            │
│         │                       │               │                      │            │
│         │                       │               │ <<include>>          │            │
│         │                       │               ▼                      │            │
│         │                       │  ┌──────────────────────────────┐   │            │
│         │                       │  │   UC09: Identificar Gaps     │   │            │
│         │                       │  │                              │   │            │
│         │                       │  │  Lista requisitos não        │   │            │
│         │                       │  │  atendidos com severidade    │   │            │
│         │                       │  │  e recomendações             │   │            │
│         │                       │  └────────────┬─────────────────┘   │            │
│         │                       │               │                      │            │
│         │                       │               │ <<include>>          │            │
│         │                       │               ▼                      │            │
│    ┌────┴────┐                  │  ┌──────────────────────────────┐   │            │
│    │         │                  │  │   UC10: Visualizar Score     │   │            │
│    │ Gestor  │─────────────────▶│  │                              │   │            │
│    │         │                  │  │  Dashboard com scores        │   │            │
│    └─────────┘                  │  │  Recomendação de participação│   │            │
│                                 │  │  Detalhamento por requisito  │   │            │
│                                 │  └──────────────────────────────┘   │            │
│                                 │                                      │            │
│                                 └──────────────────────────────────────┘            │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Relacionamentos entre Casos de Uso

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                     RELACIONAMENTOS ENTRE CASOS DE USO                              │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  DEPENDÊNCIAS (<<include>>):                                                        │
│  ──────────────────────────                                                        │
│                                                                                     │
│  UC01 ←──include──┐                                                                │
│                   │                                                                 │
│  UC02 ────────────┤←─────── Necessário para completar o perfil                     │
│                   │                                                                 │
│  UC03 ←──include──┘                                                                │
│                                                                                     │
│  UC05 ──include──▶ UC06 ──include──▶ UC07                                          │
│   │                                    │                                            │
│   │ Importar → Extrair → Validar       │                                            │
│   │                                    ▼                                            │
│   └──────────────────────────────────▶ UC08                                         │
│                                         │                                           │
│  UC08 ──include──▶ UC09 ──include──▶ UC10                                          │
│   │                                    │                                            │
│   │ Executar → Identificar Gaps → Visualizar Score                                 │
│   │                                    │                                            │
│   └────────────────────────────────────┘                                           │
│                                                                                     │
│                                                                                     │
│  EXTENSÕES (<<extend>>):                                                           │
│  ────────────────────────                                                          │
│                                                                                     │
│  UC10 ←──extend── UC11 (Gerar Relatório)                                           │
│        │                                                                            │
│        └──extend── UC12 (Gerar Checklist)                                          │
│                                                                                     │
│  UC03 ←──extend── UC15 (Alertas de Vencimento)                                     │
│                                                                                     │
│                                                                                     │
│  GENERALIZAÇÕES:                                                                    │
│  ───────────────                                                                   │
│                                                                                     │
│  UC13 (Exportar Dados)                                                             │
│        │                                                                            │
│        ├── Exportar PDF                                                            │
│        ├── Exportar Excel                                                          │
│        └── Exportar JSON (Backup)                                                  │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Especificação Resumida dos Casos de Uso

| ID | Nome | Ator Principal | Resumo |
|----|------|----------------|--------|
| UC01 | Cadastrar Empresa | Analista | Registra dados da empresa no sistema |
| UC02 | Cadastrar Capacidades | Analista | Adiciona competências e experiências |
| UC03 | Gerenciar Documentos | Analista | Upload e controle de validade |
| UC04 | Gerenciar Certificações | Analista | Cadastro de certificados e atestados |
| UC05 | Importar Edital | Analista | Upload de PDF e extração de texto |
| UC06 | Extrair Requisitos | Sistema (RAG) | Identificação automática via IA |
| UC07 | Validar Requisitos | Analista | Revisão e edição manual |
| UC08 | Executar Análise | Analista | Comparação perfil × requisitos |
| UC09 | Identificar Gaps | Sistema | Lista requisitos não atendidos |
| UC10 | Visualizar Score | Analista/Gestor | Dashboard de resultados |
| UC11 | Gerar Relatório | Analista/Gestor | Exportação de análise em PDF |
| UC12 | Gerar Checklist | Analista | Lista de documentos necessários |
| UC13 | Exportar Dados | Analista/Gestor | Backup e exportação de dados |
| UC14 | Configurar Sistema | Gestor | Ajustes de parâmetros |
| UC15 | Gerenciar Alertas | Analista/Gestor | Visualização de notificações |
| UC16 | Fazer Backup | Gestor | Backup manual do banco |

---

*Diagrama de Casos de Uso UML elaborado em Novembro/2024.*
