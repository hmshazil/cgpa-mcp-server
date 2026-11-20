import os
import sys
from fastmcp import FastMCP
# Ensure server/ folder is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
mcp = FastMCP("cgpa")

import tools

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)