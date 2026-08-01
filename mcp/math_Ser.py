from fastmcp import FastMCP
mcp=FastMCP('math server')
@mcp.tool()
def add(a:int,b:int)->int:
    """add two numbers"""
    return a+b
@mcp.tool()
def multiply(a:int,b:int)->int:
    """multiply two numbers"""
    return a*b
if __name__ == "__main__":
    mcp.run()