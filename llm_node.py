from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from typing import TypedDict
from dotenv import load_dotenv
load_dotenv(dotenv_path=r'C:\Users\SOHAIL\phase7-llm-apis\.env')
class State(TypedDict):
    user_message:str
    ai_reply:str
llm=ChatGroq(model='llama-3.3-70b-versatile')
def llm_node(state: State):
    response = llm.invoke(state["user_message"])
    return {"ai_reply": response.content}
graph = StateGraph(State)
graph.add_node("llm_node", llm_node)
graph.add_edge(START, "llm_node")
graph.add_edge("llm_node", END)
app = graph.compile()
user_input=input("you:")
result=app.invoke({"user_message":user_input})
print(result['ai_reply'])