from langgraph.graph import StateGraph, START, END
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

load_dotenv(dotenv_path='D:\proposal_agent\.env')

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatGroq(model="llama-3.3-70b-versatile")
store = InMemoryStore()
checkpointer = MemorySaver()

def load_memory(state: State, config: RunnableConfig, *, store: BaseStore):
    namespace = ("user_facts", "haseeb")
    memories = store.search(namespace)
    
    if memories:
        user_fact = memories[0].value["data"]
    else:
        user_fact = "No information about this user yet."
    
    system_msg = SystemMessage(content=f"You are a helpful assistant.\nKnown facts about this user: {user_fact}")
    return {"messages": [system_msg]}

def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def save_memory(state: State, config: RunnableConfig, *, store: BaseStore):
    namespace = ("user_facts", "haseeb")
    conversation = "\n".join([m.content for m in state["messages"]])
    
    extract_prompt = f"""Based on this conversation, extract important facts about the user worth remembering for future sessions. Be concise.

Conversation:
{conversation}"""
    
    facts = llm.invoke([HumanMessage(content=extract_prompt)])
    store.put(namespace, "memory", {"data": facts.content})
    return {}

graph_builder = StateGraph(State)
graph_builder.add_node("load_memory", load_memory)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("save_memory", save_memory)

graph_builder.add_edge(START, "load_memory")
graph_builder.add_edge("load_memory", "chatbot")
graph_builder.add_edge("chatbot", "save_memory")
graph_builder.add_edge("save_memory", END)

graph = graph_builder.compile(checkpointer=checkpointer, store=store)

config = {"configurable": {"thread_id": "session_1"}}

while True:
    user_input = input("You: ")
    if user_input == "quit":
        break
    
    result = graph.invoke({"messages": [HumanMessage(content=user_input)]}, config)
    print("AI:", result["messages"][-1].content)