# Arquitetura Técnica
## LicitaFit - Sistema de Análise de Aderência a Editais

**Versão:** 1.0
**Data:** Novembro/2024

---

## 1. Visão Geral da Arquitetura

### 1.1 Princípios Arquiteturais

| Princípio | Descrição | Justificativa |
|-----------|-----------|---------------|
| **Desktop First** | Aplicação nativa para Windows | Performance, offline, segurança |
| **Offline Capable** | Funciona 100% sem internet | Dados sensíveis ficam locais |
| **Modular** | Componentes independentes | Manutenibilidade, testabilidade |
| **Extensível** | Plugins e customizações | Evolução do produto |
| **Seguro** | Criptografia local | LGPD, dados empresariais |

### 1.2 Arquitetura de Alto Nível

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           LicitaFit Desktop Application                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        CAMADA DE APRESENTAÇÃO                        │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────────────┐ │   │
│  │  │  Tela de  │  │  Tela de  │  │  Tela de  │  │  Tela de         │ │   │
│  │  │  Perfil   │  │  Editais  │  │  Análise  │  │  Relatórios      │ │   │
│  │  └───────────┘  └───────────┘  └───────────┘  └───────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        CAMADA DE APLICAÇÃO                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │   │
│  │  │  Perfil     │  │  Edital     │  │  Análise    │  │  Relatório │ │   │
│  │  │  Service    │  │  Service    │  │  Service    │  │  Service   │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        CAMADA DE DOMÍNIO                            │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │   │
│  │  │  Empresa    │  │  Edital     │  │  Requisito  │  │  Score     │ │   │
│  │  │  Entity     │  │  Entity     │  │  Entity     │  │  Calculator│ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      CAMADA DE INFRAESTRUTURA                       │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌──────────────────┐ │   │
│  │  │  SQLite   │  │  PDF      │  │  RAG      │  │  File System     │ │   │
│  │  │  Storage  │  │  Parser   │  │  Engine   │  │  Manager         │ │   │
│  │  └───────────┘  └───────────┘  └───────────┘  └──────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              RECURSOS EXTERNOS                              │
│  ┌───────────────────┐  ┌───────────────────┐  ┌──────────────────────────┐│
│  │  AMLDO RAG Engine │  │  Modelo Embeddings │  │  Arquivos Locais (PDF)  ││
│  │  (Integrado)      │  │  (Local)           │  │                         ││
│  └───────────────────┘  └───────────────────┘  └──────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes do Sistema

### 2.1 Camada de Apresentação (UI)

#### Framework Recomendado: PyQt6

```python
# Estrutura de módulos UI
src/licitafit/
└── ui/
    ├── __init__.py
    ├── main_window.py          # Janela principal
    ├── widgets/
    │   ├── __init__.py
    │   ├── empresa_widget.py   # Widget de perfil da empresa
    │   ├── edital_widget.py    # Widget de editais
    │   ├── analise_widget.py   # Widget de análise
    │   └── relatorio_widget.py # Widget de relatórios
    ├── dialogs/
    │   ├── __init__.py
    │   ├── empresa_dialog.py   # Diálogo de cadastro de empresa
    │   ├── documento_dialog.py # Diálogo de upload de documento
    │   └── config_dialog.py    # Diálogo de configurações
    └── resources/
        ├── icons/
        ├── styles/
        └── images/
```

#### Componentes de UI

| Componente | Responsabilidade | Tecnologia |
|------------|------------------|------------|
| MainWindow | Container principal, navegação | PyQt6 QMainWindow |
| EmpresaWidget | Visualização e edição de perfil | PyQt6 QWidget |
| EditalWidget | Upload e visualização de editais | PyQt6 QWidget |
| AnaliseWidget | Exibição de score e gaps | PyQt6 QWidget |
| RelatorioWidget | Geração e preview de relatórios | PyQt6 QWidget |

### 2.2 Camada de Aplicação (Services)

```python
# Estrutura de serviços
src/licitafit/
└── services/
    ├── __init__.py
    ├── empresa_service.py      # CRUD de empresas
    ├── edital_service.py       # Processamento de editais
    ├── analise_service.py      # Cálculo de aderência
    ├── relatorio_service.py    # Geração de relatórios
    ├── documento_service.py    # Gestão de documentos
    └── backup_service.py       # Backup e restauração
```

#### Serviços Principais

