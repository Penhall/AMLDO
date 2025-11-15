
\"\"\"Módulo de indexação vetorial (FAISS) para normas estruturadas.\"\"\"

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Dict, List, Tuple

try:
    import faiss  # type: ignore
except ImportError:  # pragma: no cover
    faiss = None  # type: ignore


EmbeddingFn = Callable[[List[str]], List[List[float]]]


def load_artigos_from_jsonl(path: str) -> List[Dict]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Arquivo JSONL de artigos não encontrado: {p}")

    artigos: List[Dict] = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            artigos.append(json.loads(line))
    return artigos


def build_embeddings(
    artigos: List[Dict],
    embedding_fn: EmbeddingFn,
) -> Tuple[List[str], List[List[float]]]:
    texts = [a.get("text", "") for a in artigos]
    ids = [a.get("id", "") for a in artigos]

    vectors = embedding_fn(texts)
    if len(vectors) != len(texts):
        raise ValueError("embedding_fn deve retornar um vetor por texto.")

    return ids, vectors


def create_faiss_index(vectors: List[List[float]]):
    if faiss is None:
        raise ImportError(
            "FAISS não está instalado. Instale com: pip install faiss-cpu"
        )

    if not vectors:
        raise ValueError("Lista de vetores está vazia.")

    import numpy as np  # type: ignore

    arr = np.array(vectors, dtype="float32")
    dim = arr.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(arr)
    return index


def save_index(index, index_path: str) -> str:
    if faiss is None:
        raise ImportError(
            "FAISS não está instalado. Instale com: pip install faiss-cpu"
        )

    p = Path(index_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(p))
    return str(p)


def save_metadata(ids: List[str], artigos: List[Dict], meta_path: str) -> str:
    p = Path(meta_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "ids": ids,
        "artigos": artigos,
    }
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(p)


def indexar_normas(
    artigos_jsonl_path: str,
    embedding_fn: EmbeddingFn,
    index_path: str = "vector_store/normas.index",
    metadata_path: str = "vector_store/normas_metadata.json",
) -> Tuple[str, str]:
    artigos = load_artigos_from_jsonl(artigos_jsonl_path)
    ids, vectors = build_embeddings(artigos, embedding_fn)
    index = create_faiss_index(vectors)
    idx_path = save_index(index, index_path)
    meta_path = save_metadata(ids, artigos, metadata_path)
    return idx_path, meta_path
