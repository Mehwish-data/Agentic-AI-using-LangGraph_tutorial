from langgraph.graph import StateGraph, START, END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv() 

llm = ChatGoogleGenerativeAI()


class ChatSheet(TypedDict):
    message: Annotated[list[BaseMessage], add_messages]
    
    
def chat_node(state: ChatState):
    message = state['messsages']
    response = llm.invoke(message)
    return {"message" : [response]}

#Checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node",chat_node)
graph.add_node(START,"chat_node")
graph.add_node("chat_node", END)

chatbot =graph.compile(checkpointer=checkpointer)
    