| Serviço | Responsabilidade | Métodos Principais |
|---------|------------------|-------------------|
| EmpresaService | Gestão de perfil da empresa | create, update, delete, get |
| EditalService | Processamento de PDFs | upload, extract_text, parse |
| AnaliseService | Cálculo de aderência | analyze, calculate_score, identify_gaps |
| RelatorioService | Geração de relatórios | generate_pdf, generate_excel |
| DocumentoService | Gestão de arquivos | upload, validate, check_expiry |
| BackupService | Backup de dados | backup, restore, export |

### 2.3 Camada de Domínio (Entities)

```python
# Estrutura de entidades
src/licitafit/
└── domain/
    ├── __init__.py
    ├── entities/
    │   ├── __init__.py
    │   ├── empresa.py          # Entidade Empresa
    │   ├── capacidade.py       # Entidade Capacidade
    │   ├── certificacao.py     # Entidade Certificação
    │   ├── edital.py           # Entidade Edital
    │   ├── requisito.py        # Entidade Requisito
    │   ├── analise.py          # Entidade Análise
    │   └── documento.py        # Entidade Documento
    ├── value_objects/
    │   ├── __init__.py
    │   ├── cnpj.py             # Value Object CNPJ
    │   ├── score.py            # Value Object Score
    │   └── categoria.py        # Value Object Categoria
    └── repositories/
        ├── __init__.py
        ├── empresa_repository.py
        ├── edital_repository.py
        └── analise_repository.py
```

### 2.4 Camada de Infraestrutura

```python
# Estrutura de infraestrutura
src/licitafit/
└── infrastructure/
    ├── __init__.py
    ├── database/
    │   ├── __init__.py
    │   ├── connection.py       # Conexão SQLite
    │   ├── migrations/         # Migrações de schema
    │   └── models.py           # Modelos ORM (SQLAlchemy)
    ├── pdf/
    │   ├── __init__.py
    │   ├── extractor.py        # Extração de texto de PDF
    │   └── parser.py           # Parser de estrutura
    ├── rag/
    │   ├── __init__.py
    │   ├── engine.py           # Motor RAG integrado
    │   └── embeddings.py       # Gerador de embeddings
    └── filesystem/
        ├── __init__.py
        ├── storage.py          # Gerenciamento de arquivos
        └── crypto.py           # Criptografia local
```

---

## 3. Modelo de Dados

### 3.1 Diagrama Entidade-Relacionamento Simplificado

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     EMPRESA     │       │   CAPACIDADE    │       │  CERTIFICACAO   │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ cnpj            │1     N│ empresa_id (FK) │       │ empresa_id (FK) │
│ razao_social    │───────│ categoria_id    │       │ nome            │
│ nome_fantasia   │       │ descricao       │       │ emissor         │
│ porte           │       │ nivel           │       │ data_emissao    │
│ ramo_atividade  │       │ experiencia_anos│       │ data_validade   │
│ created_at      │       │ created_at      │       │ arquivo_path    │
└─────────────────┘       └─────────────────┘       └─────────────────┘
         │                                                    │
         │                                                    │
         │1                                                   │N
         │                                                    │
         ▼                                                    ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     EDITAL      │       │   REQUISITO     │       │   DOCUMENTO     │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ empresa_id (FK) │1     N│ edital_id (FK)  │       │ empresa_id (FK) │
│ numero          │───────│ categoria_id    │       │ tipo            │
│ orgao           │       │ descricao       │       │ nome            │
│ objeto          │       │ tipo (obrig/des)│       │ arquivo_path    │
│ data_abertura   │       │ texto_original  │       │ data_validade   │
│ arquivo_path    │       │ atendido        │       │ created_at      │
│ status          │       │ created_at      │       └─────────────────┘
│ created_at      │       └─────────────────┘
└─────────────────┘                │
         │                         │
         │                         │
         │1                        │N
         │                         │
         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐
│     ANALISE     │       │      GAP        │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ edital_id (FK)  │1     N│ analise_id (FK) │
│ empresa_id (FK) │───────│ requisito_id(FK)│
│ score_global    │       │ descricao       │
│ score_obrig     │       │ severidade      │
│ score_desej     │       │ recomendacao    │
│ data_analise    │       │ created_at      │
│ status          │       └─────────────────┘
└─────────────────┘

