#!/usr/bin/python3
from fastapi import FastAPI

#create a FASTAPI object
api=FastAPI()

# GET, POST, PUT, DELETE
#GET- when we want to get information to a server.
#POST- we want to add something to a server
# PUT- updating something on the server
#DELETE- Removing something from the server

#creating an endpoint
@api.get('/')
def index():
    return {"message":"Hello World"}

"""
TO RUN:
    cmd>> fastapi dev fast_api_hello_world.py --port 444

"""
