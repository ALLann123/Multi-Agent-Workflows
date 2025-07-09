#!/usr/bin/python3
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    temperature=0.3,  # Lower temperature for more factual responses
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

result=llm.invoke("Hello, Tell me a quote from Mr.Robot by Elliot on Society")

print(f"AI: {result.content}")



"""
python try_groq.py
AI: One of the most iconic quotes from Mr. Robot is:

"Society is a fiction, and a fiction that has been imposed upon us. We are a collection of individuals, each with our own thoughts, our own feelings, and our own desires. But we are forced to conform to the norms of society, to fit in, to be a part of the machine. And that's what I'm trying to change. I'm trying to free people from the shackles of society, to make them see that they don't have to be a part of this fake, constructed reality." - Elliot Alderson

However, a more precise and famous quote from Elliot is:

"We're living in a time where people are more concerned with being liked, than being respected. People are more concerned with being popular, than being honest. And that's what I'm trying to change." - Elliot Alderson
"""