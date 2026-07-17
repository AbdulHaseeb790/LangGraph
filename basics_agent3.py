from typing import TypedDict
from langgraph.graph import StateGraph
class State(TypedDict):
    name:str
    age:int
    skills:list[str]
    final_out:str
def first_node(state:State):
    state['final_out']=f"{state['name']} welcome to the system"
    return state
def second_node(state:State):
    state['final_out']=state['final_out']+f" you are {state['age']} years old"
    return state
def third_node(state:State):
    state['final_out']=state['final_out']+f" you have skills in {','.join(state['skills'])}"
    return state
graph=StateGraph(State)
graph.add_node('personalize',first_node)
graph.add_node('age_description',second_node)
graph.add_node('skills_description',third_node)
graph.set_entry_point('personalize')
graph.add_edge('personalize','age_description')
graph.add_edge("age_description", "skills_description")
graph.set_finish_point('skills_description')
app=graph.compile()
result=app.invoke({'name':'Haseeb','age':20,'skills':['python','langgraph','langchain'],'final_out':''})
print(result['final_out'])




    