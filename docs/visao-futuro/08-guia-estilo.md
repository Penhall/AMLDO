# Guia de Estilo Visual
## LicitaFit - Sistema de Análise de Aderência a Editais

**Versão:** 1.0
**Data:** Novembro/2024

---

## 1. Identidade Visual

### 1.1 Logo

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│         ╔═══╗                                                  │
│         ║ L ║  LicitaFit                                       │
│         ╚═══╝                                                  │
│                                                                 │
│         Versão completa (horizontal)                           │
│                                                                 │
│         ╔═══╗                                                  │
│         ║ L ║                                                   │
│         ╚═══╝                                                  │
│                                                                 │
│         Versão ícone (apenas símbolo)                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Cores Principais

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                               PALETA DE CORES                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  CORES PRIMÁRIAS                                                                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                                   │
│  │            │  │            │  │            │                                   │
│  │  Azul      │  │  Azul      │  │  Azul      │                                   │
│  │  Primário  │  │  Escuro    │  │  Claro     │                                   │
│  │            │  │            │  │            │                                   │
│  │  #2563EB   │  │  #1D4ED8   │  │  #60A5FA   │                                   │
│  └────────────┘  └────────────┘  └────────────┘                                   │
│                                                                                     │
│  CORES SEMÂNTICAS                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐                   │
│  │            │  │            │  │            │  │            │                   │
│  │  Sucesso   │  │  Atenção   │  │  Erro      │  │  Info      │                   │
│  │  (Verde)   │  │  (Amarelo) │  │  (Vermelho)│  │  (Azul)    │                   │
│  │            │  │            │  │            │  │            │                   │
│  │  #10B981   │  │  #F59E0B   │  │  #EF4444   │  │  #3B82F6   │                   │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘                   │
│                                                                                     │
│  CORES NEUTRAS                                                                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  │
│  │            │  │            │  │            │  │            │  │            │  │
│  │  Texto     │  │  Texto     │  │  Borda     │  │  Fundo     │  │  Branco    │  │
│  │  Principal │  │  Secundário│  │            │  │            │  │            │  │
│  │            │  │            │  │            │  │            │  │            │  │
│  │  #1F2937   │  │  #6B7280   │  │  #D1D5DB   │  │  #F3F4F6   │  │  #FFFFFF   │  │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘  └────────────┘  │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Tipografia

| Uso | Fonte | Peso | Tamanho |
|-----|-------|------|---------|
| Título H1 | Segoe UI | Bold (700) | 24px |
| Título H2 | Segoe UI | Semibold (600) | 20px |
| Título H3 | Segoe UI | Semibold (600) | 16px |
| Corpo | Segoe UI | Regular (400) | 14px |
| Corpo pequeno | Segoe UI | Regular (400) | 12px |
| Label | Segoe UI | Medium (500) | 12px |
| Botão | Segoe UI | Semibold (600) | 14px |
| Código | Consolas | Regular (400) | 13px |

---

## 2. Componentes Visuais

