# Diagrama Entidade-Relacionamento (ER)
## LicitaFit - Sistema de Análise de Aderência a Editais

---

## 1. Diagrama ER Completo

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                     MODELO ENTIDADE-RELACIONAMENTO                                              │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                 │
│                                          ┌─────────────────────┐                                               │
│                                          │  CATEGORIA_UNIV     │                                               │
│                                          ├─────────────────────┤                                               │
│                                          │ PK id               │                                               │
│                                          │    codigo           │                                               │
│                                          │    nome             │                                               │
│                                          │    descricao        │                                               │
│                                          │    area             │                                               │
│                                          │ FK categoria_pai_id │───────┐                                       │
│                                          └─────────────────────┘       │ (auto-referência)                     │
│                                                    │                   │                                       │
│                            ┌───────────────────────┼───────────────────┘                                       │
│                            │                       │                                                           │
│                            │                       │                                                           │
│    ┌───────────────────────┼───────────────────────┼───────────────────────┐                                   │
│    │                       │                       │                       │                                   │
│    ▼                       ▼                       ▼                       ▼                                   │
│ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                             │
│ │   CAPACIDADE    │  │  CERTIFICACAO   │  │   REQUISITO     │  │ SINON_CATEGORIA │                             │
│ ├─────────────────┤  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤                             │
│ │ PK id           │  │ PK id           │  │ PK id           │  │ PK id           │                             │
│ │ FK empresa_id   │  │ FK empresa_id   │  │ FK edital_id    │  │ FK categoria_id │                             │
│ │ FK categoria_id │  │ FK categoria_id │  │ FK secao_id     │  │    termo        │                             │
│ │    descricao    │  │    tipo         │  │ FK categoria_id │  │    peso         │                             │
│ │    nivel        │  │    nome         │  │    tipo         │  └─────────────────┘                             │
│ │    experiencia  │  │    emissor      │  │    area         │                                                  │
│ │    projetos     │  │    data_emissao │  │    descricao    │                                                  │
│ └────────┬────────┘  │    data_validade│  │    texto_orig   │                                                  │
│          │           │    arquivo      │  │    atendido     │                                                  │
│          │           └────────┬────────┘  └────────┬────────┘                                                  │
│          │                    │                    │                                                           │
│          │                    │                    │                                                           │
│          │    ┌───────────────┘                    │                                                           │
│          │    │                                    │                                                           │
│          ▼    ▼                                    │                                                           │
│    ┌─────────────────┐                             │                                                           │
│    │    EMPRESA      │                             │                                                           │
│    ├─────────────────┤                             │                                                           │
│    │ PK id           │                             │                                                           │
│    │    cnpj         │                             │                                                           │
│    │    razao_social │                             │                                                           │
│    │    nome_fantasia│        ┌────────────────────┘                                                           │
│    │    porte        │        │                                                                                │
│    │    ramo_ativid  │        │                                                                                │
│    │    endereco     │        │                                                                                │
│    │    telefone     │        ▼                                                                                │
│    │    email        │  ┌─────────────────┐                                                                    │
│    └────────┬────────┘  │    EDITAL       │                                                                    │
│             │           ├─────────────────┤                                                                    │
│             │           │ PK id           │                                                                    │
│             │           │ FK empresa_id   │◀───────────────────────────────────────┐                           │
│             │           │    numero       │                                        │                           │
│             └──────────▶│    orgao        │                                        │                           │
│                         │    modalidade   │                                        │                           │
│                         │    objeto       │        ┌─────────────────┐             │                           │
│                         │    data_abertura│        │  SECAO_EDITAL   │             │                           │
│                         │    arquivo      │        ├─────────────────┤             │                           │
│                         │    texto_extrai │◀───────│ PK id           │             │                           │
│                         │    status       │        │ FK edital_id    │             │                           │
│                         └────────┬────────┘        │    titulo       │             │                           │
│                                  │                 │    texto        │             │                           │
│                                  │                 │    tipo         │             │                           │
│                                  │                 └─────────────────┘             │                           │
│                                  │                                                 │                           │
│                                  │                                                 │                           │
│                                  ▼                                                 │                           │
│                         ┌─────────────────┐                                        │                           │
│                         │    ANALISE      │                                        │                           │
│                         ├─────────────────┤                                        │                           │
│                         │ PK id           │                                        │                           │
│                         │ FK empresa_id   │────────────────────────────────────────┘                           │
│                         │ FK edital_id    │                                                                    │
│                         │    score_global │                                                                    │
│                         │    score_obrig  │                                                                    │
│                         │    score_desej  │        ┌─────────────────┐                                         │
│                         │    recomendacao │        │      GAP        │                                         │
│                         │    data_analise │        ├─────────────────┤                                         │
│                         │    status       │◀───────│ PK id           │                                         │
│                         └────────┬────────┘        │ FK analise_id   │                                         │
│                                  │                 │ FK requisito_id │                                         │
│                                  │                 │    tipo         │                                         │
│                                  │                 │    severidade   │                                         │
│                                  │                 │    descricao    │                                         │
│                                  │                 │    recomendacao │                                         │
│                                  │                 │    status       │                                         │
│                                  │                 └─────────────────┘                                         │
│                                  │                                                                             │
│                                  ▼                                                                             │
│                         ┌─────────────────────────────────┐                                                    │
│                         │   MATCH_REQUISITO_CAPACIDADE    │                                                    │
│                         ├─────────────────────────────────┤                                                    │
│                         │ PK id                           │                                                    │
│                         │ FK analise_id                   │                                                    │
│                         │ FK requisito_id                 │                                                    │
│                         │ FK capacidade_id (nullable)     │                                                    │
│                         │ FK certificacao_id (nullable)   │                                                    │
│                         │ FK documento_id (nullable)      │                                                    │
│                         │    tipo_match                   │                                                    │
│                         │    score_match                  │                                                    │
│                         │    status_match                 │                                                    │
│                         └─────────────────────────────────┘                                                    │
│                                                                                                                 │
│    ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐                                 │
│    │   DOCUMENTO     │         │    ALERTA       │         │  LOG_AUDITORIA  │                                 │
│    ├─────────────────┤         ├─────────────────┤         ├─────────────────┤                                 │
│    │ PK id           │         │ PK id           │         │ PK id           │                                 │
│    │ FK empresa_id   │         │ FK empresa_id   │         │    timestamp    │                                 │
│    │    tipo         │         │    tipo         │         │    usuario      │                                 │
│    │    nome         │         │    prioridade   │         │    acao         │                                 │
│    │    arquivo      │         │    titulo       │         │    entidade     │                                 │
│    │    data_emissao │         │    mensagem     │         │    entidade_id  │                                 │
│    │    data_validade│         │    lido         │         │    dados_antes  │                                 │
│    │    status       │         │    descartado   │         │    dados_depois │                                 │
│    └─────────────────┘         └─────────────────┘         └─────────────────┘                                 │
│                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Relacionamentos Detalhados

