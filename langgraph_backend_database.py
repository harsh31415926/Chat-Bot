from langgraph.graph import StateGraph , START ,END
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.sqlite  import SqliteSaver
from langgraph.graph import add_messages
import sqlite3


load_dotenv()

import os 


llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages]


def chat_node(state :ChatState):

    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages' : response}


conn= sqlite3.connect(database = 'chatbot.db' , check_same_thread = False)
checkpointer = SqliteSaver(conn = conn)

graph = StateGraph(ChatState)
graph.add_node('chat_node' , chat_node)

graph.add_edge(START , 'chat_node')
graph.add_edge('chat_node' , END)

chatbot = graph.compile(checkpointer = checkpointer)


def retrieve_all_threads():
    ls = set()
    for msg in checkpointer.list(None):
        ls.add(msg.config['configurable']['thread_id'])
    return list(ls) 

