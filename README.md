# Tasks API

DecodeLabs Backend Development, Project 1: REST API Fundamentals.

A small stateless REST API built with FastAPI. It exposes a `tasks` resource
with GET and POST routes, validates input, and returns structured JSON with
accurate HTTP status codes.

**Author:** Nasirov Samandar

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Run the command from the project root. Interactive docs (Swagger UI) are
available at http://127.0.0.1:8000/docs

## Endpoints

| Method | Path        | Description    | Success | Errors |
|--------|-------------|----------------|---------|--------|
| GET    | /health     | Health check   | 200     |        |
| GET    | /tasks      | List all tasks | 200     |        |
| GET    | /tasks/{id} | Get one task   | 200     | 404    |
| POST   | /tasks      | Create a task  | 201     | 400    |

### Request body (POST /tasks)

| Field | Type    | Rules                    |
|-------|---------|--------------------------|
| title | string  | required, 1 to 100 chars |
| done  | boolean | optional, default false  |

## Examples

Create a task:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI"}'
```

```
HTTP/1.1 201 Created
{"title":"Learn FastAPI","done":false,"id":1}
```

Task not found:

```
GET /tasks/99
HTTP/1.1 404 Not Found
{"error":"Task 99 not found"}
```

Invalid input:

```
POST /tasks  with  {"title": ""}
HTTP/1.1 400 Bad Request
{"error":"Validation failed","details":[{"field":"title","message":"String should have at least 1 character"}]}
```

On Windows PowerShell use `curl.exe` instead of `curl`, and escape the quotes
inside the JSON: `-d '{\"title\": \"Learn FastAPI\"}'`.

## Error format

All errors share one JSON shape: `{"error": "..."}`. Validation errors also
include a `details` list with the field name and a message. Unknown paths (404)
and wrong methods (405) use the same format.

## Why FastAPI

I chose FastAPI for four reasons:

- **Validation is part of the schema.** Pydantic models check the request
  body, so rules like "title must be 1 to 100 characters" live in one place
  instead of being repeated as manual `if` checks in every route. This directly
  supports the project's input validation requirement.
- **Routes are easy to read.** The HTTP method, the path and the status code
  are declared in a single decorator, for example
  `@router.post("", status_code=201)`. That makes the routing logic and the
  API contract visible at a glance.
- **Documentation comes for free.** Swagger UI is generated at `/docs`, which
  makes manual testing and review quick without extra tooling.
- **It fits my background.** I mainly work with Python (Django), so I could
  focus on REST concepts such as statelessness, status codes and JSON
  handling instead of learning a new language.

Alternatives considered:

- **Flask** is simple and mature, but request validation and API documentation
  would have to be added by hand or with extra libraries.
- **Express.js** is a strong choice for JavaScript teams, but it would add a
  second language and require manual setup for JSON parsing and validation.
- **Django** was left out on purpose: its ORM, admin and migrations are not
  needed when the project has no database.

## Design decisions

- **Stateless:** no sessions or per-client state. Each request is handled from
  its own URL and JSON body alone.
- **In-memory storage:** tasks live in a Python list because Project 1 has no
  database. Data is lost on restart, and with several workers each one would
  keep its own list. A real deployment would use a database.
- **Separate modules:** schemas and routers are split from `main.py` to keep it
  small and make new resources easy to add.
- **422 to 400:** FastAPI returns 422 for validation errors by default. A custom
  handler returns 400 to match the project requirements.

## Project structure

```
main.py            app setup, health route, error handlers
schemas.py         Pydantic models
routers/tasks.py   /tasks routes
requirements.txt   pinned dependencies
```