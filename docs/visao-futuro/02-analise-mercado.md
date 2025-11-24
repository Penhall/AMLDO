# Análise de Mercado
## LicitaFit - Sistema de Análise de Aderência a Editais

**Versão:** 1.0
**Data:** Novembro/2024

---

## 1. Visão Geral do Mercado

### 1.1 Mercado de Licitações no Brasil

O mercado de licitações públicas no Brasil movimenta aproximadamente **R$ 500 bilhões** por ano, envolvendo milhares de órgãos públicos e milhões de empresas fornecedoras.

#### Números do Mercado

| Indicador | Valor | Fonte |
|-----------|-------|-------|
| Volume anual de compras públicas | ~R$ 500 bi | Portal de Compras Gov |
| Número de licitações/ano | ~300.000 | ComprasNet |
| Empresas cadastradas no SICAF | ~500.000 | SICAF |
| MPEs em licitações | ~75% | Portal Gov |
| Taxa média de propostas/licitação | 3-5 | Estimativa |

#### Segmentação por Tipo de Licitação

```
┌─────────────────────────────────────────────────────────┐
│              TIPOS DE LICITAÇÃO (Volume)                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Pregão Eletrônico     ████████████████████  65%       │
│  Concorrência          ████████              15%       │
│  Tomada de Preços      ██████                10%       │
│  Convite               ████                   5%       │
│  Outros                ████                   5%       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Perfil das Empresas Licitantes

#### Distribuição por Porte

| Porte | % do Total | Características |
|-------|------------|-----------------|
| MEI | 15% | Participam de compras diretas e pregões simplificados |
| ME | 35% | Benefícios da LC 123/2006, participam ativamente |
| EPP | 25% | Volume significativo, estrutura básica de licitações |
| Média | 15% | Equipe dedicada, participam de licitações maiores |
| Grande | 10% | Departamentos especializados, licitações complexas |

#### Distribuição por Setor

| Setor | % Participação | Complexidade dos Editais |
|-------|----------------|-------------------------|
| Comércio | 40% | Baixa-Média |
| Serviços | 35% | Média-Alta |
| Indústria | 15% | Alta |
| Construção | 10% | Muito Alta |

---

## 2. Análise da Concorrência

### 2.1 Soluções Existentes no Mercado

#### Categoria 1: Portais de Licitação

| Solução | Foco | Preço | Funcionalidade de Análise |
|---------|------|-------|---------------------------|
| Licitações-e (BB) | Portal de pregões | Gratuito | Não possui |
| ComprasNet | Portal federal | Gratuito | Não possui |
| BEC-SP | Portal estadual SP | Gratuito | Não possui |
| Licitanet | Portal privado | ~R$ 300/mês | Básico |

#### Categoria 2: Agregadores/Buscadores

| Solução | Foco | Preço | Funcionalidade de Análise |
|---------|------|-------|---------------------------|
| Portal de Compras | Busca de licitações | Freemium | Não possui |
| Licitar Digital | Monitoramento | ~R$ 150/mês | Alertas básicos |
| LicitaCon | Busca e alertas | ~R$ 200/mês | Não possui |
| Bidding | Inteligência | ~R$ 500/mês | Limitado |

#### Categoria 3: Gestão de Propostas

| Solução | Foco | Preço | Funcionalidade de Análise |
|---------|------|-------|---------------------------|
| Neogrid | Gestão de compras | Enterprise | Focado em fornecedores |
| SAP Ariba | Supply chain | Enterprise | Não focado em licitações |
| Coupa | Procurement | Enterprise | Mercado privado |

### 2.2 Gap de Mercado Identificado

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MATRIZ DE FUNCIONALIDADES                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                    Busca    Gestão    Análise    Análise de         │
│  Solução          Editais   Docs     Requisitos  Aderência          │
│  ────────────────────────────────────────────────────────────────   │
│  Portal Gov.       ✓        ✗         ✗          ✗                │
│  Agregadores       ✓        ~         ✗          ✗                 │
│  Gestão Propostas  ✗        ✓         ~          ✗                 │
│  LicitaFit        (✓)*      ✓         ✓          ✓   ← DIFERENCIAL │
│                                                                     │
│  * Via importação manual                                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.3 Análise SWOT do LicitaFit

```
┌─────────────────────────────────┬─────────────────────────────────┐
│           FORÇAS (S)            │         FRAQUEZAS (W)           │
├─────────────────────────────────┼─────────────────────────────────┤
│ • Base RAG do AMLDO já pronta   │ • Novo no mercado               │
│ • Foco específico em aderência  │ • Sem base de usuários          │
│ • Tecnologia de IA moderna      │ • Necessita validação           │
│ • Desktop = privacidade         │ • Sem busca integrada           │
│ • Sem concorrente direto        │ • Equipe pequena                │
├─────────────────────────────────┼─────────────────────────────────┤
│       OPORTUNIDADES (O)         │          AMEAÇAS (T)            │
├─────────────────────────────────┼─────────────────────────────────┤
│ • Mercado carente de IA         │ • Grandes players podem copiar  │
│ • Nova Lei de Licitações        │ • Resistência a novas techs     │
│ • Digitalização acelerada       │ • Baixa maturidade digital MPEs │
│ • Demanda por eficiência        │ • Pirataria de software         │
│ • Parcerias com contadores      │ • Mudanças regulatórias         │
└─────────────────────────────────┴─────────────────────────────────┘
```

---

## 3. Proposta de Valor Única (UVP)

### 3.1 Posicionamento

> **LicitaFit**: A única ferramenta de análise de aderência a editais com inteligência artificial, que permite às empresas descobrir em minutos se vale a pena participar de uma licitação.

### 3.2 Diferenciadores Competitivos

| # | Diferenciador | Benefício | Concorrência |
|---|---------------|-----------|--------------|
| 1 | Extração automática de requisitos | 80% menos tempo de análise | Manual |
| 2 | Score de aderência calculado | Decisão objetiva | Subjetivo |
| 3 | Desktop offline | Segurança de dados | Cloud dependente |
| 4 | Base legal AMLDO | Consultas jurídicas integradas | Sem suporte legal |
| 5 | Preço acessível | Democratização | Enterprise |

### 3.3 Canvas de Proposta de Valor

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PROPOSTA DE VALOR                               │
├───────────────────────────────┬─────────────────────────────────────┤
│     PRODUTOS E SERVIÇOS       │         GANHOS DO CLIENTE           │
├───────────────────────────────┼─────────────────────────────────────┤
│ • Extração de requisitos PDF  │ • Economia de tempo (horas → min)   │
│ • Cadastro de perfil empresa  │ • Decisões baseadas em dados        │
│ • Cálculo de score aderência  │ • Maior taxa de aprovação           │
│ • Identificação de gaps       │ • Redução de custos com propostas   │
│ • Relatórios profissionais    │ • Organização de documentos         │
│ • Alertas de validade docs    │ • Menos surpresas na habilitação    │
├───────────────────────────────┼─────────────────────────────────────┤
│      ALIVIADORES DE DOR       │          DORES DO CLIENTE           │
├───────────────────────────────┼─────────────────────────────────────┤
│ • Análise automática          │ • Editais longos e complexos        │
│ • Checklist pronto            │ • Medo de esquecer documentos       │
│ • Categorização inteligente   │ • Dificuldade em priorizar editais  │
│ • Recomendações de ação       │ • Não saber se atende requisitos    │
│ • Backup local seguro         │ • Preocupação com dados sensíveis   │
└───────────────────────────────┴─────────────────────────────────────┘
```