### 2.1 Cardinalidade dos Relacionamentos

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          CARDINALIDADE DOS RELACIONAMENTOS                         │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  EMPRESA ────────┬──── 1:N ────── CAPACIDADE                                      │
│                  │                                                                 │
│                  ├──── 1:N ────── CERTIFICACAO                                    │
│                  │                                                                 │
│                  ├──── 1:N ────── DOCUMENTO                                       │
│                  │                                                                 │
│                  ├──── 1:N ────── EDITAL                                          │
│                  │                                                                 │
│                  ├──── 1:N ────── ANALISE                                         │
│                  │                                                                 │
│                  └──── 1:N ────── ALERTA                                          │
│                                                                                    │
│  EDITAL ─────────┬──── 1:N ────── SECAO_EDITAL                                    │
│                  │                                                                 │
│                  ├──── 1:N ────── REQUISITO                                       │
│                  │                                                                 │
│                  └──── 1:N ────── ANALISE                                         │
│                                                                                    │
│  ANALISE ────────┬──── 1:N ────── GAP                                             │
│                  │                                                                 │
│                  └──── 1:N ────── MATCH_REQUISITO_CAPACIDADE                      │
│                                                                                    │
│  REQUISITO ──────┬──── 1:N ────── GAP                                             │
│                  │                                                                 │
│                  └──── 1:N ────── MATCH_REQUISITO_CAPACIDADE                      │
│                                                                                    │
│  CATEGORIA_UNIV ─┬──── 1:N ────── CAPACIDADE                                      │
│                  │                                                                 │
│                  ├──── 1:N ────── CERTIFICACAO                                    │
│                  │                                                                 │
│                  ├──── 1:N ────── REQUISITO                                       │
│                  │                                                                 │
│                  ├──── 1:N ────── SINONIMO_CATEGORIA                              │
│                  │                                                                 │
│                  └──── 1:N ────── CATEGORIA_UNIV (auto-ref)                       │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Tabela de Relacionamentos

