from fastapi import FastAPI
from cruds import server
from routers import server
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*", "https://minipc-status.togetine.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routersディレクトリのを読み込み
app.include_router(server.router)