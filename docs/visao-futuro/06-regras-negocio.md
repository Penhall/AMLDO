# Regras de Negócio
## LicitaFit - Sistema de Análise de Aderência a Editais

**Versão:** 1.0
**Data:** Novembro/2024

---

## 1. Visão Geral

Este documento detalha todas as regras de negócio do sistema LicitaFit, organizadas por domínio funcional.

### Nomenclatura

- **RN**: Regra de Negócio
- **VAL**: Validação
- **CALC**: Cálculo
- **PROC**: Processo

---

## 2. Regras de Empresa

### 2.1 Cadastro de Empresa

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-EMP-001 | CNPJ Único | O CNPJ deve ser único no sistema. Não é permitido cadastrar duas empresas com o mesmo CNPJ. | VAL |
| RN-EMP-002 | CNPJ Válido | O CNPJ deve passar na validação de dígito verificador (algoritmo da Receita Federal). | VAL |
| RN-EMP-003 | Campos Obrigatórios | São obrigatórios: CNPJ, Razão Social, Porte, Ramo de Atividade. | VAL |
| RN-EMP-004 | Porte Válido | O porte deve ser um dos valores: MEI, ME, EPP, MEDIO, GRANDE. | VAL |
| RN-EMP-005 | CNAE Formato | Se informado, CNAE deve ter 7 dígitos (XXXX-X/XX). | VAL |
| RN-EMP-006 | Email Formato | Se informado, email deve ser válido (formato RFC 5322). | VAL |
| RN-EMP-007 | UF Válida | Se informada, UF deve ser uma das 27 siglas brasileiras. | VAL |
| RN-EMP-008 | CEP Formato | Se informado, CEP deve ter 8 dígitos (XXXXX-XXX). | VAL |

### 2.2 Classificação de Porte

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-EMP-010 | Classificação MEI | MEI: Faturamento anual até R$ 81.000,00. | PROC |
| RN-EMP-011 | Classificação ME | ME: Faturamento anual até R$ 360.000,00. | PROC |
| RN-EMP-012 | Classificação EPP | EPP: Faturamento anual de R$ 360.000,01 até R$ 4.800.000,00. | PROC |
| RN-EMP-013 | Classificação Médio | MEDIO: Faturamento anual de R$ 4.800.000,01 até R$ 300.000.000,00. | PROC |
| RN-EMP-014 | Classificação Grande | GRANDE: Faturamento anual acima de R$ 300.000.000,00. | PROC |

---

## 3. Regras de Capacidade

### 3.1 Cadastro de Capacidade

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-CAP-001 | Categoria Obrigatória | Toda capacidade deve estar vinculada a uma categoria universal. | VAL |
| RN-CAP-002 | Nível Válido | O nível deve ser: BASICO, INTERMEDIARIO, AVANCADO ou ESPECIALISTA. | VAL |
| RN-CAP-003 | Experiência Positiva | Anos de experiência deve ser >= 0. | VAL |
| RN-CAP-004 | Projetos Positivos | Quantidade de projetos deve ser >= 0. | VAL |
| RN-CAP-005 | Comprovante Formato | Comprovante deve ser PDF ou imagem (JPG, PNG) até 10MB. | VAL |

### 3.2 Níveis de Experiência

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-CAP-010 | Nível Básico | BASICO: 0-2 anos de experiência, até 5 projetos. | PROC |
| RN-CAP-011 | Nível Intermediário | INTERMEDIARIO: 2-5 anos de experiência, 5-15 projetos. | PROC |
| RN-CAP-012 | Nível Avançado | AVANCADO: 5-10 anos de experiência, 15-50 projetos. | PROC |
| RN-CAP-013 | Nível Especialista | ESPECIALISTA: >10 anos de experiência, >50 projetos ou certificação específica. | PROC |

---

## 4. Regras de Certificação

