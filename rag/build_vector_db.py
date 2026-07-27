from pathlib import Path
import os 
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.vectorstores import FAISS


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"

documents = []
for pdf_file in KNOWLEDGE_BASE.glob("*.pdf"):
    loader = PyPDFLoader(str(pdf_file))
    documents.extend(loader.load())

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

chunks = text_splitter.split_documents(documents)

print(f"pages loaded {len(documents)}")
print(f'chunks created {len(chunks)}')

load_dotenv()
embeddings = HuggingFaceEndpointEmbeddings(
    model = "BAAI/bge-small-en-v1.5",
    huggingfacehub_api_token = os.getenv('HF_TOKEN')
)


vector_db = FAISS.from_documents(
    documents = chunks , 
    embedding = embeddings
)

vector_db.save_local('vector_db')
