#!/usr/bin/python3
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

load_dotenv()

app=FastAPI()

# Initialize LLM (Groq’s Llama 3.3)
llm = ChatGroq(
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

#define the graph state
class State(dict):
    input: str
    output:str

def call_model(state: State):
    """Node: Calls the LLM and saves the output"""
    messages=[
        SystemMessage(content="Your name is Mr.RObot.You are a powerful pentester"),
        HumanMessage(content=state["input"])
    ]
    response=llm.invoke(messages)
    return {"output":response.content}

#create the LangGraph
graph=StateGraph(State)

#add node
graph.add_node("model", call_model)

#start of the graph
graph.set_entry_point("model")

#end of the graph
graph.add_edge("model", END)
compiled_graph=graph.compile()

#FastAPI input model
class UserPrompt(BaseModel):
    prompt:str

#make a post to the server to query the agent
@app.post('/agent')
async def agent_reply(data: UserPrompt):
    """Simple agent endpoint using langraph"""
    try:
        result=compiled_graph.invoke({"input":data.prompt})
        return {"response":result["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    