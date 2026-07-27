from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpointEmbeddings 
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = HuggingFaceEndpointEmbeddings(
    model = "BAAI/bge-small-en-v1.5",
    huggingfacehub_api_token=os.getenv("HF_TOKEN")
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
VECTOR_DB_PATH = BASE_DIR / "vector_db"

vector_db = FAISS.load_local(
    str(VECTOR_DB_PATH),
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vector_db.as_retriever(
    search_kwargs = {'k':2}
)