┌─────────────────┐       ┌─────────────────┐
│   CATEGORIA     │       │CATEGORIA_UNIV   │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ nome            │N     1│ codigo          │
│ descricao       │───────│ nome            │
│ categoria_univ  │       │ descricao       │
│ (FK)            │       │ area            │
└─────────────────┘       └─────────────────┘
```

### 3.2 Entidades Principais (Detalhado)

#### Empresa

```python
class Empresa:
    """Entidade que representa uma empresa licitante."""

    id: int                      # Identificador único
    cnpj: str                    # CNPJ formatado
    razao_social: str            # Razão social completa
    nome_fantasia: str           # Nome fantasia (opcional)
    porte: PorteEnum             # MEI, ME, EPP, MEDIO, GRANDE
    ramo_atividade: str          # Descrição do ramo
    endereco: str                # Endereço completo
    telefone: str                # Telefone de contato
    email: str                   # Email de contato
    capacidades: List[Capacidade]
    certificacoes: List[Certificacao]
    documentos: List[Documento]
    created_at: datetime
    updated_at: datetime
```

#### Edital

```python
class Edital:
    """Entidade que representa um edital de licitação."""

    id: int                      # Identificador único
    empresa_id: int              # FK para empresa que está analisando
    numero: str                  # Número do edital
    orgao: str                   # Órgão licitante
    modalidade: ModalidadeEnum   # PREGAO, CONCORRENCIA, etc.
    objeto: str                  # Descrição do objeto
    valor_estimado: Decimal      # Valor estimado (opcional)
    data_publicacao: date        # Data de publicação
    data_abertura: datetime      # Data/hora de abertura
    arquivo_path: str            # Caminho do PDF
    texto_extraido: str          # Texto extraído do PDF
    status: StatusEditalEnum     # NOVO, ANALISADO, PARTICIPANDO, etc.
    requisitos: List[Requisito]
    analises: List[Analise]
    created_at: datetime
```

#### Requisito

```python
class Requisito:
    """Entidade que representa um requisito extraído do edital."""

    id: int                      # Identificador único
    edital_id: int               # FK para edital
    categoria_id: int            # FK para categoria universal
    descricao: str               # Descrição do requisito
    texto_original: str          # Texto original do edital
    tipo: TipoRequisitoEnum      # OBRIGATORIO, DESEJAVEL
    secao_edital: str            # Seção onde foi encontrado
    pagina: int                  # Página do PDF
    confianca: float             # Score de confiança da extração
    atendido: Optional[bool]     # Se foi atendido pela empresa
    created_at: datetime
```

#### Análise

```python
class Analise:
    """Entidade que representa uma análise de aderência."""

    id: int                      # Identificador único
    edital_id: int               # FK para edital
    empresa_id: int              # FK para empresa
    score_global: float          # Score geral (0-100)
    score_obrigatorios: float    # Score de requisitos obrigatórios
    score_desejaveis: float      # Score de requisitos desejáveis
    total_requisitos: int        # Total de requisitos
    requisitos_atendidos: int    # Quantidade atendida
    requisitos_pendentes: int    # Quantidade pendente
    recomendacao: RecomendacaoEnum  # PARTICIPAR, NAO_PARTICIPAR, AVALIAR
    observacoes: str             # Observações adicionais
    gaps: List[Gap]              # Lista de gaps identificados
    data_analise: datetime
    status: StatusAnaliseEnum    # RASCUNHO, FINALIZADA
```

---

## 4. Integrações

### 4.1 Integração com AMLDO RAG

O LicitaFit reutilizará o motor RAG do AMLDO para:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    INTEGRAÇÃO LICITAFIT ↔ AMLDO                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  LicitaFit                          AMLDO                          │
│  ┌─────────────┐                    ┌─────────────┐                │
│  │ EditalService│                    │ RAG Engine  │                │
│  │             │     Requisitos     │             │                │
│  │ extract_    │───────────────────▶│ consultar_  │                │
│  │ requisitos()│     + Consulta     │ base_rag()  │                │
│  │             │◀───────────────────│             │                │
│  └─────────────┘     Resposta       └─────────────┘                │
│         │                                  │                        │
│         │                                  │                        │
│         ▼                                  ▼                        │
│  ┌─────────────┐                    ┌─────────────┐                │
│  │ Requisitos  │                    │ Vector DB   │                │
│  │ Extraídos   │                    │ FAISS       │                │
│  └─────────────┘                    └─────────────┘                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Casos de Uso da Integração

| Caso de Uso | Entrada | Saída |
|-------------|---------|-------|
| Extrair requisitos | Texto do edital | Lista de requisitos categorizados |
| Validar requisito | Texto do requisito | Categoria universal correspondente |
| Consultar legislação | Dúvida sobre lei | Resposta contextualizada |
| Verificar conformidade | Requisito + Lei | Parecer de conformidade |

### 4.2 Processamento de PDF

```python
# Fluxo de processamento de PDF
class PDFProcessor:
    """Processador de editais em PDF."""

    def process(self, pdf_path: str) -> ProcessedEdital:
        # 1. Extrair texto
        text = self._extract_text(pdf_path)

        # 2. Identificar estrutura
        sections = self._identify_sections(text)

        # 3. Extrair requisitos via RAG
        requisitos = self._extract_requisitos(sections)

        # 4. Categorizar requisitos
        categorized = self._categorize(requisitos)

        return ProcessedEdital(
            texto=text,
            secoes=sections,
            requisitos=categorized
        )
