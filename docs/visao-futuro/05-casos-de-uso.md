# Casos de Uso
## LicitaFit - Sistema de Análise de Aderência a Editais

**Versão:** 1.0
**Data:** Novembro/2024

---

## 1. Visão Geral

### 1.1 Atores do Sistema

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ATORES DO SISTEMA                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │                 │    │                 │    │                 │         │
│  │    Analista     │    │    Gestor       │    │   Consultor     │         │
│  │   de Licitação  │    │  de Licitação   │    │   Externo       │         │
│  │                 │    │                 │    │                 │         │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘         │
│           │                      │                      │                   │
│           │                      │                      │                   │
│           ▼                      ▼                      ▼                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         LICITAFIT DESKTOP                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│                         ┌─────────────────┐                                │
│                         │                 │                                │
│                         │   AMLDO RAG     │                                │
│                         │   (Sistema)     │                                │
│                         │                 │                                │
│                         └─────────────────┘                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Descrição dos Atores

| Ator | Descrição | Responsabilidades |
|------|-----------|-------------------|
| **Analista de Licitação** | Profissional que analisa editais e prepara documentação | Importar editais, analisar aderência, preparar documentos |
| **Gestor de Licitação** | Responsável por decidir participação e supervisionar | Revisar análises, aprovar participação, acompanhar resultados |
| **Consultor Externo** | Profissional autônomo que atende múltiplas empresas | Gerenciar múltiplos perfis, gerar relatórios profissionais |
| **AMLDO RAG** | Sistema de IA para extração e consulta legal | Extrair requisitos, categorizar, consultar legislação |

### 1.3 Diagrama de Casos de Uso

