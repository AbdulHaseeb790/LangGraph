from langgraph.graph import StateGraph, END
from typing import TypedDict
import random

class State(TypedDict):
    number: int

def generate_number(state: State):
    num = random.randint(1, 6)
    print(f"Generated: {num}")
    return {"number": num}

def check_number(state: State):
    return state

def router(state: State):
    if state["number"] > 3:
        return END
    else:
        return "generate_number"

graph = StateGraph(State)

graph.add_node("generate_number", generate_number)
graph.add_node("check_number", check_number)

graph.set_entry_point("generate_number")
graph.add_edge("generate_number", "check_number")
graph.add_conditional_edges("check_number", router)

app = graph.compile()

result = app.invoke({"number": 0})
print(f"Final number: {result['number']}")