```

---

## 5. Fluxos de Dados

### 5.1 Fluxo de Análise de Aderência

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FLUXO DE ANÁLISE DE ADERÊNCIA                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. UPLOAD               2. EXTRAÇÃO              3. CATEGORIZAÇÃO          │
│  ┌──────────────┐       ┌──────────────┐         ┌──────────────┐          │
│  │   Usuário    │       │   Sistema    │         │   Sistema    │          │
│  │   faz upload │──────▶│   extrai     │────────▶│   mapeia     │          │
│  │   do PDF     │       │   texto      │         │   categorias │          │
│  └──────────────┘       └──────────────┘         └──────────────┘          │
│                                                          │                  │
│                                                          ▼                  │
│  6. RELATÓRIO            5. SCORE                4. COMPARAÇÃO              │
│  ┌──────────────┐       ┌──────────────┐         ┌──────────────┐          │
│  │   Sistema    │       │   Sistema    │         │   Sistema    │          │
│  │   gera       │◀──────│   calcula    │◀────────│   compara    │          │
│  │   relatório  │       │   score      │         │   com perfil │          │
│  └──────────────┘       └──────────────┘         └──────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Fluxo de Dados Detalhado

```
     INPUT                    PROCESSING                     OUTPUT
┌─────────────┐         ┌─────────────────────┐        ┌─────────────┐
│   PDF do    │         │   PDFProcessor      │        │   Texto     │
│   Edital    │────────▶│   .extract_text()   │───────▶│   Limpo     │
└─────────────┘         └─────────────────────┘        └─────────────┘
                                                              │
                                                              ▼
┌─────────────┐         ┌─────────────────────┐        ┌─────────────┐
│   Texto     │         │   RAGEngine         │        │   Lista de  │
│   Limpo     │────────▶│   .extract_reqs()   │───────▶│   Requisitos│
└─────────────┘         └─────────────────────┘        └─────────────┘
                                                              │
                                                              ▼
┌─────────────┐         ┌─────────────────────┐        ┌─────────────┐
│   Requisitos│         │   Categorizer       │        │   Requisitos│
│   Brutos    │────────▶│   .categorize()     │───────▶│   Categor.  │
└─────────────┘         └─────────────────────┘        └─────────────┘
                                                              │
                                                              ▼
┌─────────────┐         ┌─────────────────────┐        ┌─────────────┐
│   Perfil da │         │   AnaliseService    │        │   Score +   │
│   Empresa   │────────▶│   .compare()        │───────▶│   Gaps      │
└─────────────┘         └─────────────────────┘        └─────────────┘
                                                              │
                                                              ▼
┌─────────────┐         ┌─────────────────────┐        ┌─────────────┐
│   Score +   │         │   RelatorioService  │        │   PDF/Excel │
│   Gaps      │────────▶│   .generate()       │───────▶│   Relatório │
└─────────────┘         └─────────────────────┘        └─────────────┘
```

---

## 6. Segurança

### 6.1 Requisitos de Segurança

| Requisito | Implementação |
|-----------|---------------|
| Autenticação local | Senha com hash bcrypt |
| Criptografia de dados | SQLCipher (SQLite criptografado) |
| Proteção de arquivos | AES-256 para documentos sensíveis |
| Backup seguro | Backup criptografado exportável |
| Auditoria | Log de ações do usuário |

### 6.2 Modelo de Segurança

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MODELO DE SEGURANÇA                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────┐   │
│  │   Usuário   │     │   Camada    │     │   Dados Sensíveis   │   │
│  │   (Senha)   │────▶│   Auth      │────▶│   (Criptografados)  │   │
│  └─────────────┘     └─────────────┘     └─────────────────────┘   │
│                             │                                       │
│                             ▼                                       │
│                      ┌─────────────┐                               │
│                      │   SQLCipher │                               │
│                      │   Database  │                               │
│                      └─────────────┘                               │
│                             │                                       │
│                             ▼                                       │
│                      ┌─────────────┐                               │
│                      │   File      │                               │
│                      │   Encryption│                               │
│                      └─────────────┘                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. Performance

### 7.1 Requisitos de Performance

| Operação | Meta | Estratégia |
|----------|------|------------|
| Inicialização | < 5s | Lazy loading |
| Upload PDF 100 páginas | < 30s | Processamento assíncrono |
| Extração de texto | < 60s | PyMuPDF otimizado |
| Cálculo de score | < 5s | Cache de embeddings |
| Geração de relatório | < 10s | Template pré-compilado |
| Busca em perfil | < 500ms | Índices SQLite |

### 7.2 Estratégias de Otimização

```python
# Exemplo: Processamento assíncrono com feedback de progresso
class AsyncProcessor:
    """Processador assíncrono com feedback de progresso."""

    async def process_edital(
        self,
        pdf_path: str,
        progress_callback: Callable[[int, str], None]
    ) -> ProcessedEdital:

        progress_callback(10, "Extraindo texto do PDF...")
        text = await self._extract_text_async(pdf_path)

        progress_callback(30, "Identificando seções...")
        sections = await self._identify_sections_async(text)

        progress_callback(50, "Extraindo requisitos...")
        requisitos = await self._extract_requisitos_async(sections)

        progress_callback(80, "Categorizando requisitos...")
        categorized = await self._categorize_async(requisitos)

        progress_callback(100, "Processamento concluído!")
        return ProcessedEdital(...)
