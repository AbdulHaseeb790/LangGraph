from langgraph.graph import StateGraph,END,START
from langchain_groq import ChatGroq
from typing import TypedDict
from dotenv import load_dotenv
load_dotenv(dotenv_path='D:\proposal_agent\.env')
class State(TypedDict):
    topic:str
    fact_one:str
    fact_two:str
    final_output:str
llm=ChatGroq(model='llama-3.3-70b-versatile')
def research_one(state:State):
    topic=state['topic']
    respone=llm.invoke(f'write a intersting fact about{topic}')
    return {"fact_one":respone.content}
def research_two(state:State):
    topic=state['topic']
    respone=llm.invoke(f'write a static fact about{topic}')
    return{'fact_two':respone.content}
def combine(state:State):
    fact_one=state['fact_one']
    fact_two=state['fact_two']
    respone=llm.invoke(f'combine these two facts into paragraph{fact_one} and {fact_two}')
    return{'final_output':respone.content}
graph=StateGraph(State)
graph.add_node("research_one", research_one)
graph.add_node("research_two", research_two)
graph.add_node("combine", combine)
graph.add_edge(START,'research_one')
graph.add_edge(START,'research_two')
graph.add_edge('research_one','combine')
graph.add_edge('research_two','combine')
graph.add_edge('combine',END)
app=graph.compile()
result=app.invoke({
    'topic':'AI agents',
    'fact_one':'',
    'fact_two':'',
    'final_output':""

})
print(result['final_output'])