### 2.1 Botões

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   BOTÕES                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  PRIMÁRIO                                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │    Salvar      │  │    Salvar      │  │    Salvar      │  │    Salvar      │   │
│  │    (Normal)    │  │    (Hover)     │  │    (Active)    │  │   (Disabled)   │   │
│  │   #2563EB      │  │   #1D4ED8      │  │   #1E40AF      │  │   #93C5FD      │   │
│  └────────────────┘  └────────────────┘  └────────────────┘  └────────────────┘   │
│                                                                                     │
│  SECUNDÁRIO                                                                        │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │   Cancelar     │  │   Cancelar     │  │   Cancelar     │  │   Cancelar     │   │
│  │   (Normal)     │  │   (Hover)      │  │   (Active)     │  │  (Disabled)    │   │
│  │   Borda azul   │  │   Fundo leve   │  │   Fundo azul   │  │   Opacidade    │   │
│  └────────────────┘  └────────────────┘  └────────────────┘  └────────────────┘   │
│                                                                                     │
│  PERIGO                                                                            │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │    Excluir     │  │    Excluir     │  │    Excluir     │  │    Excluir     │   │
│  │   (Normal)     │  │   (Hover)      │  │   (Active)     │  │  (Disabled)    │   │
│  │   #EF4444      │  │   #DC2626      │  │   #B91C1C      │  │   #FCA5A5      │   │
│  └────────────────┘  └────────────────┘  └────────────────┘  └────────────────┘   │
│                                                                                     │
│  Especificações:                                                                   │
│  - Padding: 8px 16px (normal), 6px 12px (pequeno), 10px 20px (grande)             │
│  - Border-radius: 6px                                                              │
│  - Transição: 150ms ease                                                          │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Campos de Formulário

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CAMPOS DE FORMULÁRIO                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  CAMPO DE TEXTO                                                                    │
│                                                                                     │
│  Label do campo *                                                                  │
│  ┌────────────────────────────────────────────────────────────┐                   │
│  │ Placeholder ou valor                                       │                   │
│  └────────────────────────────────────────────────────────────┘                   │
│  Texto de ajuda (opcional)                                                        │
│                                                                                     │
│  Estados:                                                                          │
│  - Normal: Borda #D1D5DB                                                          │
│  - Focus: Borda #2563EB + sombra azul                                             │
│  - Erro: Borda #EF4444 + mensagem vermelha                                        │
│  - Disabled: Fundo #F3F4F6, texto #9CA3AF                                         │
│                                                                                     │
│  Especificações:                                                                   │
│  - Altura: 40px                                                                    │
│  - Padding: 10px 12px                                                             │
│  - Border-radius: 6px                                                              │
│  - Font-size: 14px                                                                │
│                                                                                     │
│  DROPDOWN / SELECT                                                                 │
│                                                                                     │
│  Modalidade *                                                                      │
│  ┌────────────────────────────────────────────────────────┬───┐                   │
│  │ Selecione...                                          │ ▼ │                   │
│  └────────────────────────────────────────────────────────┴───┘                   │
│                                                                                     │
│  CHECKBOX                                                                          │
│  ┌───┐                                                                            │
│  │ ✓ │ Opção selecionada                                                          │
│  └───┘                                                                            │
│  ┌───┐                                                                            │
│  │   │ Opção não selecionada                                                      │
│  └───┘                                                                            │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Cards

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    CARDS                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  CARD PADRÃO                                                                       │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                               │ │
│  │  Título do Card                                                               │ │
│  │  ────────────────────────────────────────────────────────────────────────────│ │
│  │                                                                               │ │
│  │  Conteúdo do card com informações relevantes                                  │ │
│  │  e outros elementos.                                                          │ │
│  │                                                                               │ │
│  │                                                          [Ação 1] [Ação 2]   │ │
│  └───────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                     │
│  Especificações:                                                                   │
│  - Background: #FFFFFF                                                             │
│  - Border: 1px solid #E5E7EB                                                       │
│  - Border-radius: 8px                                                              │
│  - Shadow: 0 1px 3px rgba(0,0,0,0.1)                                              │
│  - Padding: 16px                                                                   │
│                                                                                     │
│  CARD ESTATÍSTICA                                                                  │
│  ┌─────────────────────────────────────┐                                          │
│  │                                     │                                          │
│  │   EDITAIS                          │                                          │
│  │                                     │                                          │
│  │      12                             │                                          │
│  │   importados                        │                                          │
│  │                                     │                                          │
│  └─────────────────────────────────────┘                                          │
│                                                                                     │
│  Especificações:                                                                   │
│  - Número grande: 32px, Bold                                                       │
│  - Label: 12px, cor secundária                                                    │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.4 Tabelas

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   TABELAS                                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │  Coluna 1          Coluna 2          Coluna 3          Ações               │   │
│  ├─────────────────────────────────────────────────────────────────────────────┤   │
│  │  Valor 1           Valor 2           Valor 3           [E] [X]             │   │
│  │  ─────────────────────────────────────────────────────────────────────────  │   │
│  │  Valor 1           Valor 2           Valor 3           [E] [X]             │   │
│  │  ─────────────────────────────────────────────────────────────────────────  │   │
│  │  Valor 1           Valor 2           Valor 3           [E] [X]             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│  Especificações:                                                                   │
│  - Cabeçalho: Background #F9FAFB, texto #374151, Bold                             │
│  - Linhas alternadas (zebra): #FFFFFF / #F9FAFB                                   │
│  - Linha hover: #F3F4F6                                                            │
│  - Padding células: 12px 16px                                                      │
│  - Borda: 1px solid #E5E7EB                                                        │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Ícones

