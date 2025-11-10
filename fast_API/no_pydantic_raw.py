#!/usr/bin/python3
from fastapi import FastAPI

#create a FASTAPI object
api=FastAPI()

#make a simple database using a list and dict
all_todos=[
    {'todo_id':1, 'todo_name':'Sports','todo_description': 'Go to the gym'},
    {'todo_id':2, 'todo_name':'Read','todo_description': 'Read 10 pages'},
    {'todo_id':3, 'todo_name':'Shop','todo_description': 'Go shopping'},
    {'todo_id':4, 'todo_name':'Study','todo_description': 'Study for exam'},
    {'todo_id':5, 'todo_name':'Meditate','todo_description': 'Meditate 20 minutes'}
]

#creating an endpoint
@api.get('/')
def index():
    return {"message":"Hello World"}

#Endpoint with user input
@api.get('/todos/{todo_id}')
def get_tod(todo_id:int):
    for todo in all_todos:
        if todo['todo_id']==todo_id:
            return {'result':todo}
#how to query this endpoint: http://127.0.0.1:444/todos/  ----> you get all todos
#specify todo ID: http://127.0.0.1:444/todos/1

@api.get('/todos') 
def get_todo(first_n:int=None):
    if first_n:
        #range of todos to be displayed
        return all_todos[:first_n]
    else:
        return all_todos
# how to query the above end point:  http://127.0.0.1:444/todos?first_n=1


#make a POST endpoint
@api.post('/todos')
def create_todo(todo: dict):
    new_todo_id=max(todo['todo_id'] for todo in all_todos) + 1
    new_todo={
        'todo_id':new_todo_id,
        'todo_name':todo['todo_name'],
        'todo_description':todo['todo_description']
    }
    all_todos.append(new_todo)

    return new_todo

#Update method
@api.put('/todos/{todo_id}')
def update_todo(todo_id: int, updated_todo:dict):
    for todo in all_todos:
        if todo['todo_id']==todo_id:
            todo['todo_name']=updated_todo['todo_name']
            todo['todo_description']=updated_todo['todo_description']
            return todo
    return "Error, todo not Found"

@api.delete('/todos/{todo_id}')
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo['todo_id']==todo_id:
            deleted_todo=all_todos.pop(index)
            return deleted_todo
    return "Error, not found!!"
