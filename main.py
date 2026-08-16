from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import sqlite3


app = FastAPI()

def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row

    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY, 
            title TEXT,
            done BOOLEAN
        )
    """)

    count = cursor.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        tasks = [(1, 'Clean House', False), (2, 'Clean Car', False), (3, 'Read a Book', False)]
        cursor.executemany("""
            INSERT INTO tasks(id, title, done)
            VALUES(?,?,?)
    """, tasks)

    conn.commit()
    conn.close()

init_db()



class Task(BaseModel):
    id : int 
    title : str
    done : bool

class NewTask(BaseModel):
    title : str

class UpdateTask(BaseModel):
    title : str
    done : bool

def next_id():
    return tasks[-1].id + 1


#Root 
@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

#Status
@app.get("/health")
async def health():
    return { "status": "ok" }

#Read all the task 
@app.get("/tasks")
async def get_tasks():
    conn = get_db()
    curr = conn.cursor()

    tasks = curr.execute("SELECT * from tasks").fetchall()

    conn.close()
    return tasks

#Search & Read a specific task by id 
@app.get("/tasks/{id}")
async def get_task(id: int):
    conn = get_db()
    curr = conn.cursor()
    task = curr.execute("SELECT * FROM tasks WHERE id = ?", (id, )).fetchone()

    conn.close()

    if not task:
        return JSONResponse(status_code= 404, content= {"error": f"Task {id} not found"})
    
    return task
    

#Create a new task 
@app.post("/tasks")
async def create_task(task: NewTask):
    if task.title == None or task.title == "string" or len(task.title) == 0:
            return JSONResponse(status_code= 400, content= {"error" : "No input given"})
    else:
        conn = get_db()
        curr = conn.cursor()

        curr.execute("""INSERT INTO tasks(title, done)
                        VALUES(?, ?)
        
        """, (task.title, False))

        conn.commit()
        new_id = curr.lastrowid
        current_task = curr.execute("SELECT * FROM tasks WHERE id = ?", (new_id,)).fetchone()
        conn.close()

        return JSONResponse(status_code= 201, content= dict(current_task))



    
    # else:
    #     add_task = Task(id= next_id(tasks), title=  task.title, done= False)
    #     tasks.append(add_task)
    

#Update an old task by id
@app.put("/tasks/{id}")
async def update_task(id: int, update: UpdateTask):

    if not update.title or update.title.strip() == "" or update.title == "string" or update.done == None:
        return JSONResponse(status_code=400, content= {"error" : "Empty or Invalid Body"})
    
    conn = get_db()
    curr = conn.cursor()

    task = curr.execute("SELECT * FROM tasks WHERE id = ?", (id, )).fetchone()

    if not task:
        conn.close()
        return JSONResponse(status_code= 404, content= {"error" : "Unknown id"})
    else:
        curr.execute("""UPDATE tasks SET title = ?, done = ? WHERE id = ?
        """, (update.title, update.done, id))
        
        conn.commit()
        conn.close()

        

            
    

@app.delete("/tasks/{id}")
async def delete_task(id: int):
    conn = get_db()
    curr = conn.cursor()

    task = curr.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()

    if not task:
        conn.close()
        return JSONResponse(status_code=404, content= {"error": "Unknown id"})
    else:
        curr.execute("DELETE FROM tasks WHERE id = ?", (id,))
        conn.commit()
        conn.close()

        return JSONResponse(status_code=204, content= None)