### 4.1 Cadastro de Certificação

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-CERT-001 | Tipo Válido | Tipo deve ser: CERTIFICADO, ATESTADO, REGISTRO, LICENCA ou OUTRO. | VAL |
| RN-CERT-002 | Emissor Obrigatório | Órgão/entidade emissor é obrigatório. | VAL |
| RN-CERT-003 | Data Emissão Válida | Data de emissão não pode ser futura. | VAL |
| RN-CERT-004 | Data Validade Consistente | Data de validade deve ser >= data de emissão (quando aplicável). | VAL |
| RN-CERT-005 | Arquivo Formato | Arquivo deve ser PDF ou imagem até 20MB. | VAL |

### 4.2 Status de Certificação

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-CERT-010 | Status Válido | Status automático: data_validade < hoje → VENCIDO. | CALC |
| RN-CERT-011 | Status Vencendo | Alerta quando data_validade < hoje + 30 dias. | CALC |
| RN-CERT-012 | Renovação | Ao fazer upload de nova versão, status anterior vira "RENOVADO". | PROC |

---

## 5. Regras de Documento

### 5.1 Cadastro de Documento

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-DOC-001 | Tipo Válido | Tipo deve ser um dos predefinidos (CND, Contrato, Balanço, etc.). | VAL |
| RN-DOC-002 | Arquivo Obrigatório | Arquivo é obrigatório. | VAL |
| RN-DOC-003 | Formato Arquivo | Formato aceito: PDF, JPG, PNG. Tamanho máximo: 20MB. | VAL |
| RN-DOC-004 | Hash Integridade | Sistema calcula SHA-256 do arquivo para verificação de integridade. | PROC |
| RN-DOC-005 | Data Emissão Válida | Data de emissão não pode ser futura. | VAL |

### 5.2 Controle de Validade

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-DOC-010 | Validade Automática | Documentos com data_validade são monitorados automaticamente. | PROC |
| RN-DOC-011 | Alerta Vencimento | Alerta criado X dias antes do vencimento (X = configurável, padrão 30). | PROC |
| RN-DOC-012 | Status Vencido | Documento com data_validade < hoje → status = VENCIDO. | CALC |
| RN-DOC-013 | Validade por Tipo | Validades padrão por tipo de documento: |

#### Validades Padrão por Tipo

| Tipo de Documento | Validade Típica |
|-------------------|-----------------|
| CND Federal | 180 dias |
| CND Estadual | 30-180 dias (varia por estado) |
| CND Municipal | 30-90 dias (varia por município) |
| CNDT | 180 dias |
| CRF (FGTS) | 30 dias |
| Balanço Patrimonial | 1 ano (referente ao exercício anterior) |
| Alvará | 1 ano |

---

## 6. Regras de Edital

### 6.1 Importação de Edital

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-EDT-001 | Formato PDF | Arquivo deve ser PDF. | VAL |
| RN-EDT-002 | Tamanho Máximo | Tamanho máximo: 50MB. | VAL |
| RN-EDT-003 | Número Único | Número do edital deve ser único por empresa. | VAL |
| RN-EDT-004 | Modalidade Válida | Modalidade deve ser uma das predefinidas. | VAL |
| RN-EDT-005 | Data Abertura Futura | Data de abertura não pode ser no passado (aviso se for). | VAL |

### 6.2 Modalidades de Licitação

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-EDT-010 | Pregão Eletrônico | Modalidade mais comum, valores variados, menor preço. | PROC |
| RN-EDT-011 | Concorrência | Valores > R$ 3.300.000,00 (obras) ou > R$ 1.430.000,00 (compras/serviços). | PROC |
| RN-EDT-012 | Tomada de Preços | Valores intermediários, cadastro prévio exigido. | PROC |
| RN-EDT-013 | Convite | Valores menores, mínimo 3 convidados. | PROC |
| RN-EDT-014 | Diálogo Competitivo | Nova Lei 14.133, soluções inovadoras. | PROC |

### 6.3 Processamento de PDF

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-EDT-020 | Extração de Texto | Sistema extrai texto automaticamente do PDF. | PROC |
| RN-EDT-021 | PDF Protegido | PDF protegido requer senha para processamento. | PROC |
| RN-EDT-022 | PDF Imagem | PDF baseado em imagem requer OCR (qualidade pode variar). | PROC |
| RN-EDT-023 | Armazenamento Texto | Texto extraído é armazenado para buscas posteriores. | PROC |

---

## 7. Regras de Requisito

