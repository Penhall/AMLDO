"""
Módulo de indexação vetorial (FAISS) para normas estruturadas.

IMPORTANTE: Versão refatorada que usa embeddings REAIS (sentence-transformers)
em vez dos embeddings dummy aleatórios do POC original.

Refatorado do LicitAI POC com:
- Embeddings reais via EmbeddingManager
- Type hints melhorados
- Error handling robusto
- Integração com config centralizado
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import numpy as np

from amldo.core.exceptions import IndexingError
from amldo.pipeline.embeddings import EmbeddingManager, get_embedding_function

try:
    import faiss  # type: ignore
except ImportError:
    faiss = None  # type: ignore


# Type alias para função de embedding
# Aceita lista de strings, retorna lista de listas de floats
EmbeddingFn = Callable[[List[str]], List[List[float]]]


def load_artigos_from_jsonl(path: str) -> List[Dict]:
    """
    Carrega artigos de um arquivo JSONL.

    Args:
        path: Caminho para o arquivo JSONL

    Returns:
        Lista de artigos (dicts)

    Raises:
        FileNotFoundError: Se arquivo não existir
        IndexingError: Se falhar ao carregar o arquivo
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Arquivo JSONL de artigos não encontrado: {p}")

    try:
        artigos: List[Dict] = []
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                artigos.append(json.loads(line))
        return artigos
    except Exception as e:
        raise IndexingError(f"Falha ao carregar artigos de {path}: {e}") from e


def build_embeddings(
    artigos: List[Dict],
    embedding_fn: EmbeddingFn,
) -> Tuple[List[str], List[List[float]]]:
    """
    Gera embeddings para os artigos usando a função fornecida.

    Args:
        artigos: Lista de artigos (dicts com keys 'id' e 'text')
        embedding_fn: Função que gera embeddings

    Returns:
        Tupla (ids, vectors):
            - ids: Lista de IDs dos artigos
            - vectors: Lista de embeddings (lista de floats)

    Raises:
        IndexingError: Se falhar ao gerar embeddings
    """
    try:
        texts = [a.get("text", "") for a in artigos]
        ids = [a.get("id", "") for a in artigos]

        vectors = embedding_fn(texts)

        if len(vectors) != len(texts):
            raise IndexingError(
                f"embedding_fn deve retornar um vetor por texto. "
                f"Recebeu {len(vectors)} vetores para {len(texts)} textos."
            )

        return ids, vectors
    except IndexingError:
        raise
    except Exception as e:
        raise IndexingError(f"Falha ao gerar embeddings: {e}") from e


def create_faiss_index(vectors: List[List[float]]):
    """
    Cria um índice FAISS a partir dos vetores.

    Args:
        vectors: Lista de embeddings

    Returns:
        Índice FAISS

    Raises:
        IndexingError: Se FAISS não estiver instalado ou falhar ao criar índice
    """
    if faiss is None:
        raise IndexingError("FAISS não está instalado. Instale com: pip install faiss-cpu")

    if not vectors:
        raise IndexingError("Lista de vetores está vazia.")

    try:
        arr = np.array(vectors, dtype="float32")
        dim = arr.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(arr)
        return index
    except Exception as e:
        raise IndexingError(f"Falha ao criar índice FAISS: {e}") from e


def save_index(index, index_path: str) -> str:
    """
    Salva o índice FAISS em disco.

    Args:
        index: Índice FAISS
        index_path: Caminho para salvar o índice

    Returns:
        Caminho do arquivo salvo

    Raises:
        IndexingError: Se falhar ao salvar
    """
    if faiss is None:
        raise IndexingError("FAISS não está instalado. Instale com: pip install faiss-cpu")

    try:
        p = Path(index_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(index, str(p))
        return str(p)
    except Exception as e:
        raise IndexingError(f"Falha ao salvar índice em {index_path}: {e}") from e


def save_metadata(ids: List[str], artigos: List[Dict], meta_path: str) -> str:
    """
    Salva metadados dos artigos (IDs e conteúdos) em JSON.

    Args:
        ids: Lista de IDs dos artigos
        artigos: Lista de artigos completos
        meta_path: Caminho para salvar metadados

    Returns:
        Caminho do arquivo salvo

    Raises:
        IndexingError: Se falhar ao salvar
    """
    try:
        p = Path(meta_path)
        p.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "ids": ids,
            "artigos": artigos,
        }
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(p)
    except Exception as e:
        raise IndexingError(f"Falha ao salvar metadados em {meta_path}: {e}") from e


def indexar_normas(
    artigos_jsonl_path: str,
    embedding_fn: EmbeddingFn | None = None,
    index_path: str = "vector_store/normas.index",
    metadata_path: str = "vector_store/normas_metadata.json",
) -> Tuple[str, str]:
    """
    Pipeline completo de indexação: carrega artigos → gera embeddings → cria índice → salva.

    IMPORTANTE: Por padrão, usa embeddings REAIS (não dummy).
    Se embedding_fn=None, usa EmbeddingManager configurado globalmente.

    Args:
        artigos_jsonl_path: Caminho do arquivo JSONL com artigos
        embedding_fn: Função de embedding customizada (opcional).
                      Se None, usa embeddings reais via EmbeddingManager.
        index_path: Caminho para salvar o índice FAISS
        metadata_path: Caminho para salvar metadados

    Returns:
        Tupla (index_path, metadata_path) dos arquivos salvos

    Raises:
        FileNotFoundError: Se arquivo de entrada não existir
        IndexingError: Se falhar em qualquer etapa
    """
    # Se nenhuma função de embedding for fornecida, usa embeddings reais
    if embedding_fn is None:
        embedding_manager = get_embedding_function()
        embedding_fn = embedding_manager  # EmbeddingManager é callable

    artigos = load_artigos_from_jsonl(artigos_jsonl_path)
    ids, vectors = build_embeddings(artigos, embedding_fn)
    index = create_faiss_index(vectors)
    idx_path = save_index(index, index_path)
    meta_path = save_metadata(ids, artigos, metadata_path)
    return idx_path, meta_path
