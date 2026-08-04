from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()


class Task(BaseModel):
    id : int 
    title : str
    done : bool

class NewTask(BaseModel):
    title : str

class UpdateTask(BaseModel):
    title : str
    done : bool

tasks : List[Task] = [
    Task(id= 1, title= "Clean House", done= False),
    Task(id= 2, title= "Read a Book", done= False), 
    Task(id= 3, title= "Leetcode for 1hr", done= False)
]

def next_id(tasks):
    return tasks[-1].id + 1


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
        return JSONResponse(status_code= 400, content= {"error" : "No input given"})
    else:
        add_task = Task(id= next_id(tasks), title=  task.title, done= False)
        tasks.append(add_task)
        return JSONResponse(status_code= 201, content= add_task.model_dump())


@app.put("/tasks/{id}")
async def update_task(id: int, update: UpdateTask):
    if not update.title or update.title.strip() == "" or update.title == "string" or update.done == None:
        return JSONResponse(status_code=400, content= {"error" : "Empty or Invalid Body"})
    else:
        for task in tasks:
            if task.id == id:
                task.title = update.title
                task.done = update.done
                return task.model_dump()
            
    return JSONResponse(status_code= 404, content= {"error" : "Unknown id"})


@app.delete("/tasks/{id}")
async def delete_task(id: int):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return JSONResponse(status_code= 204, content = None)

    return JSONResponse(status_code= 404, content= {"error" : "Unknown id"})