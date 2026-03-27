from langgraph.graph import StateGraph , START ,END
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage
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
    response = llm.invoke(messages)
    return {'messages' : response}

checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node('chat_node' , chat_node)

graph.add_edge(START , 'chat_node')
graph.add_edge('chat_node' , END)

chatbot = graph.compile(checkpointer = checkpointer)