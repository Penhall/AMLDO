# Modelo de Dados
## LicitaFit - Sistema de Análise de Aderência a Editais

**Versão:** 1.0
**Data:** Novembro/2024

---

## 1. Visão Geral

### 1.1 Filosofia do Modelo

O modelo de dados do LicitaFit foi inspirado no projeto **StudentDataBank**, adaptando conceitos de equivalência curricular para o domínio de licitações:

| StudentDataBank | LicitaFit | Conceito |
|-----------------|-----------|----------|
| EducationalInstitute | Empresa | Entidade principal |
| Program | ProcessoLicitatorio | Contexto de avaliação |
| Course | Capacidade | O que a entidade oferece |
| UniversalCourse | CategoriaUniversal | Padronização entre entidades |
| ProgramRequiredCourse | Requisito | O que é exigido |
| CourseCredited | RequisitoAtendido | Matching entre oferta e demanda |

### 1.2 Diagrama Geral

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MODELO DE DADOS - LICITAFIT                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌──────────┐         ┌──────────┐         ┌───────────────┐             │
│    │ EMPRESA  │1───────N│CAPACIDADE│N───────1│CATEGORIA_UNIV │             │
│    └──────────┘         └──────────┘         └───────────────┘             │
│         │                                            │                      │
│         │1                                           │                      │
│         │                                            │1                     │
│         │N                                           │                      │
│    ┌──────────┐                              ┌──────────────┐               │
│    │CERTIFICAO│                              │   REQUISITO  │               │
│    └──────────┘                              └──────────────┘               │
│         │                                            │N                     │
│         │N                                           │                      │
│         │                                            │1                     │
│         │1                                           │                      │
│    ┌──────────┐         ┌──────────┐         ┌──────────────┐               │
│    │DOCUMENTO │         │  EDITAL  │1───────N│   SECAO      │               │
│    └──────────┘         └──────────┘         └──────────────┘               │
│                               │                                             │
│                               │1                                            │
│                               │                                             │
│                               │N                                            │
│                         ┌──────────┐         ┌──────────────┐               │
│                         │ ANALISE  │1───────N│     GAP      │               │
│                         └──────────┘         └──────────────┘               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Entidades de Empresa

### 2.1 Empresa

Representa a empresa licitante que utiliza o sistema.

```sql
CREATE TABLE empresa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cnpj VARCHAR(18) NOT NULL UNIQUE,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    porte VARCHAR(20) NOT NULL,  -- MEI, ME, EPP, MEDIO, GRANDE
    ramo_atividade VARCHAR(100),
    cnae_principal VARCHAR(10),
    endereco_logradouro VARCHAR(255),
    endereco_numero VARCHAR(20),
    endereco_complemento VARCHAR(100),
    endereco_bairro VARCHAR(100),
    endereco_cidade VARCHAR(100),
    endereco_uf CHAR(2),
    endereco_cep VARCHAR(10),
    telefone VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(255),
    data_fundacao DATE,
    capital_social DECIMAL(15,2),
    num_funcionarios INTEGER,
    ativa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_empresa_cnpj ON empresa(cnpj);
CREATE INDEX idx_empresa_porte ON empresa(porte);
CREATE INDEX idx_empresa_ramo ON empresa(ramo_atividade);
```

**Campos Importantes:**

| Campo | Tipo | Descrição | Obrigatório |
|-------|------|-----------|-------------|
| cnpj | VARCHAR(18) | CNPJ formatado (XX.XXX.XXX/XXXX-XX) | Sim |
| razao_social | VARCHAR(255) | Nome oficial da empresa | Sim |
| porte | VARCHAR(20) | Classificação por tamanho | Sim |
| cnae_principal | VARCHAR(10) | Código CNAE principal | Não |

### 2.2 Capacidade

Representa as competências e experiências da empresa.

