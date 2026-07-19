from typing import TypedDict
from langgraph.graph import StateGraph, END

class State(TypedDict):
    number: float
    result: str
def divide_node(state:State):
    state['number']=state['number']/2
    return state
def should_continue(state:State):
    if state['number']>1:
        return 'continue'
    else:
        return 'stop'
graph = StateGraph(State)
graph.add_node('divide',divide_node)
graph.set_entry_point('divide')
graph.add_conditional_edges(
    'divide',
    should_continue,
    {
        'continue':'divide',
        'stop':END
    

    }
    
)
app=graph.compile()
result=app.invoke({'number':10,'result':''})
print(result['result'])