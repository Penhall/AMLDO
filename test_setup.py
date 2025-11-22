# test_setup.py
import sys
print(f"Python: {sys.version}")

# Test imports
try:
    import langchain
    print("✅ LangChain instalado")
except ImportError:
    print("❌ LangChain não encontrado")

try:
    import faiss
    print("✅ FAISS instalado")
except ImportError:
    print("❌ FAISS não encontrado")

try:
    from sentence_transformers import SentenceTransformer
    print("✅ Sentence Transformers instalado")
except ImportError:
    print("❌ Sentence Transformers não encontrado")

try:
    import google.adk
    print("✅ Google ADK instalado")
except ImportError:
    print("❌ Google ADK não encontrado")

# Test environment
import os
from dotenv import load_dotenv
load_dotenv()

if os.getenv("GOOGLE_API_KEY"):
    print("✅ GOOGLE_API_KEY configurada")
else:
    print("❌ GOOGLE_API_KEY não encontrada no .env")

# Test data
import os
if os.path.exists("data/vector_db/v1_faiss_vector_db"):
    print("✅ Banco vetorial encontrado")
else:
    print("⚠️ Banco vetorial não encontrado (rode os notebooks)")

print("\n🎉 Setup completo!")
