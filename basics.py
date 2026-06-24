from langgraph.graph import StateGraph,END
from typing import TypedDict
class State(TypedDict):
    message:'str'
def greet(state:State):
    return{"message":"hello"}
def respond(state:State):
    return{'message':state['message']+'how are you?'}
graph = StateGraph(State)

graph.add_node("greet", greet)
graph.add_node("respond", respond)

graph.set_entry_point("greet")
graph.add_edge("greet", "respond")
graph.add_edge("respond", END)

app = graph.compile()
result = app.invoke({"message": ""})
print(result["message"])