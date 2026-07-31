import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r'D:\proposal_agent\.env')

llm = ChatGroq(model='llama-3.3-70b-versatile')

async def main():
    client = MultiServerMCPClient(
        {
            "tavily": {
                "command": "npx",
                "args": ["-y", "tavily-mcp@0.1.2"],
                "env": {"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")},
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    result = await agent.ainvoke({"messages": "What is MCP protocol?"})
    print(result['messages'][-1].content)

asyncio.run(main())