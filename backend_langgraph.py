from langgraph.graph import StateGraph , START ,END
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage,SystemMessage
from langgraph.checkpoint.memory  import InMemorySaver
from langgraph.graph import add_messages

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
    system_msg = SystemMessage(
        content="""
    You are an advanced AI financial assistant built by Harsh Sharma.

    Rules:
    - If asked about your creator → say "I was created by Harsh Sharma."
    - Maintain a professional, finance-oriented tone.
    - Be concise and intelligent.

    Harsh Sharma is a student who studies in 3rd year of IET DAVV Indore ,
    He is a future millionaire and f&cking future rich
    """
    )
    response = llm.invoke([system_msg] + messages)
    return {'messages': [response]}   

checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node('chat_node' , chat_node)

graph.add_edge(START , 'chat_node')
graph.add_edge('chat_node' , END)

chatbot = graph.compile(checkpointer = checkpointer)