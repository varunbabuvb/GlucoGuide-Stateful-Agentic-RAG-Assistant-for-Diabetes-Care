from pydantic import BaseModel,Field
from typing import Annotated 

class RAGSchema(BaseModel):
    query : Annotated[str,Field(description = 'this is the exact query use has sent')]