---

## 4. Modelo de Negócio

### 4.1 Opções de Monetização

#### Opção A: Licença Perpétua

| Plano | Preço | Inclui |
|-------|-------|--------|
| Básico | R$ 497 | 1 empresa, atualizações 1 ano |
| Profissional | R$ 997 | 3 empresas, atualizações 2 anos |
| Consultor | R$ 1.997 | Ilimitado, atualizações vitalícias |

**Prós**: Receita upfront, sem fricção de pagamento recorrente
**Contras**: Previsibilidade de receita menor

#### Opção B: Assinatura (SaaS-like)

| Plano | Preço/Mês | Inclui |
|-------|-----------|--------|
| Starter | R$ 49 | 5 análises/mês, 1 empresa |
| Pro | R$ 149 | 20 análises/mês, 3 empresas |
| Business | R$ 349 | Ilimitado, suporte prioritário |

**Prós**: Receita recorrente previsível
**Contras**: Requer licenciamento online

#### Opção C: Modelo Híbrido (Recomendado)

| Componente | Preço | Descrição |
|------------|-------|-----------|
| Licença Base | R$ 297 | Acesso ao software |
| Créditos de Análise | R$ 5/análise | Pay-per-use |
| Pacote 50 análises | R$ 197 | Desconto de 21% |
| Pacote 200 análises | R$ 597 | Desconto de 40% |

**Prós**: Baixa barreira de entrada + escalabilidade
**Contras**: Complexidade de gestão

### 4.2 Projeção de Receita (Cenário Conservador)

| Mês | Usuários | Receita/Usuário | Receita Total |
|-----|----------|-----------------|---------------|
| 1-3 | 50 | R$ 150 | R$ 7.500 |
| 4-6 | 150 | R$ 150 | R$ 22.500 |
| 7-12 | 400 | R$ 150 | R$ 60.000 |
| Ano 2 | 1.000 | R$ 150 | R$ 150.000/mês |

### 4.3 Estrutura de Custos

| Item | Custo Mensal | % do Total |
|------|--------------|------------|
| Desenvolvimento (1-2 devs) | R$ 15.000 | 60% |
| Marketing/Vendas | R$ 5.000 | 20% |
| Infraestrutura (mínima) | R$ 500 | 2% |
| Suporte | R$ 2.000 | 8% |
| Outros | R$ 2.500 | 10% |
| **Total** | **R$ 25.000** | 100% |

---

## 5. Estratégia de Go-to-Market

