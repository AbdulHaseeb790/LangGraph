from fastmcp import FastMCP
mcp=FastMCP("text server")
@mcp.tool()
def reverse_string(text:str)->str:
    """reverse the string"""
    return text[::-1]
@mcp.tool()
def word_count(text:str)->int:
    """count the words in string"""
    return len(text.split())
if __name__ == "__main__":
    mcp.run()