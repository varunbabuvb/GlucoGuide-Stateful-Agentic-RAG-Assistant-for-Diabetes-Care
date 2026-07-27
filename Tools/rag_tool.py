from langchain_core.tools import tool 
from schemas.rag_schema import RAGSchema 
from rag.retriever import retriever
import time 
@tool('rag_tool',args_schema= RAGSchema)
def rag_tool(query)->dict:
    """
Search the diabetes knowledge base to answer factual questions about diabetes.

Use this tool for questions about:
- symptoms
- causes
- diagnosis
- diet
- exercise
- medications
- insulin
- complications
- prevention
- lifestyle
- diabetes management

Returns relevant information from the diabetes knowledge base.
"""
    for attempt in range(3):
        try:
            docs = retriever.invoke(query)
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    else:
        raise RuntimeError("Failed after 3 attempts")

    context = "\n\n".join(
    doc.page_content
    for doc in docs
    )

    return {
        'retieved_context' : context
    }
