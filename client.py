from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

async def main():
    client = MultiServerMCPClient({
        "math": {
            "command": "python",
            "args": ["mathserver.py"],
            "transport": "stdio"
        }
    })

    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools = await client.get_tools()

    # Extract tool names (strings) for the request

    model = ChatGroq(model="qwen/qwen3-32b", tools=tools)

    agent = create_react_agent(model, tools)

    math_response = await agent.ainvoke({"messages":[{"role": "user", "content": "What is 2 + 3 * 5?"}]})
    print("math response:",math_response["messages"][-1].content)
asyncio.run(main())
