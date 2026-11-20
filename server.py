import os
from fastmcp import FastMCP

mcp = FastMCP("cgpa")

import tools

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)