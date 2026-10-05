from fastapi import FastAPI,Query,Path
from typing import Annotated
from pydantic import BaseModel,Field
from langchain_core.messages import HumanMessage
import time 
app = FastAPI()
class Talk_Agent(BaseModel):
       message : str = Field(title = 'user message',description='message from the user',max_length=50)


from agent import agent 
@app.post('/talk-with-agent/{thread_id}')
def talk(thread_id : Annotated[str,Path(title = 'thread_id',max_length=5)], talk_agent: Talk_Agent ):
    start_time = time.time()
    result = agent.graph.invoke({'messages':[HumanMessage(content = talk_agent.message)]},config = {'configurable':{'thread_id': thread_id}})
    content = result['messages'][-1].content
    if isinstance(content, str):
            
            response = content
    else:
            
            response = "".join(
                block["text"]
                for block in content
                if block.get("type") == "text"
            )
    end_time = time.time()
    time_taken = end_time-start_time        
    return {'response':response,'time_taken':time_taken}