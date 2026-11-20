import os
import sys
import inspect
from fastmcp import FastMCP

# Ensure server/ folder is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tools

mcp = FastMCP("cgpa")

# Automatically register every function defined in tools.py
for name, func in inspect.getmembers(tools, inspect.isfunction):
    if func.__module__ == tools.__name__ and not name.startswith("_"):
        mcp.tool(func)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)