### 7.1 Extração de Requisitos

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-REQ-001 | Fonte RAG | Requisitos são extraídos via AMLDO RAG. | PROC |
| RN-REQ-002 | Score Confiança | Cada requisito extraído tem score de confiança (0-1). | CALC |
| RN-REQ-003 | Revisão Necessária | Score < 0.7 marca requisito para revisão manual. | PROC |
| RN-REQ-004 | Categoria Sugerida | Sistema sugere categoria universal baseado em keywords. | PROC |

### 7.2 Classificação de Requisitos

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-REQ-010 | Tipo Obrigatório | Requisito pode ser OBRIGATORIO ou DESEJAVEL. | VAL |
| RN-REQ-011 | Área Obrigatória | Área deve ser: TECNICA, FINANCEIRA, JURIDICA ou ADMINISTRATIVA. | VAL |
| RN-REQ-012 | Texto Original | Texto original do edital deve ser preservado. | PROC |
| RN-REQ-013 | Edição Manual | Requisitos podem ser editados manualmente pelo usuário. | PROC |

### 7.3 Requisitos por Área

| Área | Exemplos de Requisitos |
|------|------------------------|
| TECNICA | Atestado de capacidade técnica, experiência anterior, equipe técnica |
| FINANCEIRA | Capital social mínimo, patrimônio líquido, índices contábeis |
| JURIDICA | CND, regularidade fiscal, capacidade jurídica, não impedimento |
| ADMINISTRATIVA | Declarações, formulários preenchidos, garantias |

---

## 8. Regras de Análise de Aderência

### 8.1 Execução da Análise

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-ANA-001 | Pré-requisito Empresa | Empresa deve ter perfil com capacidades cadastradas. | VAL |
| RN-ANA-002 | Pré-requisito Edital | Edital deve ter requisitos extraídos/validados. | VAL |
| RN-ANA-003 | Análise Única | Apenas uma análise ativa por par empresa/edital. | VAL |
| RN-ANA-004 | Match Automático | Sistema busca match automático por categoria universal. | PROC |

### 8.2 Cálculo de Score

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-ANA-010 | Score Global | `score_global = (requisitos_atendidos / total_requisitos) * 100` | CALC |
| RN-ANA-011 | Score Obrigatórios | `score_obrig = (obrig_atendidos / total_obrig) * 100` | CALC |
| RN-ANA-012 | Score Desejáveis | `score_desej = (desej_atendidos / total_desej) * 100` | CALC |
| RN-ANA-013 | Score por Área | Calculado separadamente para cada área (Técnica, Financeira, etc.) | CALC |

#### Fórmulas de Cálculo

```
Score Global = (Requisitos Atendidos / Total Requisitos) × 100

Score Ponderado = (Score Obrig × 0.7) + (Score Desej × 0.3)

Score Técnico = (Requisitos Técnicos Atendidos / Total Técnicos) × 100
```

### 8.3 Determinação de Match

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-ANA-020 | Match por Categoria | Requisito e Capacidade com mesma categoria universal = match. | PROC |
| RN-ANA-021 | Match por Nível | Capacidade deve ter nível >= nível exigido pelo requisito. | PROC |
| RN-ANA-022 | Match por Documento | Requisito documental é atendido se documento existe e está válido. | PROC |
| RN-ANA-023 | Match Parcial | Match com nível inferior ao exigido = parcialmente atendido. | PROC |

### 8.4 Recomendação Automática

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-ANA-030 | Participar | Score global >= 70% E score obrigatórios >= 90% → PARTICIPAR | CALC |
| RN-ANA-031 | Avaliar | Score global >= 50% E score obrigatórios >= 70% → AVALIAR | CALC |
| RN-ANA-032 | Não Participar | Score global < 50% OU score obrigatórios < 70% → NAO_PARTICIPAR | CALC |
| RN-ANA-033 | Veto Automático | Qualquer requisito obrigatório crítico não atendido → NAO_PARTICIPAR | CALC |

#### Tabela de Decisão

