from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from routers.tasks import router as tasks_router

app = FastAPI(title="Tasks API", version="1.0.0")
app.include_router(tasks_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Turn FastAPI's default 422 into a 400 with a readable message."""
    details = [
        {
            "field": ".".join(
                str(part) for part in err["loc"][1:] if isinstance(part, str)
            ) or "body",
            "message": err["msg"],
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=400,
        content={"error": "Validation failed", "details": details},
    )


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException):
    """Every HTTP error (404, 405, ...) uses the same JSON shape."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )