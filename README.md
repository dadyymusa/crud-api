# Task API

A simple to do list (crud api) 

## Getting Started

Make your own environment (optional) : `python -m venv venv`

- Activate : `source venv/bin/activate`

- Deactivate : `deactivate`

Install Dependencies:

- `pip install uv`

- `pip install "fastapi[standard]"`

Start with :

- `uv run fastapi dev`

- The API runs at `http://127.0.0.1:8000`

- Swagger UI : `http://127.0.0.1:8000/docs`


![Swagger-ui](/assets/swagger-ui-docs.png)

## Endpoints

## `GET /`

Return the metadata about the API.

### Response

`{ "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }`

![Get/](/assets/get-slash-endpoint.png)

### Example

`curl http://localhost:8000/`

## `GET /health`

Health check endpoint

### Respose

`{ "status": "ok" }`

![Get/health](/assets/get-slash-health-endpoint.png)


### Example

`curl http://localhost:8000/health`

## `GET /tasks`

Returns all tasks. 

### Response 

![Get/tasks](/assets/get-tasks-endpoint.png)

### Example

`curl http://localhost:8000/tasks`

## `GET /tasks/:id`

Returns a single task by id.

### Response (200)

`{ "id": 1, "title": "Clean House", "done": false }`

### Response (404)

`{ "error" : "Task 99 not found" }`

## `POST /tasks`

Creates new task 

### Request Body

`{ "title" : "Read a book" }`

### Response (201)

`{ "id": 4, "title": "Buy milk", "done": false }`

### Response (400)

` { "error": "No input given" } `

### Example

`curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'`

## `PUT /tasks/:id`

Updates a task (title and done) by it's id

### Request Body 

` {"title" : "Clean House", "done" : true} `

### Response (200)

` { "id": 1, "title": "Clean House", "done": true } `

### Response (400)

` {"error" : "Empty or Invalid Body"} `

### Response (404)

` {"error" : "Unknown id"} `

### Example

`curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'`

## `DELETE /tasks/:id`

Deletes task by id. 

### Response (204)

Empty body - success, nothing to return.

### Response (404)

` {"error" : "Unknown id"} `

### Example

`curl -X DELETE http://localhost:8000/tasks/1`

## Database & Setup Information

### Why SQLite Was Chosen
* **Zero Configuration:** Lightweight and serverless—no separate database server process to install, configure, or maintain.
* **Built-in Python Support:** Uses Python's native `sqlite3` standard library, eliminating the need for heavy external drivers during early development.
* **Single-File Portability:** Storing the database as a single file makes local development, testing, and sharing easy across environments.

---

### Database File Location
The database file is created and stored locally in the root directory of the project:
`./tasks.db`

![Database Screenshot](/assets/database-view.png)

![Database Screenshot](/assets/database-query-view.png)