```
┌────────────────────┬──────────────────┬─────────────────┬──────────────────┐
│   Score Global     │  Score Obrig.    │  Gaps Críticos  │   Recomendação   │
├────────────────────┼──────────────────┼─────────────────┼──────────────────┤
│      >= 70%        │     >= 90%       │       0         │    PARTICIPAR    │
│      >= 70%        │     >= 90%       │      > 0        │    AVALIAR       │
│      >= 50%        │     >= 70%       │       0         │    AVALIAR       │
│      >= 50%        │     >= 70%       │      > 0        │  NAO_PARTICIPAR  │
│      < 50%         │     qualquer     │    qualquer     │  NAO_PARTICIPAR  │
│     qualquer       │     < 70%        │    qualquer     │  NAO_PARTICIPAR  │
└────────────────────┴──────────────────┴─────────────────┴──────────────────┘
```

---

## 9. Regras de Gap

### 9.1 Identificação de Gap

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-GAP-001 | Criação Automática | Gap é criado para cada requisito não atendido ou parcialmente atendido. | PROC |
| RN-GAP-002 | Tipo de Gap | TOTAL = não atendido, PARCIAL = parcialmente atendido. | PROC |
| RN-GAP-003 | Descrição Automática | Sistema gera descrição baseada no requisito e motivo. | PROC |

### 9.2 Classificação de Severidade

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-GAP-010 | Severidade Crítica | CRITICO: Requisito obrigatório eliminatório não atendido. | CALC |
| RN-GAP-011 | Severidade Alta | ALTO: Requisito obrigatório não eliminatório não atendido. | CALC |
| RN-GAP-012 | Severidade Média | MEDIO: Requisito desejável importante não atendido. | CALC |
| RN-GAP-013 | Severidade Baixa | BAIXO: Requisito desejável menor não atendido. | CALC |

#### Matriz de Severidade

```
┌─────────────────────┬───────────────┬───────────────┬────────────────┐
│   Tipo Requisito    │  Eliminatório │  Pontuação    │   Severidade   │
├─────────────────────┼───────────────┼───────────────┼────────────────┤
│     OBRIGATORIO     │      SIM      │      N/A      │    CRITICO     │
│     OBRIGATORIO     │      NÃO      │      N/A      │    ALTO        │
│     DESEJAVEL       │      N/A      │     > 10%     │    MEDIO       │
│     DESEJAVEL       │      N/A      │    <= 10%     │    BAIXO       │
└─────────────────────┴───────────────┴───────────────┴────────────────┘
```

### 9.3 Recomendações de Ação

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-GAP-020 | Ação Documental | Gap documental → "Obter documento X junto ao órgão Y". | PROC |
| RN-GAP-021 | Ação Técnica | Gap técnico → "Contratar/capacitar profissional com perfil X". | PROC |
| RN-GAP-022 | Ação Financeira | Gap financeiro → "Melhorar índice X" ou "Aumentar capital social". | PROC |
| RN-GAP-023 | Dificuldade | Sistema estima dificuldade: FACIL, MEDIO, DIFICIL, MUITO_DIFICIL. | CALC |

---

## 10. Regras de Relatório

### 10.1 Geração de Relatório

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-REL-001 | Análise Finalizada | Relatório só pode ser gerado para análises finalizadas. | VAL |
| RN-REL-002 | Timestamp | Relatório deve conter data/hora de geração. | PROC |
| RN-REL-003 | Versão Sistema | Relatório deve conter versão do sistema. | PROC |
| RN-REL-004 | Logo Empresa | Logo da empresa pode ser inserido no cabeçalho. | PROC |

### 10.2 Templates de Relatório

| Template | Páginas | Conteúdo |
|----------|---------|----------|
| EXECUTIVO | 2-3 | Resumo, scores, recomendação, principais gaps |
| DETALHADO | 10+ | Todos os requisitos, matches, gaps, observações |
| CHECKLIST | 1-2 | Lista de documentos necessários com status |

### 10.3 Exportação

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-REL-010 | Formato PDF | PDF deve ser exportável e imprimível (A4). | PROC |
| RN-REL-011 | Formato Excel | Excel deve ter abas: Resumo, Requisitos, Gaps, Matches. | PROC |
| RN-REL-012 | Formato JSON | JSON para backup e integração. | PROC |

