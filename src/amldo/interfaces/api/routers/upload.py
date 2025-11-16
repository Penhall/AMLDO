"""
Router para upload e processamento de documentos.

Endpoints para fazer upload de PDFs e processar documentos para indexação no FAISS.
"""

import time
from pathlib import Path
from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from amldo.interfaces.api.models.response import UploadResponse, ProcessResponse
from amldo.interfaces.api.dependencies import SettingsDep
from amldo.core.exceptions import VectorStoreError
from amldo.utils.metrics import track_processing_metrics
import json

# Importar pipeline de processamento
import fitz  # PyMuPDF
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

router = APIRouter()


@router.post("/upload", response_model=UploadResponse, summary="Upload de PDFs")
async def upload_documents(files: List[UploadFile] = File(...), settings: SettingsDep = None):
    """
    Faz upload de múltiplos arquivos PDF para o sistema.

    Os arquivos são salvos em `data/raw/` e ficam disponíveis para processamento.

    **Parâmetros:**
    - files: Lista de arquivos PDF (multipart/form-data)

    **Comportamento:**
    - Apenas arquivos .pdf são aceitos
    - Se um arquivo com o mesmo nome já existir, adiciona sufixo numérico (_1, _2, etc.)
    - Arquivos inválidos são listados em 'failed' com motivo do erro

    **Exemplo de uso:**
    ```bash
    curl -X POST "http://localhost:8000/api/upload" \\
      -F "files=@lei_14133.pdf" \\
      -F "files=@decreto_10024.pdf"
    ```

    **Retorna:**
    - saved: Lista de nomes de arquivos salvos com sucesso
    - failed: Lista de arquivos que falharam (com motivo)
    """
    saved = []
    failed = []

    upload_dir = Path("data/raw")
    upload_dir.mkdir(parents=True, exist_ok=True)

    for file in files:
        filename = file.filename or "unnamed.pdf"

        # Validar tipo de arquivo
        if not filename.lower().endswith(".pdf"):
            failed.append({"file": filename, "error": "Tipo inválido - apenas PDF aceito"})
            continue

        # Evitar sobrescrever arquivos existentes
        dest = upload_dir / filename
        counter = 1
        while dest.exists():
            stem = dest.stem
            dest = upload_dir / f"{stem}_{counter}.pdf"
            counter += 1

        try:
            content = await file.read()
            dest.write_bytes(content)
            saved.append(dest.name)
        except Exception as e:
            failed.append({"file": filename, "error": f"Erro ao salvar: {str(e)}"})

    return UploadResponse(saved=saved, failed=failed)


@router.post("/process", response_model=ProcessResponse, summary="Processar PDFs")
async def process_documents(settings: SettingsDep = None):
    """
    Processa todos os PDFs em `data/raw/` e atualiza o índice FAISS.

    **Workflow:**
    1. Lê todos os arquivos .pdf em data/raw/
    2. Extrai texto de cada página usando PyMuPDF
    3. Divide texto em chunks usando RecursiveCharacterTextSplitter
    4. Cria embeddings com sentence-transformers
    5. Adiciona chunks ao índice FAISS existente
    6. Salva índice atualizado

    **Parâmetros:**
    - Nenhum (processa todos os PDFs em data/raw/)

    **Exemplo de uso:**
    ```bash
    curl -X POST "http://localhost:8000/api/process"
    ```

    **Retorna:**
    - processed: Número de arquivos processados
    - total_chunks: Total de chunks criados neste processamento
    - files: Lista de arquivos processados com número de chunks
    - duration_seconds: Tempo de processamento

    **Notas:**
    - Este endpoint pode demorar vários minutos para PDFs grandes
    - O índice FAISS é atualizado incrementalmente (não sobrescreve)
    - Arquivos que falham são ignorados silenciosamente
    """
    start_time = time.time()

    upload_dir = Path("data/raw")
    pdf_files = list(upload_dir.glob("*.pdf"))

    if not pdf_files:
        raise HTTPException(status_code=404, detail="Nenhum arquivo PDF encontrado em data/raw/")

    # Configurar splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, length_function=len
    )

    # Processar cada PDF
    new_documents = []
    files_info = []

    for pdf_path in pdf_files:
        try:
            # Extrair texto com PyMuPDF
            doc = fitz.open(str(pdf_path))
            pages_text = []

            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                pages_text.append(page.get_text("text"))

            full_text = "\n".join(pages_text)
            doc.close()

            # Dividir em chunks
            chunks = splitter.split_text(full_text)

            # Criar documentos LangChain
            for idx, chunk in enumerate(chunks):
                new_documents.append(
                    Document(
                        page_content=chunk,
                        metadata={"path": str(pdf_path), "file": pdf_path.name, "chunk_idx": idx},
                    )
                )

            files_info.append({"file": pdf_path.name, "chunks": len(chunks)})

        except Exception as e:
            # Ignorar arquivos com erro
            files_info.append({"file": pdf_path.name, "chunks": 0, "error": str(e)})
            continue

    if not new_documents:
        raise HTTPException(
            status_code=500, detail="Falha ao processar todos os PDFs - nenhum chunk criado"
        )

    # Carregar ou criar índice FAISS
    vector_db_path = Path("data/vector_db/v1_faiss_vector_db")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        encode_kwargs={"normalize_embeddings": True},
    )

    try:
        if vector_db_path.exists():
            # Carregar índice existente
            vector_db = FAISS.load_local(
                str(vector_db_path), embeddings=embeddings, allow_dangerous_deserialization=True
            )
            # Adicionar novos documentos
            vector_db.add_documents(new_documents)
        else:
            # Criar novo índice
            vector_db = FAISS.from_documents(new_documents, embeddings)

        # Salvar índice atualizado
        vector_db.save_local(str(vector_db_path))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar índice FAISS: {str(e)}")

    duration_seconds = time.time() - start_time

    # Registrar métricas
    successful_files = len([f for f in files_info if f.get("chunks", 0) > 0])
    track_processing_metrics(
        files=successful_files,
        chunks=len(new_documents),
        duration=duration_seconds,
        details=json.dumps(files_info),
    )

    return ProcessResponse(
        processed=successful_files,
        total_chunks=len(new_documents),
        files=files_info,
        duration_seconds=round(duration_seconds, 2),
    )
