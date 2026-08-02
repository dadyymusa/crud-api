from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Task(BaseModel):
    id : int 
    title : str
    done : bool = False

class NewTask(BaseModel):
    title : str

tasks : List[Task] = [
    Task(id= 1, title= "Clean House", done= False),
    Task(id= 2, title= "Read a Book", done= "False"), 
    Task(id= 3, title= "Leetcode for 1hr", done= "False")
]




@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")
async def get_tasks():
    return tasks 

# @app.get("/tasks/{id}")
# async def get_task(id: int):
#     for task in tasks:
#         if task["id"] == id:
#             return task
        
#     return JSONResponse(status_code= 404, content={"error" : f"Task {id} not found"})

@app.get("/tasks/{id}")
async def get_task(id: int):
    for task in tasks:
        if task.id == id:
            return task
        
    return JSONResponse(status_code= 404, content= {"error": f"Task {id} not found"})


@app.post("/tasks")
async def create_task(task: NewTask):
    if task.title == None or task.title == "string" or len(task.title) == 0:
        return JSONResponse(status_code= 400, content= { "error" : "No input given"})
    else:
        add_task = Task(id = len(tasks) + 1, title =  task.title, done = False)
        tasks.append(add_task)
        return JSONResponse(status_code= 201, content= add_task.dict())