---

## 11. Regras de Alerta

### 11.1 Criação de Alertas

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-ALT-001 | Vencimento Documento | Alerta criado X dias antes do vencimento (configurável). | PROC |
| RN-ALT-002 | Edital Próximo | Alerta criado 7 dias antes da data de abertura. | PROC |
| RN-ALT-003 | Gap Pendente | Alerta semanal para gaps não resolvidos. | PROC |
| RN-ALT-004 | Backup Necessário | Alerta se último backup > 7 dias. | PROC |

### 11.2 Prioridade de Alertas

| Prioridade | Cor | Exemplos |
|------------|-----|----------|
| CRITICA | Vermelho | Documento vencido, edital amanhã |
| ALTA | Laranja | Documento vencendo em 7 dias |
| MEDIA | Amarelo | Gap pendente, edital em 15 dias |
| BAIXA | Azul | Backup necessário |

---

## 12. Regras de Configuração

### 12.1 Parâmetros Configuráveis

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| analise.score_participar | 70 | Score mínimo para recomendar participação |
| analise.score_avaliar | 50 | Score mínimo para recomendar avaliação |
| analise.score_obrig_min | 90 | Score mínimo de obrigatórios para participar |
| documento.dias_alerta | 30 | Dias de antecedência para alertar vencimento |
| backup.automatico | true | Ativar backup automático |
| backup.intervalo_dias | 7 | Intervalo entre backups |
| sessao.timeout_minutos | 60 | Tempo de inatividade para encerrar sessão |

---

## 13. Regras de Segurança

### 13.1 Autenticação

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-SEG-001 | Senha Obrigatória | Sistema requer senha para acesso. | VAL |
| RN-SEG-002 | Hash de Senha | Senha armazenada com hash bcrypt. | PROC |
| RN-SEG-003 | Senha Mínima | Senha deve ter no mínimo 6 caracteres. | VAL |
| RN-SEG-004 | Timeout Sessão | Sessão encerra após X minutos de inatividade. | PROC |

### 13.2 Dados

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-SEG-010 | Criptografia BD | Banco de dados criptografado (SQLCipher). | PROC |
| RN-SEG-011 | Backup Criptografado | Backups são criptografados. | PROC |
| RN-SEG-012 | Dados Locais | Todos os dados ficam locais (sem cloud). | PROC |

### 13.3 Auditoria

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-SEG-020 | Log de Ações | Ações importantes são registradas em log. | PROC |
| RN-SEG-021 | Ações Auditadas | CREATE, UPDATE, DELETE, EXPORT são auditados. | PROC |
| RN-SEG-022 | Retenção Log | Logs são mantidos por 1 ano. | PROC |

---

## 14. Regras de Integração AMLDO

### 14.1 Extração via RAG

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-INT-001 | Timeout Extração | Timeout de 5 minutos para extração de requisitos. | PROC |
| RN-INT-002 | Retry Automático | Até 3 tentativas em caso de falha. | PROC |
| RN-INT-003 | Fallback Manual | Se falhar, permite extração manual. | PROC |

### 14.2 Consulta de Legislação

| ID | Regra | Descrição | Tipo |
|----|-------|-----------|------|
| RN-INT-010 | Base Legal | Consultas legais usam base do AMLDO (Lei 14.133, etc.). | PROC |
| RN-INT-011 | Contexto Edital | Consulta pode usar contexto do edital atual. | PROC |

---

## 15. Glossário de Termos

| Termo | Definição |
|-------|-----------|
| Licitante | Empresa que participa de licitação como fornecedora |
| Licitador | Órgão público que realiza a licitação |
| Edital | Documento com regras e requisitos da licitação |
| Requisito | Exigência do edital que deve ser atendida |
| Capacidade | Competência ou experiência da empresa |
| Certificação | Documento que comprova qualificação |
| Aderência | Grau de conformidade com requisitos |
| Gap | Requisito não atendido |
| Score | Pontuação de aderência (0-100) |
| Match | Correspondência entre requisito e capacidade |

---

*Documento de Regras de Negócio elaborado em Novembro/2024 como parte do planejamento do projeto LicitaFit.*
