#!/usr/bin/python3
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app=FastAPI()

#load environment variables
load_dotenv()

#set up our LLM in our casee llama on groq 
llm = ChatGroq(
    temperature=0.3,  # Lower temperature for more factual responses
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

class Talk(BaseModel):
    prompt: str  #user input text


#define our endpoint
@app.post('/groq')
async def chat_with_groq(data: Talk):
    try:
        #send the users prompt
        response=llm.invoke(data.prompt)
        return {"response":response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
To run: fastapi dev .\chat_cli.py --port 4444
"""