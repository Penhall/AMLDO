#!/usr/bin/env python3
"""
Script para processar documentos: ingestão → estruturação.

Uso:
    python -m amldo.scripts.process_documents --input data/raw/lei.pdf --output data/processed/
    # ou via entry point:
    amldo-process --input data/raw/lei.pdf --output data/processed/
"""

import argparse
import sys
from pathlib import Path

from amldo.pipeline.ingestion.ingest import ingest_norma, read_norma_file
from amldo.pipeline.structure.structure import estrutura_norma
from amldo.core.exceptions import IngestionError, StructureError


def main():
    parser = argparse.ArgumentParser(
        description="Processa documento: ingestão (PDF/TXT) → estruturação (artigos JSONL)"
    )
    parser.add_argument(
        "--input", "-i", type=str, required=True, help="Caminho para o documento de entrada (PDF/TXT)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="data/processed",
        help="Diretório de saída (default: data/processed/)",
    )
    parser.add_argument(
        "--name", "-n", type=str, default=None, help="Nome base para arquivos de saída (opcional)"
    )
    parser.add_argument(
        "--skip-structure",
        action="store_true",
        help="Pula estruturação, só faz ingestão",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Modo verbose")

    args = parser.parse_args()

    # Valida input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Erro: Arquivo de entrada não encontrado: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Diretórios de saída
    output_dir = Path(args.output)
    raw_dir = output_dir / "raw"
    structured_dir = output_dir / "structured"

    # Nome base
    name = args.name or input_path.stem

    if args.verbose:
        print(f"Input: {input_path}")
        print(f"Output dir: {output_dir}")
        print(f"Name: {name}")
        print()

    try:
        # ETAPA 1: Ingestão
        print("📄 Etapa 1/2: Ingestão...")
        if args.verbose:
            print(f"   Lendo {input_path.suffix} file...")

        raw_txt_path = ingest_norma(
            input_path=str(input_path), output_dir=str(raw_dir), output_name=name
        )

        print(f"   ✅ Texto bruto salvo: {raw_txt_path}")

        if args.skip_structure:
            print("\n⏭️  Estruturação ignorada (--skip-structure)")
            print(f"\n✅ Processamento concluído!")
            print(f"   Output: {raw_txt_path}")
            return

        # ETAPA 2: Estruturação
        print("\n📋 Etapa 2/2: Estruturação em artigos...")

        structured_path = structured_dir / f"{name}_artigos.jsonl"

        if args.verbose:
            print(f"   Dividindo texto em artigos...")
            print(f"   Output: {structured_path}")

        final_path = estrutura_norma(
            raw_txt_path=raw_txt_path, output_jsonl_path=str(structured_path)
        )

        # Contagem de artigos
        with open(final_path, "r", encoding="utf-8") as f:
            count = sum(1 for line in f if line.strip())

        print(f"   ✅ {count} artigos extraídos")
        print(f"   ✅ JSONL salvo: {final_path}")

        print(f"\n✅ Processamento concluído!")
        print(f"   Texto bruto: {raw_txt_path}")
        print(f"   Artigos: {final_path}")

        print(
            f"\n💡 Próximo passo: criar índice FAISS"
            f"\n   amldo-build-index --source {final_path} --output data/vector_db/"
        )

    except IngestionError as e:
        print(f"❌ Erro na ingestão: {e}", file=sys.stderr)
        sys.exit(1)
    except StructureError as e:
        print(f"❌ Erro na estruturação: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
