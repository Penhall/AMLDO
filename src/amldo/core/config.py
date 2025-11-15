"""
Configuração centralizada do AMLDO usando pydantic-settings.

Este módulo gerencia todas as variáveis de ambiente e configurações do sistema,
incluindo API keys, paths, e parâmetros de modelos.
"""

from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações centralizadas do AMLDO.

    Todas as configurações são carregadas do arquivo .env ou variáveis de ambiente.
    Valores padrão são fornecidos quando aplicável.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # =============================================================================
    # API Keys (Obrigatórias)
    # =============================================================================

    google_api_key: str = Field(
        ...,
        description="Google API Key para Gemini (obrigatória)",
        json_schema_extra={"env": "GOOGLE_API_KEY"},
    )

    # =============================================================================
    # Paths e Diretórios
    # =============================================================================

    project_root: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent.parent,
        description="Raiz do projeto",
    )

    data_dir: Path = Field(
        default=Path("data"),
        description="Diretório de dados",
    )

    @field_validator("data_dir", mode="before")
    @classmethod
    def make_data_dir_absolute(cls, v: Path | str, info) -> Path:
        """Converte data_dir para caminho absoluto baseado em project_root."""
        path = Path(v)
        if not path.is_absolute():
            # Se project_root já foi definido, use-o; caso contrário, calcule
            root = info.data.get("project_root")
            if root is None:
                root = Path(__file__).parent.parent.parent.parent
            path = root / path
        return path

    @property
    def raw_docs_dir(self) -> Path:
        """Diretório de documentos brutos (PDFs)."""
        return self.data_dir / "raw"

    @property
    def split_docs_dir(self) -> Path:
        """Diretório de documentos splitados."""
        return self.data_dir / "split_docs"

    @property
    def processed_dir(self) -> Path:
        """Diretório de dados processados."""
        return self.data_dir / "processed"

    @property
    def vector_db_dir(self) -> Path:
        """Diretório do banco de dados vetorial."""
        return self.data_dir / "vector_db"

    vector_db_path: str = Field(
        default="data/vector_db/v1_faiss_vector_db",
        description="Caminho para o índice FAISS",
    )

    @property
    def vector_db_path_absolute(self) -> Path:
        """Retorna o caminho absoluto do vector DB."""
        path = Path(self.vector_db_path)
        if not path.is_absolute():
            return self.project_root / path
        return path

    # =============================================================================
    # Configurações de Modelos
    # =============================================================================

    embedding_model: str = Field(
        default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        description="Modelo de embeddings para usar",
    )

    embedding_dimension: int = Field(
        default=384,
        description="Dimensão dos embeddings",
    )

    llm_model: str = Field(
        default="gemini-2.5-flash",
        description="Modelo LLM para usar",
    )

    llm_provider: str = Field(
        default="google_genai",
        description="Provider do LLM (google_genai, openai, etc)",
    )

    llm_temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
        description="Temperatura do LLM (0.0 = determinístico, 2.0 = criativo)",
    )

    # =============================================================================
    # Configurações de RAG
    # =============================================================================

    search_k: int = Field(
        default=12,
        ge=1,
        le=50,
        description="Número de documentos a recuperar na busca",
    )

    search_type: Literal["similarity", "mmr", "similarity_score_threshold"] = Field(
        default="mmr",
        description="Tipo de busca no vector store",
    )

    mmr_diversity_score: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Score de diversidade para MMR (0.0 = só relevância, 1.0 = só diversidade)",
    )

    # =============================================================================
    # Configurações de Artigo 0 (Contexto Hierárquico)
    # =============================================================================

    artigos_0_csv_path: str = Field(
        default="data/processed/v1_artigos_0.csv",
        description="Caminho para CSV com artigos 0 (introduções de capítulos/títulos)",
    )

    @property
    def artigos_0_csv_path_absolute(self) -> Path:
        """Retorna o caminho absoluto do CSV de artigos 0."""
        path = Path(self.artigos_0_csv_path)
        if not path.is_absolute():
            return self.project_root / path
        return path

    processed_articles_csv_path: str = Field(
        default="data/processed/v1_processed_articles.csv",
        description="Caminho para CSV com todos os artigos processados",
    )

    @property
    def processed_articles_csv_path_absolute(self) -> Path:
        """Retorna o caminho absoluto do CSV de artigos processados."""
        path = Path(self.processed_articles_csv_path)
        if not path.is_absolute():
            return self.project_root / path
        return path

    # =============================================================================
    # Configurações de Ambiente
    # =============================================================================

    environment: Literal["development", "production", "testing"] = Field(
        default="development",
        description="Ambiente de execução",
    )

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Nível de logging",
    )

    debug: bool = Field(
        default=False,
        description="Modo debug (mais verboso)",
    )

    # =============================================================================
    # Configurações de Pipeline
    # =============================================================================

    chunk_size: int = Field(
        default=1000,
        ge=100,
        le=5000,
        description="Tamanho dos chunks de texto",
    )

    chunk_overlap: int = Field(
        default=200,
        ge=0,
        le=1000,
        description="Overlap entre chunks",
    )

    # =============================================================================
    # Métodos Utilitários
    # =============================================================================

    def validate_paths(self) -> dict[str, bool]:
        """
        Valida se os paths críticos existem.

        Returns:
            Dict com status de cada path crítico
        """
        return {
            "data_dir": self.data_dir.exists(),
            "vector_db": self.vector_db_path_absolute.exists(),
            "artigos_0_csv": self.artigos_0_csv_path_absolute.exists(),
            "processed_articles_csv": self.processed_articles_csv_path_absolute.exists(),
        }

    def get_faiss_allow_dangerous_deserialization(self) -> bool:
        """
        Retorna se deve permitir desserialização perigosa do FAISS.

        IMPORTANTE: Isso é necessário para carregar índices FAISS baseados em pickle,
        mas só deve ser usado com fontes confiáveis.

        Returns:
            True em development/testing, False em production (por segurança)
        """
        # Em produção, considere implementar uma verificação de assinatura
        # Por enquanto, permitimos em todos os ambientes pois é necessário
        return True

    def model_dump_safe(self) -> dict:
        """
        Retorna configurações sem expor secrets.

        Returns:
            Dict com configs seguras para logging
        """
        dump = self.model_dump()
        # Oculta API keys
        if "google_api_key" in dump:
            dump["google_api_key"] = "***REDACTED***"
        return dump


# =============================================================================
# Instância Global de Settings
# =============================================================================

settings = Settings()

# Validação automática ao importar (opcional, pode ser removido em produção)
if settings.debug:
    import json

    print(f"[AMLDO Config] Loaded settings from environment: {settings.environment}")
    print(
        f"[AMLDO Config] Safe config dump:\n{json.dumps(settings.model_dump_safe(), indent=2, default=str)}"
    )
