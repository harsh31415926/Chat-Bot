from langgraph.graph import StateGraph , START ,END
from typing import TypedDict , Annotated
from langchain_core.messages import HumanMessage,BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from dotenv import load_dotenv  

from langgraph.prebuilt import ToolNode , tools_condition
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

import requests
import random

import os
load_dotenv()

search_tool = DuckDuckGoSearchRun(region = "us-en")

@tool
def calculator(first:float , second:float , operation:str)-> float :

    """
    Perform a basic arithematic operation between first and second number
    Supported operation = [add , sub , mul , div]
    """

    try :
        if operation == 'add':
            res =  first + second
        elif operation == 'sub':
            res = first - second
        elif operation == 'mul':
            res = first * second
        elif operation == 'div':
            res = first / second
        else :
            return {'error' : f"The operation is absurd {operation}"}

        return {"first_number" :first , "Second_number" : second , "Operation" : operation , "answer" : res}
        
    except Exception as e :
        print("The problem is " , e)

@tool
def get_stock_price(name:str)->dict:
    """
    Fetch latest stock price of the stocks that have been asked 
    eg ("AAPL", "TSLA")
    using Alpha Ventage API key
    """

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={name}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
    r = requests.get(url)
    return r.json()



llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# ======================== Checkpointer =============================
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

conn = sqlite3.connect("chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)


def retrieve_all_threads():
    ls = set()
    for msg in checkpointer.list(None):
        ls.add(msg.config['configurable']['thread_id'])
    return list(ls) 


tools = [search_tool ,get_stock_price,calculator]

llm_with_tool = llm.bind_tools(tools)

class chatState(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages]

def chat_node(state:chatState):
    """LLM node that may answer or request a tool call """
    message= state['messages']
    res= llm_with_tool.invoke(message)
    return {'messages' : [res]}

tool_call = ToolNode(tools)

graph = StateGraph(chatState)

graph.add_node('chat_node' , chat_node)
graph.add_node('tools' , tool_call)

graph.add_edge(START , 'chat_node')

# ===================Add conditional Edge=======================

graph.add_conditional_edges("chat_node" , tools_condition) 
graph.add_edge('tools', 'chat_node')

# tools_condition --> if need tool go to tool else go to the END

chatbot = graph.compile(checkpointer = checkpointer)

result = chatbot.invoke({"messages" :[HumanMessage(content="Find the multiplication of 3 and 342 and tell it in the way of ElonMusk")]},
                        config = {'configurable' : {'thread_id' : 'thread-1'}})

print(result['messages'][-1].content)
