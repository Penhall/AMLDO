# Stack Tecnológica
## LicitaFit - Sistema de Análise de Aderência a Editais

**Versão:** 1.0
**Data:** Novembro/2024

---

## 1. Visão Geral

### 1.1 Princípios de Seleção

| Critério | Peso | Justificativa |
|----------|------|---------------|
| **Maturidade** | Alto | Tecnologias estáveis e documentadas |
| **Python** | Alto | Compatibilidade com AMLDO |
| **Licença** | Alto | Uso comercial permitido |
| **Comunidade** | Médio | Suporte e recursos disponíveis |
| **Performance** | Médio | Adequado para desktop |
| **Facilidade** | Médio | Curva de aprendizado razoável |

### 1.2 Stack Resumida

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              STACK TECNOLÓGICA                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  LINGUAGEM                Python 3.11+                                             │
│  ──────────────────────────────────────────────────────────────────────────────    │
│                                                                                     │
│  INTERFACE                PyQt6                                                    │
│  ──────────────────────────────────────────────────────────────────────────────    │
│                                                                                     │
│  BANCO DE DADOS           SQLite + SQLAlchemy                                      │
│  ──────────────────────────────────────────────────────────────────────────────    │
│                                                                                     │
│  PDF PROCESSING           PyMuPDF (fitz)                                           │
│  ──────────────────────────────────────────────────────────────────────────────    │
│                                                                                     │
│  RAG ENGINE               AMLDO (integração)                                       │
│  ──────────────────────────────────────────────────────────────────────────────    │
│                                                                                     │
│  RELATÓRIOS               ReportLab / WeasyPrint                                   │
│  ──────────────────────────────────────────────────────────────────────────────    │
│                                                                                     │
│  EMPACOTAMENTO            PyInstaller                                              │
│  ──────────────────────────────────────────────────────────────────────────────    │
│                                                                                     │
│  INSTALADOR               Inno Setup (Windows)                                     │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Detalhamento por Camada

### 2.1 Interface de Usuário (UI)

#### PyQt6 (Recomendado)

| Aspecto | Detalhes |
|---------|----------|
| **Biblioteca** | PyQt6 |
| **Versão** | 6.6+ |
| **Licença** | GPL v3 / Comercial |
| **Por que?** | Maturidade, aparência nativa, documentação |

```python
# requirements.txt
PyQt6>=6.6.0
PyQt6-Qt6>=6.6.0
PyQt6-sip>=13.6.0
```

**Alternativas Consideradas:**

| Alternativa | Prós | Contras | Decisão |
|-------------|------|---------|---------|
| Tkinter | Nativo Python | UI datada, limitado | Descartado |
| PySide6 | LGPL (comercial) | Menor comunidade | Alternativa |
| Dear PyGui | Moderno | Imatura | Descartado |
| Kivy | Cross-platform | Não parece nativo | Descartado |

### 2.2 Banco de Dados

#### SQLite + SQLAlchemy

| Aspecto | Detalhes |
|---------|----------|
| **Banco** | SQLite 3 |
| **ORM** | SQLAlchemy 2.0+ |
| **Criptografia** | SQLCipher (opcional) |
| **Licença** | Public Domain / MIT |

```python
# requirements.txt
SQLAlchemy>=2.0.0
sqlcipher3>=0.5.0  # Para criptografia
alembic>=1.12.0     # Para migrações
```

**Justificativa:**
- Não requer servidor
- Portátil (arquivo único)
- Backup simples (cópia do arquivo)
- Performance adequada para volume esperado

### 2.3 Processamento de PDF

#### PyMuPDF (fitz)

| Aspecto | Detalhes |
|---------|----------|
| **Biblioteca** | PyMuPDF |
| **Versão** | 1.23+ |
| **Licença** | AGPL / Comercial |
| **Capacidades** | Extração de texto, metadados, imagens |

```python
# requirements.txt
PyMuPDF>=1.23.0
```

**Funcionalidades utilizadas:**
- Extração de texto com layout preservado
- Identificação de estrutura (títulos, parágrafos)
- Metadados do documento
- Contagem de páginas

### 2.4 Integração com AMLDO (RAG)

#### Reutilização do Motor RAG

```python
# Integração direta com módulos AMLDO
from amldo.rag.v2.tools import consultar_base_rag
from amldo.pipeline.embeddings import EmbeddingManager
```

**Dependências compartilhadas:**
```python
# requirements.txt (do AMLDO)
langchain>=0.1.0
langchain-google-genai>=1.0.0
faiss-cpu>=1.7.4
sentence-transformers>=2.2.0
```

### 2.5 Geração de Relatórios

#### ReportLab + Jinja2

| Aspecto | Detalhes |
|---------|----------|
| **PDF** | ReportLab |
| **Templates** | Jinja2 |
| **Excel** | openpyxl |
| **Licença** | BSD / MIT |

```python
# requirements.txt
reportlab>=4.0.0
Jinja2>=3.1.0
openpyxl>=3.1.0
```

**Alternativa para PDFs complexos:**
```python
# Para relatórios com CSS styling
weasyprint>=60.0  # Requer GTK
```

### 2.6 Utilitários

```python
# requirements.txt - Utilitários
pydantic>=2.5.0          # Validação de dados
python-dotenv>=1.0.0     # Variáveis de ambiente
loguru>=0.7.0            # Logging
bcrypt>=4.1.0            # Hash de senhas
cryptography>=41.0.0     # Criptografia geral
apscheduler>=3.10.0      # Agendamento de tarefas
```

---

## 3. Empacotamento e Distribuição

### 3.1 PyInstaller

```python
# requirements-dev.txt
pyinstaller>=6.0.0
```

