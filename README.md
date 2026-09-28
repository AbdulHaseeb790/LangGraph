# LangGraph

A collection of hands-on [LangGraph](https://langchain-ai.github.io/langgraph/) examples, built step by step from core graph concepts up to agents, memory, RAG, and MCP integration.

## Learning Path

Scripts are listed roughly in the order I learned them.

### Core Graph Concepts

| File | What it demonstrates |
| --- | --- |
| `basics.py` | Graph fundamentals: state, nodes, and edges |
| `seq.py` | Sequential workflows (node → node → node) |
| `llm_node.py` | Calling an LLM inside a graph node |
| `parallel.py` | Running nodes in parallel and merging results |
| `conditional_edges.py` | Routing the flow based on state |
| `loops.py` | Loops and cycles in a graph |
| `iterative_workflow.py` | Iterative workflows that refine output over multiple passes |

### Agents and Tools

| File | What it demonstrates |
| --- | --- |
| `tools_agent.py` | An agent that calls external tools |
| `agent2.py` | Agent example |
| `basics_agent3.py` | Agent example |

### Memory and RAG

| File | What it demonstrates |
| --- | --- |
| `memory_chatbot.py` | Chatbot with conversation memory |
| `longterm_memory.py` | Long-term memory that persists across conversations |
| `rag_graph.py` | Retrieval-Augmented Generation as a graph |

### Integrations

| Folder | What it contains |
| --- | --- |
| `mcp/` | Model Context Protocol (MCP) examples |

## Tech Stack

- Python
- LangGraph
- LangChain
- LLM provider API keys via `.env`

## Getting Started

```bash
git clone https://github.com/AbdulHaseeb790/LangGraph.git   # download the repo
cd LangGraph                                                # move into the project
pip install langgraph langchain python-dotenv               # install core dependencies
```

Create a `.env` file in the project root with the API keys your chosen scripts need, then run any example:

```bash
python basics.py   # run the first example
```

## Author

**Abdul Haseeb**, Software Engineering student at MUET, building AI agents & automation
GitHub: [AbdulHaseeb790](https://github.com/AbdulHaseeb790)
