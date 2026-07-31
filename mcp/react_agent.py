from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

load_dotenv(dotenv_path=r'D:\proposal_agent\.env')

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatGroq(model='llama-3.3-70b-versatile')
tool = TavilySearchResults(max_results=2)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: State):
    response = llm_with_tools.invoke(state['messages'])
    return {'messages': response}

graph_builder = StateGraph(State)
graph_builder.add_node('agent', agent_node)
graph_builder.add_node('tools', ToolNode(tools))
graph_builder.add_edge(START, 'agent')
graph_builder.add_conditional_edges("agent", tools_condition)
graph_builder.add_edge('tools', 'agent')

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)