```

---

## 8. Deployment

### 8.1 Estrutura de Distribuição

```
LicitaFit/
├── LicitaFit.exe              # Executável principal
├── config/
│   └── default.ini            # Configurações padrão
├── data/
│   ├── database.db            # Banco SQLite (criado no primeiro uso)
│   ├── embeddings/            # Cache de embeddings
│   └── documents/             # Documentos do usuário
├── resources/
│   ├── icons/
│   ├── templates/
│   └── models/                # Modelo de embeddings
├── logs/
│   └── app.log
└── README.txt                 # Instruções básicas
```

### 8.2 Requisitos de Sistema

| Requisito | Mínimo | Recomendado |
|-----------|--------|-------------|
| SO | Windows 10 64-bit | Windows 11 64-bit |
| CPU | Intel i3 / AMD Ryzen 3 | Intel i5 / AMD Ryzen 5 |
| RAM | 4 GB | 8 GB |
| Disco | 500 MB + dados | 1 GB + dados |
| Tela | 1366x768 | 1920x1080 |

### 8.3 Instalador

```
# Tecnologia: PyInstaller + Inno Setup
# ou NSIS

Wizard de Instalação:
1. Boas-vindas
2. Aceite de licença
3. Pasta de instalação
4. Opções (criar atalho, iniciar com Windows)
5. Instalação
6. Conclusão (abrir aplicativo)
```

---

## 9. Testes

### 9.1 Estratégia de Testes

| Tipo | Cobertura | Ferramenta |
|------|-----------|------------|
| Unitários | 80% | pytest |
| Integração | Críticos | pytest |
| UI | Fluxos principais | pytest-qt |
| Performance | Operações críticas | pytest-benchmark |

### 9.2 Estrutura de Testes

```
tests/
├── unit/
│   ├── test_entities.py
│   ├── test_services.py
│   └── test_repositories.py
├── integration/
│   ├── test_pdf_processing.py
│   ├── test_rag_integration.py
│   └── test_database.py
├── ui/
│   ├── test_main_window.py
│   └── test_dialogs.py
└── fixtures/
    ├── sample_editais/
    └── sample_empresas.json
```

---

## 10. Considerações Finais

### 10.1 Decisões Arquiteturais Chave

| Decisão | Justificativa | Trade-offs |
|---------|---------------|------------|
| Desktop (não web) | Segurança, offline, performance | Distribuição mais complexa |
| PyQt6 | Maturidade, documentação, aparência nativa | Curva de aprendizado |
| SQLite + SQLCipher | Simples, portátil, criptografado | Não escala para multiusuário |
| Embeddings locais | Offline, privacidade | Tamanho do instalador |
| Integração AMLDO | Reutilização, consistência | Dependência |

### 10.2 Evolução Futura

| Fase | Recurso | Impacto Arquitetural |
|------|---------|---------------------|
| v1.5 | Sincronização cloud opcional | Adicionar camada de sync |
| v2.0 | Versão web complementar | API REST, frontend separado |
| v2.5 | App mobile companion | API compartilhada |
| v3.0 | Marketplace de editais | Arquitetura de microserviços |

---

*Documento de arquitetura elaborado em Novembro/2024 como parte do planejamento do projeto LicitaFit.*