```sql
CREATE TABLE capacidade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_id INTEGER NOT NULL,
    categoria_universal_id INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    nivel VARCHAR(20) DEFAULT 'INTERMEDIARIO',  -- BASICO, INTERMEDIARIO, AVANCADO, ESPECIALISTA
    anos_experiencia INTEGER DEFAULT 0,
    quantidade_projetos INTEGER DEFAULT 0,
    valor_total_projetos DECIMAL(15,2),
    observacoes TEXT,
    comprovante_path VARCHAR(500),
    ativa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empresa_id) REFERENCES empresa(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_universal_id) REFERENCES categoria_universal(id)
);

-- Índices
CREATE INDEX idx_capacidade_empresa ON capacidade(empresa_id);
CREATE INDEX idx_capacidade_categoria ON capacidade(categoria_universal_id);
CREATE INDEX idx_capacidade_nivel ON capacidade(nivel);
```

### 2.3 Certificacao

Representa certificados, atestados e qualificações da empresa.

```sql
CREATE TABLE certificacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_id INTEGER NOT NULL,
    categoria_universal_id INTEGER,
    tipo VARCHAR(50) NOT NULL,  -- CERTIFICADO, ATESTADO, REGISTRO, LICENCA, OUTRO
    nome VARCHAR(255) NOT NULL,
    emissor VARCHAR(255) NOT NULL,
    numero_registro VARCHAR(100),
    data_emissao DATE NOT NULL,
    data_validade DATE,
    escopo TEXT,
    arquivo_path VARCHAR(500),
    arquivo_hash VARCHAR(64),  -- SHA-256 do arquivo
    status VARCHAR(20) DEFAULT 'VALIDO',  -- VALIDO, VENCIDO, REVOGADO
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empresa_id) REFERENCES empresa(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_universal_id) REFERENCES categoria_universal(id)
);

-- Índices
CREATE INDEX idx_certificacao_empresa ON certificacao(empresa_id);
CREATE INDEX idx_certificacao_tipo ON certificacao(tipo);
CREATE INDEX idx_certificacao_validade ON certificacao(data_validade);
CREATE INDEX idx_certificacao_status ON certificacao(status);
```

### 2.4 Documento

Representa documentos gerais da empresa (contrato social, certidões, etc.).

```sql
CREATE TABLE documento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_id INTEGER NOT NULL,
    tipo VARCHAR(50) NOT NULL,  -- Ver tabela de tipos abaixo
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    arquivo_path VARCHAR(500) NOT NULL,
    arquivo_hash VARCHAR(64),
    tamanho_bytes INTEGER,
    data_emissao DATE,
    data_validade DATE,
    orgao_emissor VARCHAR(255),
    numero_documento VARCHAR(100),
    status VARCHAR(20) DEFAULT 'VALIDO',
    alertar_vencimento BOOLEAN DEFAULT TRUE,
    dias_antecedencia_alerta INTEGER DEFAULT 30,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empresa_id) REFERENCES empresa(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_documento_empresa ON documento(empresa_id);
CREATE INDEX idx_documento_tipo ON documento(tipo);
CREATE INDEX idx_documento_validade ON documento(data_validade);
```

**Tipos de Documento:**

| Código | Descrição |
|--------|-----------|
| CONTRATO_SOCIAL | Contrato Social / Estatuto |
| CND_FEDERAL | Certidão Negativa Federal |
| CND_ESTADUAL | Certidão Negativa Estadual |
| CND_MUNICIPAL | Certidão Negativa Municipal |
| CND_TRABALHISTA | Certidão Negativa Trabalhista |
| FGTS | Certificado de Regularidade FGTS |
| BALANCO | Balanço Patrimonial |
| ALVARA | Alvará de Funcionamento |
| REGISTRO_CLASSE | Registro em Conselho de Classe |
| OUTRO | Outros Documentos |

---

## 3. Entidades de Categorização

### 3.1 CategoriaUniversal

Representa categorias padronizadas para mapeamento de capacidades e requisitos.

```sql
CREATE TABLE categoria_universal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    area VARCHAR(50) NOT NULL,  -- TECNICA, FINANCEIRA, JURIDICA, ADMINISTRATIVA
    subarea VARCHAR(50),
    nivel_hierarquia INTEGER DEFAULT 1,
    categoria_pai_id INTEGER,
    keywords TEXT,  -- Palavras-chave para matching (separadas por vírgula)
    ativa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_pai_id) REFERENCES categoria_universal(id)
);

-- Índices
CREATE INDEX idx_categoria_codigo ON categoria_universal(codigo);
CREATE INDEX idx_categoria_area ON categoria_universal(area);
CREATE INDEX idx_categoria_pai ON categoria_universal(categoria_pai_id);
```

