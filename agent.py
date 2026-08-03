import os 
from langgraph.graph import StateGraph , START ,END
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage
from dotenv import load_dotenv 
from agent_state import AgentState 
from system_prompt import system_prompt 
from Tools.bmi_tool import calculate_bmi 
from Tools.blood_sugar_tool import blood_suagr_level 
from Tools.rag_tool import rag_tool
from langgraph.checkpoint.memory import InMemorySaver 

load_dotenv() 

llm = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash',
    google_api_key = os.getenv('GOOGLE_API_KEY')
)


class Agent : 
    def __init__(self,llm,system_prompt,tools):
        self.system_prompt = system_prompt 
        graph = StateGraph(AgentState)
        self.tools = {t.name : t for t in tools}
        self.llm = llm.bind_tools(tools)
        graph.add_node('llm',self.call_llm)
        graph.add_node('take_action',self.take_action)
        graph.add_edge(START,'llm')
        graph.add_conditional_edges('llm',self.exists_action,
                                    {True:'take_action',False : END})
        graph.add_edge('take_action','llm')
        checkpointer = InMemorySaver()
        self.graph = graph.compile(checkpointer = checkpointer)
    def call_llm(self,state : AgentState)->dict:
        messages = state['messages']
        if self.system_prompt :
            messages = [SystemMessage(content = self.system_prompt)] + messages 

        message = self.llm.invoke(messages)
        return {'messages':[message]}
    def take_action(self,state : AgentState) ->dict:
        tool_calls = state['messages'][-1].tool_calls 
        results = []
        for t in tool_calls :
            print(f'Calling tool {t['name']}')
            try:
                result = self.tools[t["name"]].invoke(t["args"])
            except Exception as e:
                result = f"Tool execution failed: {str(e)}"
            print('Back to Model')
            print()
            results.append(ToolMessage(content = result,tool_call_id = t['id'],name=t['name']))
        return {'messages':results}
    
    def exists_action(self,state : AgentState)->bool :
        result = state['messages'][-1]
        return len(result.tool_calls) > 0 
    
    
    

tools = [calculate_bmi,blood_suagr_level,rag_tool]
agent = Agent(llm = llm ,system_prompt = system_prompt,tools = tools)
user_message = input('hello how may i help you ? ')
while(user_message.lower() != 'exit'):
    result = agent.graph.invoke({'messages':[HumanMessage(content = user_message)]},config = {'configurable':{'thread_id': '1'}})
    content = result['messages'][-1].content
    if isinstance(content, str):
        response = content
    else:
        response = "".join(
            block["text"]
            for block in content
            if block.get("type") == "text"
        )
    print(response)
    user_message = input('Add a follow on question : ')
print(list(agent.graph.get_state_history(config = {'configurable':{'thread_id': '1'}})))