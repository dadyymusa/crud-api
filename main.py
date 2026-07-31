from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

tasks = [ 
    {"id": 1, "title": "Clean the car", "done" : True},
    {"id": 2, "title": "Clean the house", "done" : False},
    {"id": 3, "title": "Clean the garage", "done" : False}
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

@app.get("/tasks/{id}")
async def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
        
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
