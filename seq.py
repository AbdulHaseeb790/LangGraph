from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv(dotenv_path='D:\proposal_agent\.env')
llm=ChatGroq(model='llama-3.3-70b-versatile')
class State(TypedDict):
    topic:str
    title:str
    description:str
    fun_fact:str
def node_one(state:State):
    topic=state['topic']
    response=llm.invoke(f"generate a short catchy title about{topic}")
    return{'title':response.content}
def node_two(state:State):
    title=state['title']
    respone=llm.invoke(f"write a one line description about {title}")
    return{"description":respone.content}
def node_three(state:State):
    description=state['description']
    respone=llm.invoke(f"write a fun fact about this {description}")
    return{'fun_fact':respone.content}
graph=StateGraph(State)
graph.add_node('node_one',node_one)
graph.add_node('node_two',node_two)
graph.add_node('node_three',node_three)
graph.set_entry_point('node_one')
graph.add_edge('node_one','node_two')
graph.add_edge('node_two','node_three')
graph.add_edge('node_three',END)
app=graph.compile()
result=app.invoke({
    'topic':'Ai agents',
    'title':'',
    'description':'',
    'fun_fact':''

})
print('title',result['title'])
print('descpritn',result['description'])
print('fun_fact',result['fun_fact'])