| Entidade Origem | Relacionamento | Entidade Destino | Cardinalidade | FK |
|-----------------|----------------|------------------|---------------|-----|
| EMPRESA | possui | CAPACIDADE | 1:N | capacidade.empresa_id |
| EMPRESA | possui | CERTIFICACAO | 1:N | certificacao.empresa_id |
| EMPRESA | possui | DOCUMENTO | 1:N | documento.empresa_id |
| EMPRESA | analisa | EDITAL | 1:N | edital.empresa_id |
| EMPRESA | realiza | ANALISE | 1:N | analise.empresa_id |
| EMPRESA | recebe | ALERTA | 1:N | alerta.empresa_id |
| EDITAL | contém | SECAO_EDITAL | 1:N | secao_edital.edital_id |
| EDITAL | contém | REQUISITO | 1:N | requisito.edital_id |
| EDITAL | é analisado por | ANALISE | 1:N | analise.edital_id |
| ANALISE | identifica | GAP | 1:N | gap.analise_id |
| ANALISE | gera | MATCH | 1:N | match.analise_id |
| REQUISITO | gera | GAP | 1:N | gap.requisito_id |
| REQUISITO | gera | MATCH | 1:N | match.requisito_id |
| CATEGORIA_UNIV | classifica | CAPACIDADE | 1:N | capacidade.categoria_universal_id |
| CATEGORIA_UNIV | classifica | CERTIFICACAO | 1:N | certificacao.categoria_universal_id |
| CATEGORIA_UNIV | classifica | REQUISITO | 1:N | requisito.categoria_universal_id |
| CATEGORIA_UNIV | possui | SINONIMO | 1:N | sinonimo.categoria_universal_id |
| CATEGORIA_UNIV | é pai de | CATEGORIA_UNIV | 1:N | categoria.categoria_pai_id |

---