### 5.1 Fases de Lançamento

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ESTRATÉGIA DE LANÇAMENTO                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FASE 1: VALIDAÇÃO              FASE 2: EARLY ADOPTERS              │
│  ┌─────────────────────┐       ┌─────────────────────┐             │
│  │ • 10-20 usuários    │       │ • 50-100 usuários   │             │
│  │ • Feedback intenso  │──────▶│ • Preço promocional │             │
│  │ • Iterações rápidas │       │ • Testimonials      │             │
│  │ • Gratuito/Desconto │       │ • Case studies      │             │
│  └─────────────────────┘       └─────────────────────┘             │
│           │                            │                            │
│           ▼                            ▼                            │
│  FASE 3: CRESCIMENTO           FASE 4: ESCALA                      │
│  ┌─────────────────────┐       ┌─────────────────────┐             │
│  │ • 500+ usuários     │       │ • 2000+ usuários    │             │
│  │ • Marketing digital │──────▶│ • Parcerias         │             │
│  │ • SEO/Conteúdo      │       │ • Novos canais      │             │
│  │ • Indicações        │       │ • Expansão produto  │             │
│  └─────────────────────┘       └─────────────────────┘             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 Canais de Aquisição

| Canal | Prioridade | Custo | Potencial |
|-------|------------|-------|-----------|
| SEO/Conteúdo | Alta | Baixo | Alto |
| LinkedIn | Alta | Médio | Alto |
| Parcerias (contadores) | Alta | Baixo | Muito Alto |
| YouTube (tutoriais) | Média | Baixo | Alto |
| Google Ads | Média | Alto | Médio |
| Eventos/Feiras | Baixa | Alto | Médio |

### 5.3 Parcerias Estratégicas

| Parceiro | Tipo | Benefício Mútuo |
|----------|------|-----------------|
| Escritórios de contabilidade | Revenda | Acesso a clientes, comissão |
| Sebrae | Institucional | Credibilidade, alcance |
| Sindicatos empresariais | Institucional | Acesso a associados |
| Consultores de licitação | Afiliado | Ferramenta para trabalho |
| Portais de licitação | Integração | Tráfego qualificado |

---

## 6. Análise de Risco de Mercado

### 6.1 Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Baixa adoção por MPEs | Média | Alto | Versão gratuita limitada, educação |
| Concorrente com IA | Média | Alto | First mover advantage, nicho |
| Mudança regulatória | Baixa | Médio | Flexibilidade no sistema |
| Pirataria | Alta | Médio | Modelo de créditos, funcionalidades cloud |
| Dependência de tecnologia | Baixa | Alto | Arquitetura modular |

### 6.2 Barreiras de Entrada para Concorrentes

| Barreira | Força | Descrição |
|----------|-------|-----------|
| Base RAG especializada | Alta | Anos de curadoria legal |
| Conhecimento de domínio | Alta | Expertise em licitações |
| Relacionamento com usuários | Média | Feedback loop |
| Marca/Reputação | Baixa (inicial) | A construir |
| Patentes | Baixa | Não aplicável |

---

## 7. Oportunidades de Expansão

### 7.1 Roadmap de Produto (Longo Prazo)

```
MVP                    v1.x                   v2.x                   v3.x
┌───────────┐         ┌───────────┐         ┌───────────┐         ┌───────────┐
│ Análise   │         │ Gestão de │         │ Integração│         │ IA        │
│ Aderência │────────▶│ Propostas │────────▶│ Portais   │────────▶│ Preditiva │
│ Desktop   │         │ Completas │         │ Gov       │         │ de Preços │
└───────────┘         └───────────┘         └───────────┘         └───────────┘
                                                                        │
                                                                        ▼
                                                                  ┌───────────┐
                                                                  │ Marketplace│
                                                                  │ de        │
                                                                  │ Licitações│
                                                                  └───────────┘
```

### 7.2 Novos Segmentos

| Segmento | Potencial | Adaptação Necessária |
|----------|-----------|---------------------|
| Órgãos públicos | Alto | Módulo de avaliação de propostas |
| Advogados | Médio | Análise de editais para impugnação |
| Investidores | Baixo | Due diligence de empresas licitantes |

---

## 8. Conclusões e Recomendações

### 8.1 Oportunidade Validada

O mercado de licitações apresenta uma oportunidade clara para uma ferramenta de análise de aderência:
- **Gap identificado**: Nenhuma solução atual oferece análise automatizada de aderência
- **Demanda real**: Empresas gastam horas em análise manual
- **Tecnologia disponível**: RAG do AMLDO já está operacional
- **Barreira de entrada**: Conhecimento especializado

### 8.2 Recomendações

1. **Iniciar com MVP Desktop** focado exclusivamente em análise de aderência
2. **Validar com 10-20 usuários** antes de investir em funcionalidades adicionais
3. **Modelo de precificação híbrido** (licença + créditos) para testar elasticidade
4. **Parcerias com consultores** como canal principal de aquisição
5. **Conteúdo educativo** para construir autoridade e SEO

### 8.3 Próximos Passos

1. Finalizar documentação técnica
2. Desenvolver protótipo de alta fidelidade
3. Recrutar usuários beta
4. Implementar MVP
5. Lançar programa de early adopters

---

*Análise de mercado elaborada em Novembro/2024 como parte do planejamento do projeto LicitaFit.*