**Exemplo de Hierarquia de Categorias:**

```
AREA: TECNICA
├── TEC.001 - Tecnologia da Informação
│   ├── TEC.001.001 - Desenvolvimento de Software
│   ├── TEC.001.002 - Infraestrutura de TI
│   └── TEC.001.003 - Segurança da Informação
├── TEC.002 - Engenharia Civil
│   ├── TEC.002.001 - Construção
│   └── TEC.002.002 - Manutenção Predial
└── TEC.003 - Serviços Gerais
    ├── TEC.003.001 - Limpeza
    └── TEC.003.002 - Vigilância

AREA: FINANCEIRA
├── FIN.001 - Capital Social Mínimo
├── FIN.002 - Patrimônio Líquido
└── FIN.003 - Índices Financeiros

AREA: JURIDICA
├── JUR.001 - Regularidade Fiscal
├── JUR.002 - Regularidade Trabalhista
└── JUR.003 - Capacidade Jurídica
```

### 3.2 SinonimoCategoria

Permite mapeamento de termos encontrados em editais para categorias universais.

```sql
CREATE TABLE sinonimo_categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_universal_id INTEGER NOT NULL,
    termo VARCHAR(255) NOT NULL,
    peso FLOAT DEFAULT 1.0,  -- Peso para ranking de similaridade
    origem VARCHAR(50),  -- MANUAL, AUTOMATICO, RAG
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_universal_id) REFERENCES categoria_universal(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_sinonimo_categoria ON sinonimo_categoria(categoria_universal_id);
CREATE INDEX idx_sinonimo_termo ON sinonimo_categoria(termo);
```

---

## 4. Entidades de Edital

### 4.1 Edital

Representa um edital de licitação importado para análise.

```sql
CREATE TABLE edital (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_id INTEGER NOT NULL,  -- Empresa que está analisando
    numero VARCHAR(100) NOT NULL,
    ano INTEGER,
    orgao VARCHAR(255) NOT NULL,
    uasg VARCHAR(20),  -- Código UASG (órgãos federais)
    modalidade VARCHAR(50) NOT NULL,  -- PREGAO_ELETRONICO, CONCORRENCIA, etc.
    tipo VARCHAR(50),  -- MENOR_PRECO, TECNICA_PRECO, etc.
    natureza VARCHAR(50),  -- COMPRA, SERVICO, OBRA
    objeto TEXT NOT NULL,
    objeto_resumido VARCHAR(500),
    valor_estimado DECIMAL(15,2),
    data_publicacao DATE,
    data_abertura DATETIME,
    data_limite_proposta DATETIME,
    local_entrega VARCHAR(500),
    prazo_execucao VARCHAR(100),
    garantia_proposta_percentual DECIMAL(5,2),
    garantia_contrato_percentual DECIMAL(5,2),
    arquivo_path VARCHAR(500) NOT NULL,
    arquivo_hash VARCHAR(64),
    texto_extraido TEXT,
    num_paginas INTEGER,
    status VARCHAR(20) DEFAULT 'NOVO',  -- NOVO, PROCESSANDO, ANALISADO, ARQUIVADO
    portal_origem VARCHAR(100),  -- ComprasNet, BEC, etc.
    url_origem VARCHAR(500),
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empresa_id) REFERENCES empresa(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_edital_empresa ON edital(empresa_id);
CREATE INDEX idx_edital_numero ON edital(numero);
CREATE INDEX idx_edital_orgao ON edital(orgao);
CREATE INDEX idx_edital_modalidade ON edital(modalidade);
CREATE INDEX idx_edital_data_abertura ON edital(data_abertura);
CREATE INDEX idx_edital_status ON edital(status);
```

**Modalidades de Licitação:**

| Código | Descrição |
|--------|-----------|
| PREGAO_ELETRONICO | Pregão Eletrônico |
| PREGAO_PRESENCIAL | Pregão Presencial |
| CONCORRENCIA | Concorrência |
| TOMADA_PRECOS | Tomada de Preços |
| CONVITE | Convite |
| CONCURSO | Concurso |
| LEILAO | Leilão |
| DIALOGO_COMPETITIVO | Diálogo Competitivo |
| RDC | Regime Diferenciado de Contratações |