### 3.1 Biblioteca de Ícones

Utilizar **Lucide Icons** (fork do Feather Icons) por ser leve e consistente.

### 3.2 Ícones do Sistema

| Ícone | Uso | Nome Lucide |
|-------|-----|-------------|
| Home | Dashboard | `home` |
| Empresa | Empresas | `building-2` |
| Documento | Editais | `file-text` |
| Análise | Análises | `bar-chart-2` |
| Relatório | Relatórios | `file-chart` |
| Config | Configurações | `settings` |
| Adicionar | Novo item | `plus` |
| Editar | Editar | `pencil` |
| Excluir | Excluir | `trash-2` |
| Buscar | Busca | `search` |
| Upload | Upload arquivo | `upload` |
| Download | Download | `download` |
| Check | Sucesso/Atendido | `check` |
| X | Erro/Não atendido | `x` |
| Alerta | Aviso | `alert-triangle` |
| Info | Informação | `info` |
| Expandir | Expandir | `chevron-down` |
| Recolher | Recolher | `chevron-up` |

---

## 4. Espaçamento

### 4.1 Sistema de Grid

| Token | Valor | Uso |
|-------|-------|-----|
| `space-1` | 4px | Mínimo entre elementos |
| `space-2` | 8px | Pequeno |
| `space-3` | 12px | Interno de componentes |
| `space-4` | 16px | Padrão |
| `space-5` | 20px | Entre seções |
| `space-6` | 24px | Grande |
| `space-8` | 32px | Entre blocos |
| `space-10` | 40px | Separação de seções |

### 4.2 Layout

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                  GRID DO LAYOUT                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌──────────────────────────────────────────────────────────────────────────────┐  │
│  │ Sidebar: 240px (fixo)                                                        │  │
│  │                                                                              │  │
│  │ ┌────────────────────────────────────────────────────────────────────────┐  │  │
│  │ │                                                                        │  │  │
│  │ │ Área de conteúdo: flex (100% - 240px)                                  │  │  │
│  │ │                                                                        │  │  │
│  │ │ Padding interno: 24px                                                  │  │  │
│  │ │                                                                        │  │  │
│  │ │ Max-width do conteúdo: 1200px                                         │  │  │
│  │ │                                                                        │  │  │
│  │ └────────────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                              │  │
│  └──────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                     │
│  Barra de status: 32px (fixo, inferior)                                            │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Tema Escuro (Dark Mode)

### 5.1 Paleta Dark

| Elemento | Light | Dark |
|----------|-------|------|
| Background | #FFFFFF | #1F2937 |
| Background secundário | #F3F4F6 | #111827 |
| Texto principal | #1F2937 | #F9FAFB |
| Texto secundário | #6B7280 | #9CA3AF |
| Borda | #D1D5DB | #374151 |
| Primário | #2563EB | #3B82F6 |
| Card | #FFFFFF | #374151 |

### 5.2 Alternância

- Botão de toggle no rodapé ou configurações
- Respeitar preferência do sistema operacional
- Salvar preferência do usuário

---

## 6. Animações e Transições

| Elemento | Propriedade | Duração | Timing |
|----------|-------------|---------|--------|
| Botões | background, border | 150ms | ease |
| Campos focus | border, shadow | 200ms | ease-out |
| Modais | opacity, transform | 200ms | ease-out |
| Sidebar collapse | width | 200ms | ease |
| Cards hover | shadow | 150ms | ease |
| Loading spinner | rotation | 1000ms | linear |
| Toast | translate, opacity | 300ms | ease |
| Dropdown | max-height | 200ms | ease-out |

---

*Guia de Estilo elaborado em Novembro/2024.*