```
                                    LICITAFIT
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│    ┌─────────────────────────────────────────────────────────────────┐    │
│    │                    Gestão de Perfil                             │    │
│    │  ┌─────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │    │
│    │  │ UC01: Cad.  │ │ UC02: Cad.   │ │ UC03: Gerenciar          │ │    │
│    │  │ Empresa     │ │ Capacidades  │ │ Documentos               │ │    │
│    │  └─────────────┘ └──────────────┘ └──────────────────────────┘ │    │
│    └─────────────────────────────────────────────────────────────────┘    │
│                                                                            │
│    ┌─────────────────────────────────────────────────────────────────┐    │
│    │                    Análise de Editais                           │    │
│    │  ┌─────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │    │
│    │  │ UC04: Import│ │ UC05: Extrair│ │ UC06: Editar             │ │    │
│    │  │ Edital      │ │ Requisitos   │ │ Requisitos               │ │    │
│    │  └─────────────┘ └──────────────┘ └──────────────────────────┘ │    │
│    └─────────────────────────────────────────────────────────────────┘    │
│                                                                            │
│    ┌─────────────────────────────────────────────────────────────────┐    │
│    │                    Análise de Aderência                         │    │
│    │  ┌─────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │    │
│    │  │ UC07: Exec. │ │ UC08: Ident. │ │ UC09: Visualizar         │ │    │
│    │  │ Análise     │ │ Gaps         │ │ Score                    │ │    │
│    │  └─────────────┘ └──────────────┘ └──────────────────────────┘ │    │
│    └─────────────────────────────────────────────────────────────────┘    │
│                                                                            │
│    ┌─────────────────────────────────────────────────────────────────┐    │
│    │                    Relatórios e Exportação                      │    │
│    │  ┌─────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │    │
│    │  │ UC10: Gerar │ │ UC11: Gerar  │ │ UC12: Exportar           │ │    │
│    │  │ Relatório   │ │ Checklist    │ │ Dados                    │ │    │
│    │  └─────────────┘ └──────────────┘ └──────────────────────────┘ │    │
│    └─────────────────────────────────────────────────────────────────┘    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Casos de Uso - Gestão de Perfil

### UC01: Cadastrar Empresa

**Identificador:** UC01
**Nome:** Cadastrar Empresa
**Ator Principal:** Analista de Licitação
**Pré-condições:** Aplicação instalada e iniciada
**Pós-condições:** Empresa cadastrada no sistema

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Seleciona "Nova Empresa" | Exibe formulário de cadastro |
| 2 | Informa CNPJ | Valida formato do CNPJ |
| 3 | | Busca dados da Receita (se online) ou aguarda preenchimento manual |
| 4 | Preenche dados obrigatórios (Razão Social, Porte, Ramo) | Valida campos obrigatórios |
| 5 | Preenche dados opcionais | Aceita dados complementares |
| 6 | Clica em "Salvar" | Persiste empresa no banco de dados |
| 7 | | Exibe confirmação e redireciona para perfil |

#### Fluxo Alternativo A: CNPJ já cadastrado

| Passo | Ator | Sistema |
|-------|------|---------|
| 2a | | Detecta CNPJ já existente |
| 2b | | Exibe mensagem "Empresa já cadastrada" |
| 2c | | Oferece opção de editar empresa existente |

#### Fluxo Alternativo B: Dados incompletos

| Passo | Ator | Sistema |
|-------|------|---------|
| 6a | | Identifica campos obrigatórios vazios |
| 6b | | Destaca campos faltantes |
| 6c | Preenche campos faltantes | Revalida formulário |

#### Regras de Negócio

- RN01: CNPJ deve ser único no sistema
- RN02: CNPJ deve ser válido (dígito verificador)
- RN03: Razão Social é obrigatória
- RN04: Porte deve ser selecionado de lista pré-definida

---

### UC02: Cadastrar Capacidades

**Identificador:** UC02
**Nome:** Cadastrar Capacidades da Empresa
**Ator Principal:** Analista de Licitação
**Pré-condições:** Empresa cadastrada (UC01)
**Pós-condições:** Capacidades vinculadas à empresa

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa perfil da empresa | Exibe tela de perfil |
| 2 | Seleciona aba "Capacidades" | Lista capacidades existentes |
| 3 | Clica em "Adicionar Capacidade" | Abre formulário de capacidade |
| 4 | Seleciona categoria universal | Carrega descrição da categoria |
| 5 | Preenche nível de experiência | Valida nível (Básico a Especialista) |
| 6 | Preenche anos de experiência | Valida número positivo |
| 7 | Adiciona descrição detalhada | Aceita texto livre |
| 8 | (Opcional) Anexa comprovante | Valida arquivo (PDF, até 10MB) |
| 9 | Clica em "Salvar" | Persiste capacidade |
| 10 | | Atualiza lista de capacidades |

#### Fluxo Alternativo: Busca de Categoria

| Passo | Ator | Sistema |
|-------|------|---------|
| 4a | Digita texto para busca | Filtra categorias por termo |
| 4b | Seleciona categoria da lista filtrada | Preenche campo de categoria |

#### Regras de Negócio

- RN05: Cada capacidade deve ter uma categoria universal
- RN06: Nível de experiência deve ser: Básico, Intermediário, Avançado ou Especialista
- RN07: Anos de experiência deve ser >= 0
- RN08: Uma empresa pode ter múltiplas capacidades na mesma categoria

---

### UC03: Gerenciar Documentos

**Identificador:** UC03
**Nome:** Gerenciar Documentos da Empresa
**Ator Principal:** Analista de Licitação
**Pré-condições:** Empresa cadastrada (UC01)
**Pós-condições:** Documentos armazenados e organizados

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa aba "Documentos" | Lista documentos existentes |
| 2 | Clica em "Adicionar Documento" | Abre formulário de upload |
| 3 | Seleciona tipo de documento | Carrega campos específicos do tipo |
| 4 | Faz upload do arquivo | Valida formato e tamanho |
| 5 | | Calcula hash do arquivo (integridade) |
| 6 | Informa data de emissão | Valida data não futura |
| 7 | Informa data de validade (se aplicável) | Valida data >= emissão |
| 8 | Clica em "Salvar" | Persiste documento e metadados |
| 9 | | Cria alerta de vencimento se configurado |

#### Fluxo Alternativo A: Documento vencido

| Passo | Ator | Sistema |
|-------|------|---------|
| 7a | Informa data de validade no passado | Exibe aviso de documento vencido |
| 7b | | Marca documento como "Vencido" |
| 7c | Confirma cadastro mesmo assim | Salva com status "Vencido" |

#### Fluxo Alternativo B: Atualizar documento existente

| Passo | Ator | Sistema |
|-------|------|---------|
| 1a | Seleciona documento existente | Exibe detalhes do documento |
| 1b | Clica em "Atualizar" | Abre formulário com dados preenchidos |
| 1c | Faz upload de nova versão | Mantém histórico da versão anterior |

#### Regras de Negócio

- RN09: Tipos de documento válidos: Certidão, Atestado, Contrato, Licença, Balanço, Alvará, Outro
- RN10: Formatos aceitos: PDF, JPG, PNG
- RN11: Tamanho máximo: 20MB por arquivo
- RN12: Alertas de vencimento são criados com 30 dias de antecedência (configurável)

---

## 3. Casos de Uso - Análise de Editais

### UC04: Importar Edital

**Identificador:** UC04
**Nome:** Importar Edital
**Ator Principal:** Analista de Licitação
**Pré-condições:** Empresa selecionada
**Pós-condições:** Edital importado e texto extraído

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Seleciona "Novo Edital" | Abre formulário de importação |
| 2 | Clica em "Selecionar Arquivo" | Abre diálogo de seleção de arquivo |
| 3 | Seleciona arquivo PDF do edital | Valida formato PDF |
| 4 | | Exibe nome e tamanho do arquivo |
| 5 | Preenche número do edital | Valida campo obrigatório |
| 6 | Preenche órgão licitante | Valida campo obrigatório |
| 7 | Seleciona modalidade | Valida seleção obrigatória |
| 8 | (Opcional) Preenche dados adicionais | Aceita dados complementares |
| 9 | Clica em "Importar" | Inicia processamento |
| 10 | | Extrai texto do PDF |
| 11 | | Exibe barra de progresso |
| 12 | | Exibe confirmação de importação |

#### Fluxo Alternativo A: PDF protegido

| Passo | Ator | Sistema |
|-------|------|---------|
| 10a | | Detecta PDF protegido por senha |
| 10b | | Solicita senha do PDF |
| 10c | Informa senha | Tenta desbloquear PDF |
| 10d | | Se senha correta, continua extração |

#### Fluxo Alternativo B: PDF escaneado (imagem)

| Passo | Ator | Sistema |
|-------|------|---------|
| 10a | | Detecta PDF baseado em imagem |
| 10b | | Exibe aviso sobre limitações de OCR |
| 10c | | Oferece opção de prosseguir com OCR (se disponível) |

#### Regras de Negócio

- RN13: Formato obrigatório: PDF
- RN14: Tamanho máximo: 50MB
- RN15: Número do edital deve ser único por empresa
- RN16: Texto extraído é armazenado para consultas posteriores

---

### UC05: Extrair Requisitos do Edital

**Identificador:** UC05
**Nome:** Extrair Requisitos Automaticamente
**Ator Principal:** Sistema (AMLDO RAG)
**Ator Secundário:** Analista de Licitação
**Pré-condições:** Edital importado (UC04)
**Pós-condições:** Requisitos extraídos e categorizados

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Seleciona edital importado | Carrega dados do edital |
| 2 | Clica em "Extrair Requisitos" | Inicia processamento RAG |
| 3 | | Identifica seções do edital |
| 4 | | Envia texto para AMLDO RAG |
| 5 | | Recebe requisitos identificados |
| 6 | | Categoriza requisitos (Técnico, Financeiro, Jurídico) |
| 7 | | Classifica como Obrigatório/Desejável |
| 8 | | Exibe lista de requisitos extraídos |
| 9 | | Indica score de confiança de cada extração |

#### Fluxo Alternativo: Requisito não categorizado

| Passo | Ator | Sistema |
|-------|------|---------|
| 6a | | Não encontra categoria adequada |
| 6b | | Marca requisito como "Não categorizado" |
| 6c | | Solicita categorização manual |

#### Regras de Negócio

- RN17: Seções padrão buscadas: Objeto, Habilitação, Qualificação Técnica, Qualificação Financeira
- RN18: Score de confiança < 70% deve ser destacado para revisão
- RN19: Requisitos são inicialmente marcados como "não validados"

---

### UC06: Editar Requisitos Extraídos

**Identificador:** UC06
**Nome:** Editar Requisitos Extraídos
**Ator Principal:** Analista de Licitação
**Pré-condições:** Requisitos extraídos (UC05)
**Pós-condições:** Requisitos validados e ajustados

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Visualiza lista de requisitos | Exibe requisitos com status de validação |
| 2 | Seleciona requisito para editar | Abre painel de edição |
| 3 | Revisa texto do requisito | Exibe texto original do edital |
| 4 | Ajusta descrição se necessário | Aceita edição de texto |
| 5 | Confirma/altera tipo (Obrig./Desej.) | Atualiza classificação |
| 6 | Confirma/altera categoria | Atualiza categoria universal |
| 7 | Marca como "Validado" | Atualiza status de validação |
| 8 | Clica em "Salvar" | Persiste alterações |

#### Fluxo Alternativo A: Adicionar requisito manualmente

| Passo | Ator | Sistema |
|-------|------|---------|
| 1a | Clica em "Adicionar Requisito" | Abre formulário em branco |
| 1b | Preenche todos os campos | Valida campos obrigatórios |
| 1c | Marca origem como "Manual" | Salva requisito manual |

#### Fluxo Alternativo B: Excluir requisito incorreto

| Passo | Ator | Sistema |
|-------|------|---------|
| 2a | Clica em "Excluir" no requisito | Solicita confirmação |
| 2b | Confirma exclusão | Remove requisito do edital |

#### Regras de Negócio

- RN20: Requisitos manuais devem ter todas as informações preenchidas
- RN21: Exclusão de requisito é reversível até a análise ser finalizada
- RN22: Alterações são registradas no log de auditoria

---

## 4. Casos de Uso - Análise de Aderência

### UC07: Executar Análise de Aderência

**Identificador:** UC07
**Nome:** Executar Análise de Aderência
**Ator Principal:** Analista de Licitação
**Pré-condições:**
- Perfil da empresa completo (capacidades cadastradas)
- Edital com requisitos extraídos/validados
**Pós-condições:** Análise executada com score calculado

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Seleciona edital para análise | Carrega edital e requisitos |
| 2 | Confirma empresa para análise | Carrega perfil da empresa |
| 3 | Clica em "Executar Análise" | Inicia processo de análise |
| 4 | | Para cada requisito: |
| 5 | | → Busca capacidades compatíveis |
| 6 | | → Busca certificações compatíveis |
| 7 | | → Busca documentos relacionados |
| 8 | | → Calcula score de match |
| 9 | | → Determina se atende (sim/não/parcial) |
| 10 | | Calcula score global |
| 11 | | Calcula scores por área |
| 12 | | Determina recomendação |
| 13 | | Exibe resultado da análise |

#### Fluxo Alternativo: Conflito de categorias

| Passo | Ator | Sistema |
|-------|------|---------|
| 6a | | Encontra múltiplas capacidades para mesmo requisito |
| 6b | | Seleciona melhor match automaticamente |
| 6c | | Registra alternativas para revisão |

#### Regras de Negócio

- RN23: Score global = (requisitos atendidos / total requisitos) * 100
- RN24: Score de requisitos obrigatórios é calculado separadamente
- RN25: Recomendações: >= 70% = Participar, 50-69% = Avaliar, < 50% = Não Participar
- RN26: Se qualquer requisito obrigatório crítico não atendido = Não Participar

---

### UC08: Identificar Gaps

**Identificador:** UC08
**Nome:** Identificar e Classificar Gaps
**Ator Principal:** Sistema
**Ator Secundário:** Analista de Licitação
**Pré-condições:** Análise executada (UC07)
**Pós-condições:** Gaps identificados com severidade e recomendações

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | | Para cada requisito não atendido: |
| 2 | | → Cria registro de gap |
| 3 | | → Determina severidade (Crítico a Baixo) |
| 4 | | → Gera descrição do gap |
| 5 | | → Sugere ação para resolução |
| 6 | | → Estima dificuldade de resolução |
| 7 | Visualiza lista de gaps | Exibe gaps ordenados por severidade |
| 8 | Seleciona gap para detalhes | Mostra detalhes e recomendações |

#### Fluxo Alternativo: Ajuste manual de severidade

| Passo | Ator | Sistema |
|-------|------|---------|
| 8a | Altera severidade do gap | Valida justificativa obrigatória |
| 8b | Informa justificativa | Salva ajuste com justificativa |

#### Regras de Negócio

- RN27: Severidades: Crítico (elimina), Alto (dificulta muito), Médio (dificulta), Baixo (impacto menor)
- RN28: Requisitos obrigatórios não atendidos = severidade mínima "Alto"
- RN29: Gaps críticos disparam alerta visual destacado

---

### UC09: Visualizar Score de Aderência

**Identificador:** UC09
**Nome:** Visualizar Score e Detalhamento
**Ator Principal:** Analista de Licitação / Gestor
**Pré-condições:** Análise executada (UC07)
**Pós-condições:** Nenhuma (visualização apenas)

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa análise | Exibe painel de resultados |
| 2 | | Mostra score global em destaque |
| 3 | | Mostra scores por área (Técnico, Financeiro, Jurídico) |
| 4 | | Mostra gráfico de requisitos (atendidos x não atendidos) |
| 5 | | Mostra recomendação com justificativa |
| 6 | | Lista requisitos com status de cada um |
| 7 | Filtra por área ou status | Atualiza visualização filtrada |
| 8 | Seleciona requisito específico | Mostra detalhes do match |

#### Regras de Negócio

- RN30: Cores do score: Verde (>= 70%), Amarelo (50-69%), Vermelho (< 50%)
- RN31: Recomendação é destacada com cor e ícone
- RN32: Detalhes incluem texto original do edital e capacidade vinculada

---

## 5. Casos de Uso - Relatórios

### UC10: Gerar Relatório de Aderência

**Identificador:** UC10
**Nome:** Gerar Relatório de Aderência
**Ator Principal:** Analista de Licitação / Gestor
**Pré-condições:** Análise finalizada (UC07)
**Pós-condições:** Relatório PDF gerado

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa análise finalizada | Exibe opções de relatório |
| 2 | Clica em "Gerar Relatório" | Abre configurações de relatório |
| 3 | Seleciona template (Executivo/Detalhado) | Carrega template selecionado |
| 4 | (Opcional) Adiciona logo da empresa | Insere logo no cabeçalho |
| 5 | (Opcional) Adiciona observações | Inclui texto adicional |
| 6 | Clica em "Gerar PDF" | Processa geração do PDF |
| 7 | | Exibe preview do relatório |
| 8 | Clica em "Salvar" | Abre diálogo para salvar arquivo |
| 9 | Seleciona local e nome | Salva PDF no disco |

#### Fluxo Alternativo: Gerar Excel

| Passo | Ator | Sistema |
|-------|------|---------|
| 2a | Clica em "Exportar Excel" | Gera planilha com dados |
| 2b | | Inclui abas: Resumo, Requisitos, Gaps, Matches |

#### Regras de Negócio

- RN33: Template Executivo: 2-3 páginas, foco em decisão
- RN34: Template Detalhado: Completo com todos os requisitos
- RN35: Relatório inclui data/hora de geração e versão do sistema

---

### UC11: Gerar Checklist de Documentos

**Identificador:** UC11
**Nome:** Gerar Checklist de Documentos
**Ator Principal:** Analista de Licitação
**Pré-condições:** Edital com requisitos extraídos
**Pós-condições:** Checklist de documentos necessários

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Seleciona edital | Carrega requisitos documentais |
| 2 | Clica em "Gerar Checklist" | Processa requisitos |
| 3 | | Identifica documentos exigidos |
| 4 | | Cruza com documentos cadastrados da empresa |
| 5 | | Marca quais já possui |
| 6 | | Destaca documentos faltantes ou vencidos |
| 7 | | Exibe checklist interativo |
| 8 | Marca documento como "verificado" | Atualiza status no checklist |
| 9 | Exporta checklist | Gera PDF ou Excel do checklist |

#### Regras de Negócio

- RN36: Documentos vencidos são destacados em vermelho
- RN37: Documentos próximos do vencimento (< 30 dias) em amarelo
- RN38: Checklist pode ser impresso para conferência manual

---

### UC12: Exportar Dados

**Identificador:** UC12
**Nome:** Exportar Dados do Sistema
**Ator Principal:** Analista / Gestor
**Pré-condições:** Dados existentes no sistema
**Pós-condições:** Arquivo exportado

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu "Ferramentas > Exportar" | Exibe opções de exportação |
| 2 | Seleciona tipo de exportação | Configura parâmetros |
| 3 | Seleciona formato (JSON/CSV/Excel) | Prepara exportação |
| 4 | Seleciona entidades (Empresa/Editais/Análises) | Filtra dados a exportar |
| 5 | Clica em "Exportar" | Processa exportação |
| 6 | | Gera arquivo com dados |
| 7 | Seleciona local para salvar | Salva arquivo |

#### Tipos de Exportação

| Tipo | Descrição | Formato |
|------|-----------|---------|
| Backup Completo | Todos os dados do sistema | JSON |
| Perfil da Empresa | Dados da empresa, capacidades, documentos | JSON/CSV |
| Histórico de Análises | Todas as análises realizadas | Excel |
| Dados de Edital | Edital específico com requisitos | JSON |

---

## 6. Casos de Uso - Administração

### UC13: Configurar Sistema

**Identificador:** UC13
**Nome:** Configurar Parâmetros do Sistema
**Ator Principal:** Gestor / Administrador
**Pré-condições:** Sistema instalado
**Pós-condições:** Configurações salvas

#### Configurações Disponíveis

| Categoria | Parâmetro | Descrição |
|-----------|-----------|-----------|
| Interface | Tema | Claro / Escuro |
| Interface | Idioma | Português (BR) |
| Análise | Score mínimo para "Participar" | Padrão: 70% |
| Análise | Score mínimo para "Avaliar" | Padrão: 50% |
| Alertas | Dias antes do vencimento | Padrão: 30 dias |
| Backup | Backup automático | Sim/Não |
| Backup | Intervalo de backup | Padrão: 7 dias |
| Segurança | Tempo de sessão | Padrão: 60 min |

---

### UC14: Gerenciar Alertas

**Identificador:** UC14
**Nome:** Gerenciar Alertas do Sistema
**Ator Principal:** Analista / Gestor
**Pré-condições:** Sistema em uso
**Pós-condições:** Alertas visualizados/gerenciados

#### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Visualiza ícone de alertas | Exibe contador de alertas |
| 2 | Clica no ícone | Abre painel de alertas |
| 3 | | Lista alertas por prioridade |
| 4 | Seleciona alerta | Exibe detalhes |
| 5 | Marca como lido | Atualiza status |
| 6 | (Opcional) Descarta alerta | Remove da lista |

#### Tipos de Alerta

| Tipo | Prioridade | Descrição |
|------|------------|-----------|
| Documento vencido | Crítica | Documento já venceu |
| Documento vencendo | Alta | Documento vence em < 30 dias |
| Edital próximo | Alta | Data de abertura em < 7 dias |
| Gap pendente | Média | Gap não resolvido |
| Backup necessário | Baixa | Último backup > 7 dias |

---

## 7. Matriz de Rastreabilidade

### Casos de Uso x Requisitos Funcionais

| UC | RF01 | RF02 | RF03 | RF04 | RF05 | RF06 | RF07 | RF08 | RF09 | RF10 |
|----|------|------|------|------|------|------|------|------|------|------|
| UC01 | X |   |   |   |   |   |   |   |   |   |
| UC02 |   | X |   |   |   |   |   |   |   |   |
| UC03 |   |   | X |   |   |   |   |   |   |   |
| UC04 |   |   |   | X |   |   |   |   |   |   |
| UC05 |   |   |   |   | X |   |   |   |   |   |
| UC06 |   |   |   |   | X |   |   |   |   |   |
| UC07 |   |   |   |   |   | X |   |   |   |   |
| UC08 |   |   |   |   |   |   | X |   |   |   |
| UC09 |   |   |   |   |   |   |   | X |   |   |
| UC10 |   |   |   |   |   |   |   |   | X |   |
| UC11 |   |   |   |   |   |   |   |   | X |   |
| UC12 |   |   |   |   |   |   |   |   |   | X |

### Legenda RF

| ID | Requisito Funcional |
|----|---------------------|
| RF01 | Cadastrar e gerenciar empresas |
| RF02 | Cadastrar capacidades e certificações |
| RF03 | Gerenciar documentos com validade |
| RF04 | Importar e processar editais PDF |
| RF05 | Extrair e editar requisitos |
| RF06 | Calcular score de aderência |
| RF07 | Identificar e classificar gaps |
| RF08 | Visualizar resultados de análise |
| RF09 | Gerar relatórios e checklists |
| RF10 | Exportar dados do sistema |

---

*Documento de Casos de Uso elaborado em Novembro/2024 como parte do planejamento do projeto LicitaFit.*