**Configuração (licitafit.spec):**
```python
# licitafit.spec
a = Analysis(
    ['src/licitafit/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/licitafit/ui/resources', 'ui/resources'),
        ('data/models', 'models'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'sqlalchemy.dialects.sqlite',
    ],
    ...
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    name='LicitaFit',
    icon='resources/icon.ico',
    console=False,  # GUI application
    ...
)
```

### 3.2 Inno Setup (Instalador Windows)

```ini
; licitafit_setup.iss
[Setup]
AppName=LicitaFit
AppVersion=1.0.0
DefaultDirName={autopf}\LicitaFit
DefaultGroupName=LicitaFit
OutputBaseFilename=LicitaFit_Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\LicitaFit\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\LicitaFit"; Filename: "{app}\LicitaFit.exe"
Name: "{commondesktop}\LicitaFit"; Filename: "{app}\LicitaFit.exe"

[Run]
Filename: "{app}\LicitaFit.exe"; Description: "Executar LicitaFit"; Flags: nowait postinstall
```

---

## 4. Estrutura de Arquivos do Projeto

```
licitafit/
├── pyproject.toml              # Configuração do projeto
├── requirements/
│   ├── base.txt                # Dependências principais
│   ├── dev.txt                 # Desenvolvimento
│   └── test.txt                # Testes
│
├── src/
│   └── licitafit/
│       ├── __init__.py
│       ├── main.py             # Entry point
│       ├── app.py              # Aplicação principal
│       │
│       ├── ui/                 # Interface PyQt6
│       │   ├── __init__.py
│       │   ├── main_window.py
│       │   ├── widgets/
│       │   ├── dialogs/
│       │   └── resources/
│       │       ├── icons/
│       │       ├── styles/
│       │       └── images/
│       │
│       ├── services/           # Lógica de negócio
│       ├── domain/             # Entidades
│       ├── infrastructure/     # Acesso a dados
│       └── core/               # Configurações
│
├── tests/                      # Testes
├── data/                       # Dados locais
├── docs/                       # Documentação
├── scripts/                    # Scripts de build
│   ├── build.py
│   └── installer/
│
├── licitafit.spec              # PyInstaller spec
└── README.md
```

---

## 5. Requisitos de Sistema

### 5.1 Ambiente de Desenvolvimento

| Requisito | Mínimo | Recomendado |
|-----------|--------|-------------|
| Python | 3.11 | 3.12 |
| RAM | 8 GB | 16 GB |
| Disco | 5 GB | 10 GB |
| SO | Windows 10 | Windows 11 |
| IDE | VS Code | PyCharm |

### 5.2 Ambiente de Produção (Usuário Final)

| Requisito | Mínimo | Recomendado |
|-----------|--------|-------------|
| SO | Windows 10 64-bit | Windows 11 |
| RAM | 4 GB | 8 GB |
| Disco | 500 MB | 1 GB |
| CPU | Intel i3 / AMD Ryzen 3 | Intel i5 / AMD Ryzen 5 |
| Tela | 1366x768 | 1920x1080 |

---

## 6. Dependências Completas

### 6.1 requirements/base.txt

```
# Core
Python>=3.11

# UI
PyQt6>=6.6.0
PyQt6-Qt6>=6.6.0
PyQt6-sip>=13.6.0

# Database
SQLAlchemy>=2.0.0
alembic>=1.12.0

# PDF
PyMuPDF>=1.23.0

# Reports
reportlab>=4.0.0
Jinja2>=3.1.0
openpyxl>=3.1.0

# RAG Integration (from AMLDO)
langchain>=0.1.0
langchain-google-genai>=1.0.0
faiss-cpu>=1.7.4
sentence-transformers>=2.2.0

# Utils
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-dotenv>=1.0.0
loguru>=0.7.0
bcrypt>=4.1.0
cryptography>=41.0.0
apscheduler>=3.10.0
```

### 6.2 requirements/dev.txt

```
-r base.txt

# Testing
pytest>=7.4.0
pytest-qt>=4.2.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0

# Code Quality
black>=23.0.0
ruff>=0.1.0
mypy>=1.7.0
pre-commit>=3.6.0

# Build
pyinstaller>=6.0.0

# Docs
mkdocs>=1.5.0
mkdocs-material>=9.5.0
```

### 6.3 requirements/test.txt

```
-r base.txt

pytest>=7.4.0
pytest-qt>=4.2.0
pytest-cov>=4.1.0
pytest-mock>=3.12.0
factory-boy>=3.3.0
faker>=22.0.0
```

---

## 7. Configuração de Ambiente

### 7.1 Setup Inicial

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements/dev.txt

# Instalar em modo editável
pip install -e .

# Configurar pre-commit
pre-commit install
```

### 7.2 Variáveis de Ambiente (.env)

```env
# Configurações do LicitaFit
LICITAFIT_DEBUG=false
LICITAFIT_LOG_LEVEL=INFO
LICITAFIT_DB_PATH=data/licitafit.db

# Integração AMLDO (se necessário)
GOOGLE_API_KEY=your_key_here
AMLDO_VECTOR_DB_PATH=../amldo/data/vector_db
```

---

## 8. Considerações de Segurança

### 8.1 Bibliotecas de Segurança

| Biblioteca | Uso | Notas |
|------------|-----|-------|
| bcrypt | Hash de senhas | Salt automático |
| cryptography | Criptografia AES | Para arquivos sensíveis |
| SQLCipher | Criptografia do BD | Opcional, requer build |

### 8.2 Boas Práticas

- Nunca armazenar senhas em texto plano
- Usar SQLCipher para dados sensíveis
- Validar todas as entradas com Pydantic
- Sanitizar caminhos de arquivo
- Manter dependências atualizadas

---

*Stack Tecnológica elaborada em Novembro/2024.*
