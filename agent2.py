from typing import TypedDict
from langgraph.graph import StateGraph
import math
class State(TypedDict):
    name: str
    values: list[int]
    operation: str
    output: str
def operation(state:State):
    if state['operation']=='+':
        state['output']=f"hi {state['name']},your answer is {sum(state['values'])}"
    elif state['operation']=='*':
        state['output']=f"hi {state['name']},your answer is {math.prod(state['values'])}"
    return state
graph=StateGraph(State)
graph.add_node('opr',operation)
graph.set_entry_point('opr')
graph.set_finish_point('opr')
app=graph.compile()
result=app.invoke({"name":'haseeb','values':[10,20,30],'operation':"+",'output':''})
print(result['output'])

