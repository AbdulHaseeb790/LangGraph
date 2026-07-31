from langchain_mcp_adapters.client import MultiServerMCPClient  # MCP Client to connect to our server
from langgraph.prebuilt import create_react_agent  # builds ReAct agent
from langchain_groq import ChatGroq  # our LLM
from dotenv import load_dotenv  # load API keys
import asyncio  # needed to run async functions

load_dotenv(dotenv_path=r'D:\proposal_agent\.env')  # load .env file

llm = ChatGroq(model='llama-3.3-70b-versatile')  # initialize the LLM

async def main():
    client = MultiServerMCPClient(
        {
            "math": {  # name we give our server
                "command": "python",  # run our server using python (not npx like Tavily)
                "args": [r"D:\proposal_agent\langgraph\math_server.py"],  # path to our server file
                "transport": "stdio",  # same transport our server uses
            }
        }
    )

    tools = await client.get_tools()  # discover tools from our math server (add, multiply)

    agent = create_react_agent(llm, tools)  # create agent with our custom tools

    result = await agent.ainvoke({"messages": "what is 5 plus 3?"})  # ask a math question

    print(result['messages'][-1].content)  # print the agent's final answer

asyncio.run(main())  # run the async main function