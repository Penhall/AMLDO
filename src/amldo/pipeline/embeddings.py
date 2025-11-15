"""
Gerenciador de embeddings para o pipeline AMLDO.

Este módulo fornece embeddings REAIS (não dummy) usando sentence-transformers,
substituindo os embeddings aleatórios usados no POC LicitAI original.
"""

from __future__ import annotations

from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from amldo.core.config import settings
from amldo.core.exceptions import EmbeddingError


class EmbeddingManager:
    """
    Gerenciador de embeddings usando sentence-transformers.

    Fornece embeddings semânticos reais, otimizados para português (multilíngue).
    """

    def __init__(
        self,
        model_name: str | None = None,
        normalize: bool = True,
    ):
        """
        Inicializa o gerenciador de embeddings.

        Args:
            model_name: Nome do modelo sentence-transformers. Usa settings se None.
            normalize: Se True, normaliza os embeddings (recomendado para cosine similarity)

        Raises:
            EmbeddingError: Se falhar ao carregar o modelo
        """
        self.model_name = model_name or settings.embedding_model
        self.normalize = normalize

        try:
            self.model = SentenceTransformer(self.model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
        except Exception as e:
            raise EmbeddingError(
                f"Falha ao carregar modelo de embedding '{self.model_name}': {e}"
            ) from e

    def embed(self, texts: List[str]) -> np.ndarray:
        """
        Gera embeddings para uma lista de textos.

        Args:
            texts: Lista de textos para embedar

        Returns:
            Array numpy (n_texts, dimension) com embeddings

        Raises:
            EmbeddingError: Se falhar ao gerar embeddings
        """
        if not texts:
            raise ValueError("Lista de textos está vazia")

        try:
            embeddings = self.model.encode(
                texts,
                normalize_embeddings=self.normalize,
                show_progress_bar=False,
            )
            return embeddings.astype("float32")
        except Exception as e:
            raise EmbeddingError(f"Falha ao gerar embeddings: {e}") from e

    def embed_single(self, text: str) -> np.ndarray:
        """
        Gera embedding para um único texto.

        Args:
            text: Texto para embedar

        Returns:
            Array numpy (dimension,) com embedding

        Raises:
            EmbeddingError: Se falhar ao gerar embedding
        """
        return self.embed([text])[0]

    def __call__(self, texts: List[str]) -> List[List[float]]:
        """
        Torna a classe callable, compatível com assinatura EmbeddingFn do indexer.

        Args:
            texts: Lista de textos

        Returns:
            Lista de listas de floats (compatível com indexer legado)
        """
        embeddings = self.embed(texts)
        return embeddings.tolist()

    def __repr__(self) -> str:
        return (
            f"EmbeddingManager(model='{self.model_name}', "
            f"dimension={self.dimension}, normalize={self.normalize})"
        )


# =============================================================================
# Instância Global para uso direto
# =============================================================================

# Instância global configurada com settings
embedding_manager = EmbeddingManager()


# =============================================================================
# Funções de conveniência
# =============================================================================


def get_embedding_function() -> EmbeddingManager:
    """
    Retorna uma função de embedding configurada.

    Returns:
        EmbeddingManager configurado com settings globais
    """
    return embedding_manager


def embed_texts(texts: List[str]) -> np.ndarray:
    """
    Função de conveniência para embedar textos usando a instância global.

    Args:
        texts: Lista de textos

    Returns:
        Array numpy com embeddings
    """
    return embedding_manager.embed(texts)
