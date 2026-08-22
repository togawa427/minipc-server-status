from fastapi import FastAPI
from cruds import server
from routers import server

app = FastAPI()

# routersディレクトリのを読み込み
app.include_router(server.router)