### 4.2 SecaoEdital

Representa seções identificadas no edital.

```sql
CREATE TABLE secao_edital (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    edital_id INTEGER NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    numero_secao VARCHAR(50),
    texto TEXT NOT NULL,
    pagina_inicio INTEGER,
    pagina_fim INTEGER,
    tipo VARCHAR(50),  -- OBJETO, HABILITACAO, PROPOSTA, JULGAMENTO, etc.
    ordem INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (edital_id) REFERENCES edital(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_secao_edital ON secao_edital(edital_id);
CREATE INDEX idx_secao_tipo ON secao_edital(tipo);
```

### 4.3 Requisito

Representa requisitos extraídos do edital.

```sql
CREATE TABLE requisito (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    edital_id INTEGER NOT NULL,
    secao_edital_id INTEGER,
    categoria_universal_id INTEGER,
    tipo VARCHAR(20) NOT NULL,  -- OBRIGATORIO, DESEJAVEL, PONTUACAO
    area VARCHAR(50) NOT NULL,  -- TECNICA, FINANCEIRA, JURIDICA, ADMINISTRATIVA
    descricao TEXT NOT NULL,
    texto_original TEXT NOT NULL,
    criterio_avaliacao TEXT,
    valor_minimo DECIMAL(15,2),
    valor_maximo DECIMAL(15,2),
    unidade VARCHAR(50),
    pagina INTEGER,
    confianca_extracao FLOAT DEFAULT 1.0,  -- Score de confiança do RAG
    validado_usuario BOOLEAN DEFAULT FALSE,
    atendido BOOLEAN,  -- NULL = não avaliado, TRUE = atende, FALSE = não atende
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (edital_id) REFERENCES edital(id) ON DELETE CASCADE,
    FOREIGN KEY (secao_edital_id) REFERENCES secao_edital(id),
    FOREIGN KEY (categoria_universal_id) REFERENCES categoria_universal(id)
);

-- Índices
CREATE INDEX idx_requisito_edital ON requisito(edital_id);
CREATE INDEX idx_requisito_tipo ON requisito(tipo);
CREATE INDEX idx_requisito_area ON requisito(area);
CREATE INDEX idx_requisito_categoria ON requisito(categoria_universal_id);
CREATE INDEX idx_requisito_atendido ON requisito(atendido);
```

---

## 5. Entidades de Análise

### 5.1 Analise

Representa uma análise de aderência empresa x edital.

```sql
CREATE TABLE analise (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_id INTEGER NOT NULL,
    edital_id INTEGER NOT NULL,
    data_analise TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Scores
    score_global FLOAT NOT NULL,  -- 0.0 a 100.0
    score_obrigatorios FLOAT NOT NULL,
    score_desejaveis FLOAT,
    score_tecnico FLOAT,
    score_financeiro FLOAT,
    score_juridico FLOAT,

    -- Contadores
    total_requisitos INTEGER NOT NULL,
    requisitos_obrigatorios INTEGER NOT NULL,
    requisitos_desejaveis INTEGER,
    requisitos_atendidos INTEGER NOT NULL,
    requisitos_nao_atendidos INTEGER NOT NULL,
    requisitos_parciais INTEGER DEFAULT 0,
    requisitos_nao_avaliados INTEGER DEFAULT 0,

    -- Resultado
    recomendacao VARCHAR(20) NOT NULL,  -- PARTICIPAR, NAO_PARTICIPAR, AVALIAR
    justificativa_recomendacao TEXT,
    nivel_risco VARCHAR(20),  -- BAIXO, MEDIO, ALTO, CRITICO

    -- Metadados
    status VARCHAR(20) DEFAULT 'RASCUNHO',  -- RASCUNHO, FINALIZADA, ARQUIVADA
    usuario_responsavel VARCHAR(100),
    observacoes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empresa_id) REFERENCES empresa(id) ON DELETE CASCADE,
    FOREIGN KEY (edital_id) REFERENCES edital(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_analise_empresa ON analise(empresa_id);
CREATE INDEX idx_analise_edital ON analise(edital_id);
CREATE INDEX idx_analise_score ON analise(score_global);
CREATE INDEX idx_analise_recomendacao ON analise(recomendacao);
CREATE INDEX idx_analise_status ON analise(status);

-- Constraint de unicidade
CREATE UNIQUE INDEX idx_analise_empresa_edital ON analise(empresa_id, edital_id);
```

