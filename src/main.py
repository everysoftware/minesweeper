from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.controllers import routers
from src.schemes import ErrorResponse

app = FastAPI(title="Minesweeper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://minesweeper-test.studiotg.ru"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authentication",
    ],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_app: FastAPI, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=exc.detail).model_dump(),
    )


for router in routers:
    app.include_router(router)
