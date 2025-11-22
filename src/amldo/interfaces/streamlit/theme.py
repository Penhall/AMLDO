"""
Tema Chat ONN para AMLDO Streamlit.

Inspirado em: Chat ONN UI
Identidade: Claro, moderno, roxo/violeta como destaque
CSS compartilhado entre todas as páginas.
"""

CHAT_ONN_THEME_CSS = """
<style>
/* =============================================================================
   AMLDO Streamlit - Tema Chat ONN (Light Purple/Violet)
   Inspirado em: Chat ONN UI
   Identidade: Claro, moderno, limpo com acentos roxo/violeta
   ============================================================================= */

/* Importar fonte */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Cores principais - Chat ONN Light */
:root {
    --bg-primary: #f8f9fc;
    --bg-secondary: #ffffff;
    --bg-sidebar: #6c5ce7;
    --bg-sidebar-dark: #5b4cdb;
    --bg-card: #ffffff;
    --bg-input: #f1f3f9;
    --bg-hover: #f0f0f5;

    /* Acentos - Roxo/Violeta */
    --accent-primary: #6c5ce7;
    --accent-secondary: #a29bfe;
    --accent-light: #e8e5ff;
    --accent-gradient: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);

    /* Texto */
    --text-primary: #2d3436;
    --text-secondary: #636e72;
    --text-muted: #b2bec3;
    --text-white: #ffffff;

    /* Status */
    --success: #00b894;
    --warning: #fdcb6e;
    --error: #e17055;
    --info: #74b9ff;

    /* Bordas */
    --border-color: #e9ecef;
    --border-light: #f1f3f5;

    /* Sombras */
    --shadow-sm: 0 2px 8px rgba(108, 92, 231, 0.08);
    --shadow-md: 0 4px 16px rgba(108, 92, 231, 0.12);
    --shadow-lg: 0 8px 32px rgba(108, 92, 231, 0.15);

    /* Efeitos */
    --transition: all 0.2s ease;
    --radius: 16px;
    --radius-sm: 10px;
    --radius-xs: 6px;
}

/* Base */
.stApp {
    background: var(--bg-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Sidebar - Roxo gradiente como Chat ONN */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-sidebar) 0%, var(--bg-sidebar-dark) 100%) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: rgba(255, 255, 255, 0.9) !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text-white) !important;
}

/* Headers */
h1 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    font-size: 1.75rem !important;
}

h2 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 1.25rem !important;
}

h3 {
    color: var(--accent-primary) !important;
    font-weight: 600 !important;
}

/* Main container */
.main .block-container {
    padding: 2rem 3rem !important;
    max-width: 1200px !important;
}

/* Cards/Containers */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-sm) !important;
}

[data-testid="stExpander"]:hover {
    box-shadow: var(--shadow-md) !important;
}

/* Botões - Estilo Chat ONN */
.stButton > button {
    background: var(--accent-gradient) !important;
    color: var(--text-white) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.625rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    transition: var(--transition) !important;
    box-shadow: var(--shadow-sm) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-md) !important;
    opacity: 0.95 !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Botão secundário */
.stButton > button[kind="secondary"] {
    background: var(--bg-card) !important;
    color: var(--accent-primary) !important;
    border: 2px solid var(--accent-primary) !important;
}

.stButton > button[kind="secondary"]:hover {
    background: var(--accent-light) !important;
}

/* Inputs - Estilo Chat ONN */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-input) !important;
    border: 2px solid transparent !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.9rem !important;
    transition: var(--transition) !important;
    color: var(--text-primary) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px var(--accent-light) !important;
    background: var(--bg-card) !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--text-muted) !important;
}

/* Select boxes */
.stSelectbox > div > div {
    background: var(--bg-input) !important;
    border: 2px solid transparent !important;
    border-radius: var(--radius-sm) !important;
}

.stSelectbox > div > div:focus-within {
    border-color: var(--accent-primary) !important;
}

/* Radio buttons - Estilo Chat ONN */
.stRadio > div {
    background: var(--bg-card) !important;
    padding: 1rem !important;
    border-radius: var(--radius) !important;
    border: 1px solid var(--border-color) !important;
}

.stRadio > div > label {
    padding: 0.5rem 1rem !important;
    border-radius: var(--radius-xs) !important;
    transition: var(--transition) !important;
}

.stRadio > div > label:hover {
    background: var(--bg-hover) !important;
}

/* Checkboxes */
.stCheckbox > label > span {
    color: var(--text-primary) !important;
}

/* Métricas - Estilo Chat ONN */
[data-testid="stMetricValue"] {
    color: var(--accent-primary) !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}

[data-testid="stMetricDelta"] {
    color: var(--success) !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    padding: 1.25rem !important;
    border-radius: var(--radius) !important;
    border: 1px solid var(--border-color) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* Alertas - Estilo Chat ONN */
.stAlert {
    border-radius: var(--radius-sm) !important;
    border: none !important;
    padding: 1rem 1.25rem !important;
}

[data-testid="stAlert"] {
    border-radius: var(--radius-sm) !important;
}

/* Info alert */
.stAlert[data-baseweb="notification"][kind="info"] {
    background: linear-gradient(135deg, var(--accent-light) 0%, #f0edff 100%) !important;
    border-left: 4px solid var(--accent-primary) !important;
}

/* Success alert */
.stAlert[data-baseweb="notification"][kind="success"] {
    background: linear-gradient(135deg, #d4f5ed 0%, #e8faf5 100%) !important;
    border-left: 4px solid var(--success) !important;
}

/* Warning alert */
.stAlert[data-baseweb="notification"][kind="warning"] {
    background: linear-gradient(135deg, #fef5e1 0%, #fffbf0 100%) !important;
    border-left: 4px solid var(--warning) !important;
}

/* Error alert */
.stAlert[data-baseweb="notification"][kind="error"] {
    background: linear-gradient(135deg, #fde8e4 0%, #fef5f3 100%) !important;
    border-left: 4px solid var(--error) !important;
}

/* Dividers */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent) !important;
    margin: 2rem 0 !important;
}

/* File uploader - Estilo Chat ONN */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 2px dashed var(--accent-secondary) !important;
    border-radius: var(--radius) !important;
    padding: 2rem !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-primary) !important;
    background: var(--accent-light) !important;
}

[data-testid="stFileUploader"] label {
    color: var(--accent-primary) !important;
    font-weight: 500 !important;
}

/* Slider */
.stSlider > div > div > div {
    background: var(--accent-gradient) !important;
}

.stSlider > div > div > div > div {
    background: var(--accent-primary) !important;
    border: 3px solid var(--bg-card) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* Tabs - Estilo Chat ONN */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-input) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.25rem !important;
    gap: 0.25rem !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-xs) !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    padding: 0.5rem 1rem !important;
}

.stTabs [aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--accent-primary) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* Code blocks */
code {
    background: var(--accent-light) !important;
    color: var(--accent-primary) !important;
    padding: 0.2rem 0.5rem !important;
    border-radius: var(--radius-xs) !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 0.85rem !important;
}

pre {
    background: #2d3436 !important;
    border-radius: var(--radius-sm) !important;
    padding: 1rem !important;
}

pre code {
    background: transparent !important;
    color: #dfe6e9 !important;
}

/* Dataframes */
.stDataFrame {
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-sm) !important;
}

/* Progress bar */
.stProgress > div > div {
    background: var(--accent-gradient) !important;
    border-radius: 10px !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px !important;
    height: 8px !important;
}

::-webkit-scrollbar-track {
    background: var(--bg-input) !important;
    border-radius: 4px !important;
}

::-webkit-scrollbar-thumb {
    background: var(--accent-secondary) !important;
    border-radius: 4px !important;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-primary) !important;
}

/* Links */
a {
    color: var(--accent-primary) !important;
    text-decoration: none !important;
    font-weight: 500 !important;
}

a:hover {
    text-decoration: underline !important;
}

/* Custom classes */
.chat-onn-header {
    background: var(--accent-gradient);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: var(--radius);
    margin-bottom: 2rem;
    box-shadow: var(--shadow-md);
}

.chat-onn-header h1 {
    color: white !important;
    margin: 0 !important;
    font-size: 1.5rem !important;
}

.chat-onn-header p {
    color: rgba(255, 255, 255, 0.85) !important;
    margin: 0.5rem 0 0 0 !important;
}

.chat-onn-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 0.75rem;
}

.chat-onn-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
}

.chat-onn-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

/* Notification badges like Chat ONN */
.notification-badge {
    background: var(--error);
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.15rem 0.4rem;
    border-radius: 10px;
    min-width: 18px;
    text-align: center;
}

/* Online status indicator */
.status-online {
    width: 10px;
    height: 10px;
    background: var(--success);
    border-radius: 50%;
    display: inline-block;
    margin-right: 0.5rem;
}

/* Avatar style */
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--accent-gradient);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
}

/* Responsivo */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem !important;
    }

    h1 {
        font-size: 1.5rem !important;
    }
}
</style>
"""


def apply_theme():
    """Aplica o tema Chat ONN na página atual."""
    import streamlit as st
    st.markdown(CHAT_ONN_THEME_CSS, unsafe_allow_html=True)
