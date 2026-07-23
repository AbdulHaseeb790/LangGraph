from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from typing import TypedDict, Annotated
import operator
from dotenv import load_dotenv
load_dotenv(dotenv_path='D:\proposal_agent\.env')
class State(TypedDict):
    messages:Annotated[list,operator.add]
@tool
def add_number(a:int,b:int)-> int:
    """add two numbers together"""
    return a+b
def multiply_number(a:int,b:int)-> int:
    """multiply two numbers"""
    return a*b
tools=[add_number,multiply_number]
llm=ChatGroq(model='llama-3.3-70b-versatile')
llm_with_tools=llm.bind_tools(tools)
def chat_node(state:State):
    response=llm_with_tools.invoke(state['messages'])
    return{'messages':[response]}
check_pointer=MemorySaver()
graph_builder=StateGraph(State)
graph_builder.add_node('chat',chat_node)
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_edge(START,'chat')
graph_builder.add_conditional_edges('chat',tools_condition)
graph_builder.add_edge("tools", "chat")
graph = graph_builder.compile(check_pointer=check_pointer)
config={"configurable":{"thread_id":1}}
while True:
    user_input=input("you:")
    if user_input=='quit':
        break
    result=graph.invoke({"messages":HumanMessage(content=user_input)},config)
    print("AI",result['messages'][-1].content)