## 3. Diagrama de Classes (Simplificado)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                               DIAGRAMA DE CLASSES                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────┐       ┌─────────────────────────────┐             │
│  │         <<entity>>          │       │         <<entity>>          │             │
│  │          Empresa            │       │      CategoriaUniversal     │             │
│  ├─────────────────────────────┤       ├─────────────────────────────┤             │
│  │ - id: int                   │       │ - id: int                   │             │
│  │ - cnpj: CNPJ                │       │ - codigo: str               │             │
│  │ - razao_social: str         │       │ - nome: str                 │             │
│  │ - porte: PorteEnum          │       │ - area: AreaEnum            │             │
│  ├─────────────────────────────┤       ├─────────────────────────────┤             │
│  │ + adicionar_capacidade()    │       │ + get_filhas()              │             │
│  │ + adicionar_documento()     │       │ + buscar_sinonimos()        │             │
│  │ + verificar_documentos()    │       └──────────────┬──────────────┘             │
│  └──────────────┬──────────────┘                      │                            │
│                 │                                     │                            │
│                 │ 1:N                                 │ 1:N                        │
│                 ▼                                     ▼                            │
│  ┌─────────────────────────────┐       ┌─────────────────────────────┐             │
│  │         <<entity>>          │       │         <<entity>>          │             │
│  │        Capacidade           │       │         Requisito           │             │
│  ├─────────────────────────────┤       ├─────────────────────────────┤             │
│  │ - id: int                   │       │ - id: int                   │             │
│  │ - descricao: str            │       │ - tipo: TipoRequisitoEnum   │             │
│  │ - nivel: NivelEnum          │       │ - area: AreaEnum            │             │
│  │ - anos_experiencia: int     │       │ - descricao: str            │             │
│  ├─────────────────────────────┤       │ - texto_original: str       │             │
│  │ + atende_requisito()        │       ├─────────────────────────────┤             │
│  └─────────────────────────────┘       │ + esta_atendido(): bool     │             │
│                                        └─────────────────────────────┘             │
│                                                                                     │
│  ┌─────────────────────────────┐       ┌─────────────────────────────┐             │
│  │         <<entity>>          │       │         <<entity>>          │             │
│  │          Edital             │       │          Analise            │             │
│  ├─────────────────────────────┤       ├─────────────────────────────┤             │
│  │ - id: int                   │       │ - id: int                   │             │
│  │ - numero: str               │       │ - score_global: float       │             │
│  │ - orgao: str                │       │ - score_obrig: float        │             │
│  │ - modalidade: ModalidadeEnum│       │ - recomendacao: RecomEnum   │             │
│  │ - data_abertura: datetime   │       ├─────────────────────────────┤             │
│  ├─────────────────────────────┤       │ + calcular_score()          │             │
│  │ + extrair_requisitos()      │       │ + identificar_gaps()        │             │
│  │ + processar_pdf()           │       │ + gerar_recomendacao()      │             │
│  └─────────────────────────────┘       └─────────────────────────────┘             │
│                                                                                     │
│  ┌─────────────────────────────┐       ┌─────────────────────────────┐             │
│  │         <<entity>>          │       │      <<value_object>>       │             │
│  │            Gap              │       │           Score             │             │
│  ├─────────────────────────────┤       ├─────────────────────────────┤             │
│  │ - id: int                   │       │ - valor: float              │             │
│  │ - tipo: TipoGapEnum         │       │ - min: float = 0            │             │
│  │ - severidade: SeveridadeEnum│       │ - max: float = 100          │             │
│  │ - descricao: str            │       ├─────────────────────────────┤             │
│  │ - recomendacao: str         │       │ + is_participar(): bool     │             │
│  ├─────────────────────────────┤       │ + is_avaliar(): bool        │             │
│  │ + resolver()                │       │ + get_cor(): str            │             │
│  │ + ignorar()                 │       └─────────────────────────────┘             │
│  └─────────────────────────────┘                                                   │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Enumerações (Enums)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   ENUMERAÇÕES                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  <<enum>>                    <<enum>>                    <<enum>>                   │
│  PorteEnum                   ModalidadeEnum             TipoRequisitoEnum          │
│  ─────────────               ─────────────              ─────────────────          │
│  MEI                         PREGAO_ELETRONICO          OBRIGATORIO                │
│  ME                          PREGAO_PRESENCIAL          DESEJAVEL                  │
│  EPP                         CONCORRENCIA                                          │
│  MEDIO                       TOMADA_PRECOS                                         │
│  GRANDE                      CONVITE                                               │
│                              CONCURSO                                              │
│                              LEILAO                                                │
│                              DIALOGO_COMPETITIVO                                   │
│                                                                                     │
│  <<enum>>                    <<enum>>                    <<enum>>                   │
│  AreaEnum                    NivelEnum                  SeveridadeEnum             │
│  ─────────                   ─────────                  ──────────────             │
│  TECNICA                     BASICO                     CRITICO                    │
│  FINANCEIRA                  INTERMEDIARIO              ALTO                       │
│  JURIDICA                    AVANCADO                   MEDIO                      │
│  ADMINISTRATIVA              ESPECIALISTA               BAIXO                      │
│                                                                                     │
│  <<enum>>                    <<enum>>                    <<enum>>                   │
│  RecomendacaoEnum            StatusEditalEnum           StatusAnaliseEnum          │
│  ───────────────             ────────────────           ─────────────────          │
│  PARTICIPAR                  NOVO                       RASCUNHO                   │
│  AVALIAR                     PROCESSANDO                FINALIZADA                 │
│  NAO_PARTICIPAR              ANALISADO                  ARQUIVADA                  │
│                              ARQUIVADO                                             │
│                                                                                     │
│  <<enum>>                    <<enum>>                    <<enum>>                   │
│  TipoDocumentoEnum           TipoCertificacaoEnum       StatusMatchEnum            │
│  ─────────────────           ──────────────────         ───────────────            │
│  CND_FEDERAL                 CERTIFICADO                ATENDE                     │
│  CND_ESTADUAL                ATESTADO                   NAO_ATENDE                 │
│  CND_MUNICIPAL               REGISTRO                   PARCIAL                    │
│  CND_TRABALHISTA             LICENCA                                               │
│  FGTS                        OUTRO                                                 │
│  BALANCO                                                                           │
│  CONTRATO_SOCIAL                                                                   │
│  ALVARA                                                                            │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

*Diagrama ER elaborado em Novembro/2024.*
