from langgraph.graph import StateGraph,END
from typing import TypedDict
class State(TypedDict):
    message:str
    mood:str
def greet(state: State):
    return {"mood": ""}
    
def check_mood(state:State):
    if 'good' in state['message'].lower():
        return{'mood':'positive'}
    else:
        return{'mood':'negative'}
def router(state:State):
    if state['mood']=='positive':
        return "happy_response"
    else:
        return "sad_response"
def happy_response(state:State):
    return{"message":'glad to hear that'}
def sad_response(state:State):
    return{'message':'sorry to hear that bro'}

graph=StateGraph(State)
graph.add_node('greet',greet)
graph.add_node('check_mood',check_mood)
graph.add_node('happy_response',happy_response)
graph.add_node('sad_response',sad_response)
graph.set_entry_point('greet')
graph.add_edge('greet','check_mood')
graph.add_conditional_edges('check_mood',router)
graph.add_edge("happy_response", END)
graph.add_edge("sad_response", END)
app=graph.compile()
result=app.invoke({'message':'iam feeling bad today!','mood':""})
print(result['message'])
