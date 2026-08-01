from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import asyncio

load_dotenv(dotenv_path='D:\proposal_agent\.env')

async def main():
    client = MultiServerMCPClient({
        'math': {
            'command': 'python',
            'args': [r'D:\proposal_agent\langgraph\math_Ser.py'],
            'transport': 'stdio'
        },
        'text': {
            'command': 'python',
            'args': [r'D:\proposal_agent\langgraph\text_server.py'],
            'transport': 'stdio'
        }
    })
    tools = await client.get_tools()
    llm = ChatGroq(model='llama-3.1-8b-instant')
    agent = create_react_agent(llm, tools)
    result = await agent.ainvoke({'messages': 'use the add tool to add 5 and 3. use the reverse_string tool to reverse the word hello'})
    print(result['messages'][-1].content)

asyncio.run(main())