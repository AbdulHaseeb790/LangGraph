from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage,AIMessage
from langchain_groq import ChatGroq
from typing import TypedDict,Annotated
import operator
from dotenv import load_dotenv
load_dotenv(dotenv_path='D:\proposal_agent\.env')

class State(TypedDict):
    messages:Annotated[list,operator.add]
llm=ChatGroq(model='llama-3.3-70b-versatile')
def chat_node(state:State):
    response=llm.invoke(state['messages'])
    return{'messages':[AIMessage(content=response.content)]}
checkpointer = SqliteSaver.from_conn_string("memory.db")
build_graph=StateGraph(State)
build_graph.add_node('chat',chat_node)
build_graph.add_edge(START,'chat')
build_graph.add_edge('chat',END)
graph=build_graph.compile(checkpointer=checkpointer)
config={'configurable':{"thread_id":"2"}}
while True:
    user_input=input('you:')
    if user_input=='quit':
        break
    result=graph.invoke({"messages":[HumanMessage(content=user_input)]},config)
    print("AI:", result["messages"][-1].content)


