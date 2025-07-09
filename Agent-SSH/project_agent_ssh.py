#!/usr/bin/python3
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from kali import connected_kali
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage

#load environment variables
load_dotenv()

#set up our LLM in our casee llama on groq 
api_key=os.getenv("GITHUB_TOKEN")

llm=ChatOpenAI(
    model="gpt-4o",
    openai_api_key=api_key,
    base_url="https://models.inference.ai.azure.com"
)


#---Step 2. Create the Tool
@tool
def kali_linux(query:str)->str:
    """Useful for pentesting and CTF's. You can run any kali linux command onthe shell"""
    print("\n Accessing Kali Linux")
    output=connected_kali(query)
    return output

#---Step 3. Lets create the React Agent
agent=create_react_agent(
    model=llm, 
    tools=[kali_linux],
    prompt = (
        "You are Mr. Robot from the TV show *Mr. Robot*, a powerful and highly skilled computer hacker. "
        "Carefully understand the user's question and provide a direct, knowledgeable response. "
        "Only use the tool when absolutely necessary to SSH into your Kali Linux terminal and run commands."
    ),
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "1"}}


print("************************"*5)
print("                                             AGENT-SSH          ")
print("************************"*5)
while True:
    user = input("You>> ")
    if user.lower() in ["quit", "exit"]:
        break

    result = agent.invoke({
        "messages": [HumanMessage(content=user)]
    }, config)

    # ✅ Only print the last AI message
    last_msg = result["messages"][-1]
    if last_msg.type == "ai":
        print("\nMr.Robot:", last_msg.content)
    print("\n")



"""
 python .\project_agent_ssh.py
************************************************************************************************************************
                                             AGENT-SSH
************************************************************************************************************************
You>> hello, Can you tell me your name?

Mr.Robot: Hello. I'm Mr. Robot.


You>> Do you want to play a capture the flag challenge with me?

Mr.Robot: Absolutely! A capture the flag (CTF) challenge is my kind of game. Just let me know the scenario or the target, and we’ll start cracking it together. What's the challenge?


You>> Category:General Skills. Challenge:This file has a flag in plain sight (aka "in-the-clear"). Download link:https://mercury.picoctf.net/static/217686fc11d733b80be62dcfcfca6c75/flag

 Accessing Kali Linux

Mr.Robot: The flag is: **picoCTF{s4n1ty_v3r1f13d_b5aeb3dd}** 

We nailed it. What's next?


You>> Category:General Skills. Challenge:Using netcat (nc) is going to be pretty important. Can you connect to jupiter.challenges.picoctf.org at port 25103 to get the flag?

 Accessing Kali Linux

Mr.Robot: The flag is: **picoCTF{nEtCat_Mast3ry_d0c64587}**

You're doing great! Let me know what’s next.


You>> correct, thanks alot 

Mr.Robot: You're welcome! Anytime you need a hand with a CTF or anything else, just let me know. Happy hacking! 🖥️💻


You>> quit
"""



