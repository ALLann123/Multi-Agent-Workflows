#!/usr/bin/python3
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import json
import httpx
from bs4 import BeautifulSoup

load_dotenv()

mcp=FastMCP("docs")

USER_AGENT="docs-api/1.8"

SERPER_URL="https://google.serper.dev/search"

docs_url={
    "langchain":"python.langchain.com/docs",
    "llama-index":"docs.llamaindex.ai/en/stable",
    "openai":"platform.openai.com/docs",
}


#get the search results of our URL
async def search_web(query:str)->dict | None:
    #send in the query and the number of results we want
    payload=json.dumps({"q":query, "num":2})

    #initialize serper which we will use to search
    headers={
        "X-API-KEY":os.getenv("SERPER_API_KEY"),
        "Content-Type":"application/json",
    }

    #sends in our search query
    async with httpx.AsyncClient() as client:
        try:
            response=await client.post(
                SERPER_URL, headers=headers, data=payload, timeout=30.0
            )
            response.raise_for_status()
            #GET THE RESULTS IN A DICTIONARY
            return response.json()
        except httpx.TimeoutException:
            return {"organic":[]}

#get contents of the URL
async def fetch_url(url: str):
    async with httpx.AsyncClient() as client:
        try:
            #sends a get request and scrape the URL text
            response=await client.get(url, timeout=30.0)
            soup = BeautifulSoup(response.text, "html.parser")
            text=soup.get_text()
            return text
        except httpx.TimeoutException:
            return "Timeout error"

#decorator below converts our function to an MCP compatable tool
@mcp.tool()
async def get_docs(query: str, library:str):
    """
    Search the latest docs for a given query and library.
    Supports langchain, openai, and llama-index.

    Args:
        query: The query to search for (e.g. "Chroma DB")
        library: The library to search in (e.g. "langchain")

    Returns:
        Text from the docs
    """
    #check if the documentation is in the 
    if library not in docs_url:
        raise ValueError(f"Library {library} not supported by this tool")
    
    query=f"site:{docs_url[library]} {query}"

    results=await search_web(query)

    if len(results["organic"]) == 0:
        return "No Results Found"
    
    text=""
    for result in results["organic"]:
        text=await fetch_url(result["link"])
    return text

if __name__ =="__main__":
    mcp.run(transport="stdio")
    




