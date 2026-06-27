from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import TypedDict
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=r'C:\Users\SOHAIL\phase7-llm-apis\.env')
class State(TypedDict):
    user_message: str
    ai_reply: str
llm = ChatGroq(model="llama-3.3-70b-versatile")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
loader=TextLoader(r"C:\Users\SOHAIL\phase7-llm-apis\lang_chain\Data\sample.txt")
docs=loader.load()
splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
chunks=splitter.split_documents(docs)

vector_store=FAISS.from_documents(chunks,embeddings)
retriever=vector_store.as_retriever()
def rag_node(state: State):
    retrieved_docs = retriever.invoke(state["user_message"])
    context = "\n".join([doc.page_content for doc in retrieved_docs])
    prompt = f"Answer this question using the context below:\n\nContext: {context}\n\nQuestion: {state['user_message']}"
    response = llm.invoke(prompt)
    return {"ai_reply": response.content}
graph = StateGraph(State)
graph.add_node("rag_node", rag_node)
graph.add_edge(START, "rag_node")
graph.add_edge("rag_node", END)
app = graph.compile()
user_input=input("you:")
result=app.invoke({"user_message": user_input})
print(result["ai_reply"])