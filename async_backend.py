from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from dotenv import load_dotenv  

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

import requests
import asyncio
import os

# ================== ENV ==================
load_dotenv()

# ================== TOOLS ==================

search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first: float, second: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation.
    Supported operations: add, sub, mul, div
    """

    try:
        if operation == 'add':
            res = first + second
        elif operation == 'sub':
            res = first - second
        elif operation == 'mul':
            res = first * second
        elif operation == 'div':
            res = first / second
        else:
            return {"error": f"Invalid operation: {operation}"}

        return {
            "first_number": first,
            "second_number": second,
            "operation": operation,
            "answer": res
        }

    except Exception as e:
        return {"error": str(e)}


@tool
def get_stock_price(name: str) -> dict:
    """
    Fetch latest stock price using Alpha Vantage API
    Example: AAPL, TSLA
    """

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={name}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
    r = requests.get(url)
    return r.json()


tools = [search_tool, get_stock_price, calculator]

# ================== LLM ==================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

llm_with_tool = llm.bind_tools(tools)

# ================== STATE ==================

class chatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# ================== GRAPH BUILDER ==================

def build_graph(checkpointer):

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

        chatbot = build_graph(checkpointer)

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