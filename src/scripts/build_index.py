#!/usr/bin/env python3
"""
Script para criar índice FAISS a partir de artigos processados.

Uso:
    python -m amldo.scripts.build_index --source data/processed/ --output data/vector_db/
    # ou via entry point:
    amldo-build-index --source data/processed/ --output data/vector_db/
"""

import argparse
import sys
from pathlib import Path

from amldo.pipeline.indexer.indexer import indexar_normas
from amldo.pipeline.embeddings import get_embedding_function
from amldo.core.exceptions import IndexingError


def main():
    parser = argparse.ArgumentParser(
        description="Cria índice FAISS a partir de artigos estruturados (JSONL)"
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Caminho para o arquivo JSONL com artigos estruturados",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="vector_store",
        help="Diretório de saída para índice e metadados (default: vector_store/)",
    )
    parser.add_argument(
        "--index-name", type=str, default="normas.index", help="Nome do arquivo de índice"
    )
    parser.add_argument(
        "--metadata-name",
        type=str,
        default="normas_metadata.json",
        help="Nome do arquivo de metadados",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Modo verbose")

    args = parser.parse_args()

    # Valida source
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"❌ Erro: Arquivo fonte não encontrado: {source_path}", file=sys.stderr)
        sys.exit(1)

    # Paths de saída
    output_dir = Path(args.output)
    index_path = output_dir / args.index_name
    metadata_path = output_dir / args.metadata_name

    if args.verbose:
        print(f"Source: {source_path}")
        print(f"Output dir: {output_dir}")
        print(f"Index path: {index_path}")
        print(f"Metadata path: {metadata_path}")
        print()

    try:
        print("🔧 Inicializando embedding function...")
        embedding_fn = get_embedding_function()

        if args.verbose:
            print(f"Embedding model: {embedding_fn.model_name}")
            print(f"Dimension: {embedding_fn.dimension}")
            print()

        print("📚 Carregando artigos e gerando embeddings...")
        idx_path, meta_path = indexar_normas(
            artigos_jsonl_path=str(source_path),
            embedding_fn=embedding_fn,
            index_path=str(index_path),
            metadata_path=str(metadata_path),
        )

        print()
        print("✅ Índice criado com sucesso!")
        print(f"   Índice: {idx_path}")
        print(f"   Metadados: {meta_path}")

    except IndexingError as e:
        print(f"❌ Erro na indexação: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
