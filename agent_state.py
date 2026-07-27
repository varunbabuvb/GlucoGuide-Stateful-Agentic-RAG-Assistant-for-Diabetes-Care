from typing import TypedDict,Annotated
import operator 
from langchain_core.messages import AnyMessage,SystemMessage,ToolMessage
class AgentState(TypedDict):
    messages : Annotated[list[AnyMessage],operator.add]