
\"\"\"Camada RAG (Retrieval-Augmented Generation) simplificada.\"\"\"

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

try:
    import faiss  # type: ignore
except ImportError:  # pragma: no cover
    faiss = None  # type: ignore


def load_index(index_path: str):
    if faiss is None:
        raise ImportError(
            "FAISS não está instalado. Instale com: pip install faiss-cpu"
        )

    p = Path(index_path)
    if not p.exists():
        raise FileNotFoundError(f"Índice FAISS não encontrado: {p}")
    return faiss.read_index(str(p))


def load_metadata(metadata_path: str) -> Dict[str, Any]:
    p = Path(metadata_path)
    if not p.exists():
        raise FileNotFoundError(f"Arquivo de metadados não encontrado: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def search_normas(
    query: str,
    embedding_fn,
    index_path: str = "vector_store/normas.index",
    metadata_path: str = "vector_store/normas_metadata.json",
    k: int = 5,
) -> List[Dict]:
    import numpy as np  # type: ignore

    index = load_index(index_path)
    meta = load_metadata(metadata_path)

    ids: List[str] = meta.get("ids", [])
    artigos: List[Dict] = meta.get("artigos", [])

    if not ids or not artigos:
        return []

    query_vec = embedding_fn([query])[0]
    q = np.array([query_vec], dtype="float32")
    distances, indices = index.search(q, k)

    results: List[Dict] = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0 or idx >= len(ids):
            continue
        artigo = artigos[idx]
        results.append(
            {
                "score": float(dist),
                "id": artigo.get("id"),
                "label": artigo.get("label"),
                "text": artigo.get("text"),
            }
        )

    return results