### 5.2 Gap

Representa gaps identificados na análise (requisitos não atendidos).

```sql
CREATE TABLE gap (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analise_id INTEGER NOT NULL,
    requisito_id INTEGER NOT NULL,

    -- Classificação
    tipo VARCHAR(20) NOT NULL,  -- TOTAL, PARCIAL
    severidade VARCHAR(20) NOT NULL,  -- CRITICO, ALTO, MEDIO, BAIXO
    impacto_score FLOAT,  -- Impacto no score se atendido

    -- Descrição
    descricao TEXT NOT NULL,
    motivo_nao_atendimento TEXT,

    -- Recomendação
    recomendacao TEXT,
    acao_sugerida TEXT,
    prazo_estimado VARCHAR(100),
    custo_estimado DECIMAL(15,2),
    dificuldade VARCHAR(20),  -- FACIL, MEDIO, DIFICIL, MUITO_DIFICIL

    -- Tracking
    status VARCHAR(20) DEFAULT 'PENDENTE',  -- PENDENTE, EM_ANDAMENTO, RESOLVIDO, IGNORADO
    data_resolucao TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (analise_id) REFERENCES analise(id) ON DELETE CASCADE,
    FOREIGN KEY (requisito_id) REFERENCES requisito(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_gap_analise ON gap(analise_id);
CREATE INDEX idx_gap_requisito ON gap(requisito_id);
CREATE INDEX idx_gap_severidade ON gap(severidade);
CREATE INDEX idx_gap_status ON gap(status);
```

### 5.3 MatchRequisitoCapacidade

Representa o matching entre requisitos do edital e capacidades da empresa.

```sql
CREATE TABLE match_requisito_capacidade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analise_id INTEGER NOT NULL,
    requisito_id INTEGER NOT NULL,
    capacidade_id INTEGER,
    certificacao_id INTEGER,
    documento_id INTEGER,

    -- Match
    tipo_match VARCHAR(20) NOT NULL,  -- AUTOMATICO, MANUAL
    score_match FLOAT,  -- 0.0 a 1.0
    status_match VARCHAR(20) NOT NULL,  -- ATENDE, NAO_ATENDE, PARCIAL

    -- Detalhes
    justificativa TEXT,
    observacoes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (analise_id) REFERENCES analise(id) ON DELETE CASCADE,
    FOREIGN KEY (requisito_id) REFERENCES requisito(id) ON DELETE CASCADE,
    FOREIGN KEY (capacidade_id) REFERENCES capacidade(id),
    FOREIGN KEY (certificacao_id) REFERENCES certificacao(id),
    FOREIGN KEY (documento_id) REFERENCES documento(id)
);

-- Índices
CREATE INDEX idx_match_analise ON match_requisito_capacidade(analise_id);
CREATE INDEX idx_match_requisito ON match_requisito_capacidade(requisito_id);
CREATE INDEX idx_match_status ON match_requisito_capacidade(status_match);
```

---

## 6. Entidades de Suporte

### 6.1 Configuracao

Armazena configurações do sistema.

```sql
CREATE TABLE configuracao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chave VARCHAR(100) NOT NULL UNIQUE,
    valor TEXT,
    tipo VARCHAR(20) DEFAULT 'STRING',  -- STRING, INTEGER, FLOAT, BOOLEAN, JSON
    descricao TEXT,
    editavel BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Configurações padrão
INSERT INTO configuracao (chave, valor, tipo, descricao) VALUES
('app.theme', 'light', 'STRING', 'Tema da aplicação'),
('app.language', 'pt-BR', 'STRING', 'Idioma da aplicação'),
('analise.score_minimo_participar', '70', 'INTEGER', 'Score mínimo para recomendar participação'),
('analise.score_minimo_avaliar', '50', 'INTEGER', 'Score mínimo para recomendar avaliação'),
('documento.dias_alerta_vencimento', '30', 'INTEGER', 'Dias de antecedência para alertar vencimento'),
('backup.automatico', 'true', 'BOOLEAN', 'Realizar backup automático'),
('backup.intervalo_dias', '7', 'INTEGER', 'Intervalo entre backups automáticos');
```

