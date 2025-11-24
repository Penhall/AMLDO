# Prompts para Geração de Imagens - LicitaFit

Este diretório contém prompts otimizados para geração de imagens de UI/UX do sistema LicitaFit usando o aplicativo **NanoBanana** ou geradores de imagem similares.

---

## Estrutura dos Arquivos

| Arquivo | Conteúdo | Qtd Prompts |
|---------|----------|-------------|
| `01-telas-principais.md` | Telas da aplicação (Login, Dashboard, Formulários, etc.) | ~50 |
| `02-fluxos-interacao.md` | Fluxos, modais, notificações, navegação | ~50 |
| `03-mobile-icones-extras.md` | Logos, ícones, ilustrações, marketing | ~50 |

**Total: ~150 prompts**

---

## Como Usar

### 1. Prefixo Recomendado

Adicione este prefixo ao início de cada prompt para manter consistência:

```
Modern desktop application UI screenshot, professional business software,
clean minimalist design, Windows 11 style, light theme, Brazilian Portuguese
text labels, high quality render
```

### 2. Parâmetros Sugeridos no NanoBanana

- **Estilo**: UI/UX Design, Digital Art, ou Realistic
- **Proporção**: 16:9 para telas completas, 1:1 para ícones
- **Qualidade**: Alta ou Máxima
- **Passos**: 30-50 para melhor qualidade

### 3. Ordem de Geração Sugerida

1. **Logo e Identidade** (Seção 21) - Definir visual base
2. **Dashboard** (Seção 3) - Tela principal de referência
3. **Componentes** (Seção 10) - Score gauges, badges
4. **Fluxos** (Seção 11) - Entender jornadas do usuário
5. **Demais telas** - Conforme necessidade

---

## Paleta de Cores

Use estas cores nos prompts quando relevante:

| Cor | Hex | Uso |
|-----|-----|-----|
| Azul Primário | `#2563EB` | Botões, links, destaques |
| Azul Escuro | `#1E3A5F` | Sidebar, headers |
| Verde Sucesso | `#22C55E` | Score alto, confirmações |
| Amarelo Alerta | `#EAB308` | Score médio, avisos |
| Vermelho Erro | `#EF4444` | Score baixo, erros |
| Cinza Fundo | `#F9FAFB` | Background geral |
| Cinza Texto | `#111827` | Texto principal |

---

## Categorias de Prompts

### Telas Principais (01)
- Splash Screen e Loading
- Login e Autenticação
- Dashboard
- Gestão de Empresas
- Gestão de Editais
- Análise de Aderência
- Relatórios
- Configurações
- Estados (vazio, erro, carregando)
- Componentes (gauges, cards, badges)

### Fluxos e Interação (02)
- Storyboards de fluxos
- Modais e diálogos
- Notificações e toasts
- Menus e navegação
- Formulários e inputs
- Tabelas e listas
- Gráficos e visualizações
- Responsividade
- Onboarding
- Impressão/Exportação

### Ícones e Extras (03)
- Logo e variações
- Ícones de navegação
- Ícones de status
- Ilustrações de estados
- Mockups de dispositivo
- Diagramas técnicos
- Material de marketing
- Screenshots documentação
- Telas de instalação
- Elementos de acessibilidade

---

## Exemplos de Uso

### Exemplo 1: Dashboard Completo
```
Modern desktop application dashboard screenshot, professional business
software, sidebar navigation on left with icons (Dashboard highlighted,
Empresas, Editais, Análises, Relatórios), main content area showing 4
metric cards (Empresas: 3, Editais: 12, Análises: 8, Alertas: 5), recent
analyses list below with percentage scores and colored indicators, blue
accent color #2563EB, white background, Windows 11 style, Brazilian
Portuguese labels, 1920x1080, high quality render
```

### Exemplo 2: Score Gauge
```
Desktop UI component, large circular score gauge, percentage "78%" in
center with bold font, circular progress arc in green #22C55E, label
"Score Global" below, subtle shadow, modern gauge design, white background,
clean minimal style
```

### Exemplo 3: Card de Gap
```
Desktop list item component, gap card with red left border #EF4444,
red X icon, requirement text in Portuguese, badges "Obrigatório" and
"Financeiro", severity badge "ALTA", "Ver detalhes" button, subtle
card shadow, warning design style
```

---

## Dicas para Melhores Resultados

1. **Seja específico**: Inclua detalhes sobre cores, layout, e elementos
2. **Mantenha consistência**: Use os mesmos termos de estilo em todos os prompts
3. **Especifique texto**: Mencione que os labels devem estar em português
4. **Resolução**: Indique 1920x1080 para screenshots, 256x256 para ícones
5. **Iteração**: Gere múltiplas versões e refine o prompt

---

## Próximos Passos

Após gerar as imagens:

1. Organize em pastas por categoria
2. Crie um documento visual compilado (PDF/Figma)
3. Use para validação com stakeholders
4. Refine prompts baseado no feedback
5. Gere variações (dark mode, responsivo, etc.)

---

*Prompts criados para o projeto LicitaFit - Novembro/2024*
