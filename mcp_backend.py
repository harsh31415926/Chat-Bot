from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from dotenv import load_dotenv  

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_mcp_adapters.client import MultiServerMCPClient
import requests
import asyncio
import os

# ================== ENV ==================
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


#==================MCP Server================

client = MultiServerMCPClient(
    {
        'arith':{
            'transport':'stdio',
            'command': "C:/Users/harsh/anaconda3/python.exe",
            "args": ["C:/Users/harsh/Desktop/Real_Ones/Chat_Bot/Chat-Bot/mcp.py"]
        }
    }
)


# ================== TOOLS ==================

search_tool = DuckDuckGoSearchRun(region="us-en")




@tool
def get_stock_price(name: str) -> dict:
    """
    Fetch latest stock price using Alpha Vantage API
    Example: AAPL, TSLA
    """

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={name}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
    r = requests.get(url)
    return r.json()


# # tools = [search_tool, get_stock_price, calculator]


# ================== STATE ==================

class chatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# ================== GRAPH BUILDER ==================

async def build_graph(checkpointer):

    tools = await client.get_tools()

    print(tools)

    llm_with_tool = llm.bind_tools(tools)

    async def chat_node(state: chatState):
        messages = state['messages']
        response = await llm_with_tool.ainvoke(messages)
        return {"messages": [response]}

    tool_node = ToolNode(tools)

    graph = StateGraph(chatState)

    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "chat_node")

    # Conditional routing (tool or end)
    graph.add_conditional_edges("chat_node", tools_condition)

    graph.add_edge("tools", "chat_node")

    chatbot = graph.compile(checkpointer=checkpointer)

    return chatbot

# ================== MAIN ==================

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

async def main():

    async with AsyncSqliteSaver.from_conn_string("chatbot.db") as checkpointer:

        chatbot = await build_graph(checkpointer)

        # Better query for tool triggering
        query = "What is 542 squared multiplied by 453 squared?"

        result = await chatbot.ainvoke(
            {"messages": [HumanMessage(content=query)]},
            config={"configurable": {"thread_id": "thread-1"}}
        )

        print("\nAI Response:\n")
        print(result["messages"][-1].content)


# ================== RUN ==================

if __name__ == "__main__":
    asyncio.run(main())