### 6.2 LogAuditoria

Registra ações importantes para auditoria.

```sql
CREATE TABLE log_auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario VARCHAR(100),
    acao VARCHAR(50) NOT NULL,  -- CREATE, UPDATE, DELETE, VIEW, EXPORT, etc.
    entidade VARCHAR(50) NOT NULL,  -- empresa, edital, analise, etc.
    entidade_id INTEGER,
    dados_antes TEXT,  -- JSON
    dados_depois TEXT,  -- JSON
    ip_address VARCHAR(45),
    descricao TEXT
);

-- Índices
CREATE INDEX idx_log_timestamp ON log_auditoria(timestamp);
CREATE INDEX idx_log_acao ON log_auditoria(acao);
CREATE INDEX idx_log_entidade ON log_auditoria(entidade, entidade_id);
```

### 6.3 Alerta

Gerencia alertas do sistema (vencimentos, pendências, etc.).

```sql
CREATE TABLE alerta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_id INTEGER NOT NULL,
    tipo VARCHAR(50) NOT NULL,  -- VENCIMENTO_DOCUMENTO, EDITAL_PROXIMO, GAP_PENDENTE
    prioridade VARCHAR(20) DEFAULT 'MEDIA',  -- BAIXA, MEDIA, ALTA, CRITICA
    titulo VARCHAR(255) NOT NULL,
    mensagem TEXT NOT NULL,
    entidade_relacionada VARCHAR(50),
    entidade_id INTEGER,
    data_referencia DATE,
    lido BOOLEAN DEFAULT FALSE,
    descartado BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empresa_id) REFERENCES empresa(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_alerta_empresa ON alerta(empresa_id);
CREATE INDEX idx_alerta_tipo ON alerta(tipo);
CREATE INDEX idx_alerta_lido ON alerta(lido);
CREATE INDEX idx_alerta_data ON alerta(data_referencia);
```

---

## 7. Views e Queries Importantes

### 7.1 View de Documentos Próximos do Vencimento

```sql
CREATE VIEW vw_documentos_vencendo AS
SELECT
    d.id,
    d.nome,
    d.tipo,
    d.data_validade,
    e.razao_social AS empresa,
    julianday(d.data_validade) - julianday('now') AS dias_para_vencer
FROM documento d
JOIN empresa e ON d.empresa_id = e.id
WHERE d.data_validade IS NOT NULL
  AND d.status = 'VALIDO'
  AND d.data_validade <= date('now', '+30 days')
ORDER BY d.data_validade;
```

### 7.2 View de Resumo de Análises

```sql
CREATE VIEW vw_resumo_analises AS
SELECT
    a.id,
    e.razao_social AS empresa,
    ed.numero AS numero_edital,
    ed.orgao,
    ed.objeto_resumido,
    a.score_global,
    a.recomendacao,
    a.total_requisitos,
    a.requisitos_atendidos,
    a.data_analise,
    a.status
FROM analise a
JOIN empresa e ON a.empresa_id = e.id
JOIN edital ed ON a.edital_id = ed.id
ORDER BY a.data_analise DESC;
```

### 7.3 Query de Gaps Críticos

```sql
SELECT
    g.id,
    e.razao_social AS empresa,
    ed.numero AS edital,
    r.descricao AS requisito,
    g.severidade,
    g.descricao AS gap_descricao,
    g.recomendacao,
    g.status
FROM gap g
JOIN analise a ON g.analise_id = a.id
JOIN empresa e ON a.empresa_id = e.id
JOIN edital ed ON a.edital_id = ed.id
JOIN requisito r ON g.requisito_id = r.id
WHERE g.severidade IN ('CRITICO', 'ALTO')
  AND g.status = 'PENDENTE'
ORDER BY
    CASE g.severidade
        WHEN 'CRITICO' THEN 1
        WHEN 'ALTO' THEN 2
        ELSE 3
    END,
    a.data_analise DESC;
```

---

## 8. Migração e Versionamento

### 8.1 Tabela de Controle de Versão

```sql
CREATE TABLE schema_version (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version VARCHAR(20) NOT NULL,
    description TEXT,
    script_name VARCHAR(255),
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT TRUE
);
```

### 8.2 Exemplo de Script de Migração

```sql
-- Migration: 001_initial_schema.sql
-- Description: Criação do schema inicial

BEGIN TRANSACTION;

-- Criar tabelas...

INSERT INTO schema_version (version, description, script_name)
VALUES ('1.0.0', 'Schema inicial', '001_initial_schema.sql');

COMMIT;
```

---

## 9. Dados de Referência

### 9.1 Categorias Universais Iniciais

```sql
INSERT INTO categoria_universal (codigo, nome, descricao, area, subarea) VALUES
-- Técnica - TI
('TEC.TI.001', 'Desenvolvimento de Software', 'Desenvolvimento de sistemas e aplicações', 'TECNICA', 'TECNOLOGIA_INFORMACAO'),
('TEC.TI.002', 'Infraestrutura de TI', 'Servidores, redes, datacenter', 'TECNICA', 'TECNOLOGIA_INFORMACAO'),
('TEC.TI.003', 'Suporte Técnico', 'Help desk, suporte a usuários', 'TECNICA', 'TECNOLOGIA_INFORMACAO'),
('TEC.TI.004', 'Segurança da Informação', 'Cibersegurança, LGPD', 'TECNICA', 'TECNOLOGIA_INFORMACAO'),

-- Técnica - Engenharia
('TEC.ENG.001', 'Construção Civil', 'Obras, reformas, construções', 'TECNICA', 'ENGENHARIA'),
('TEC.ENG.002', 'Engenharia Elétrica', 'Instalações elétricas, manutenção', 'TECNICA', 'ENGENHARIA'),
('TEC.ENG.003', 'Engenharia Mecânica', 'Equipamentos, manutenção industrial', 'TECNICA', 'ENGENHARIA'),

-- Técnica - Serviços
('TEC.SVC.001', 'Limpeza e Conservação', 'Serviços de limpeza predial', 'TECNICA', 'SERVICOS'),
('TEC.SVC.002', 'Vigilância', 'Segurança patrimonial', 'TECNICA', 'SERVICOS'),
('TEC.SVC.003', 'Transporte', 'Logística, frete, transporte', 'TECNICA', 'SERVICOS'),

-- Financeira
('FIN.001', 'Capital Social', 'Capital social mínimo exigido', 'FINANCEIRA', NULL),
('FIN.002', 'Patrimônio Líquido', 'Patrimônio líquido mínimo', 'FINANCEIRA', NULL),
('FIN.003', 'Faturamento', 'Faturamento mínimo anual', 'FINANCEIRA', NULL),
('FIN.004', 'Índices Contábeis', 'Liquidez, endividamento, etc.', 'FINANCEIRA', NULL),

-- Jurídica
('JUR.001', 'Regularidade Fiscal Federal', 'CND Federal, Previdência', 'JURIDICA', NULL),
('JUR.002', 'Regularidade Fiscal Estadual', 'CND Estadual', 'JURIDICA', NULL),
('JUR.003', 'Regularidade Fiscal Municipal', 'CND Municipal', 'JURIDICA', NULL),
('JUR.004', 'Regularidade Trabalhista', 'CNDT, FGTS', 'JURIDICA', NULL),
('JUR.005', 'Capacidade Jurídica', 'Contrato social, procurações', 'JURIDICA', NULL);
```

---

## 10. Considerações de Performance

### 10.1 Índices Recomendados

Todos os índices importantes já estão definidos nas tabelas acima. Principais critérios:
- Chaves estrangeiras (FK)
- Campos usados em WHERE frequentes
- Campos usados em ORDER BY
- Campos usados em GROUP BY

### 10.2 Estratégias de Otimização

| Cenário | Estratégia |
|---------|------------|
| Busca em texto | FTS5 (Full-Text Search) do SQLite |
| Cache de queries | Application-level cache |
| Dados históricos | Particionamento por data (manual) |
| Relatórios pesados | Views materializadas (manual) |

---

*Modelo de dados elaborado em Novembro/2024 como parte do planejamento do projeto LicitaFit.*
