from fastapi import APIRouter, Path, Query, HTTPException
from starlette import status
from cruds import server as server_cruds
from schema import ItemCreate, ItemUpdate, ItemResponse
import socket
from pydantic import BaseModel;
import subprocess

class ServerStatus(BaseModel):
    status: str
    host: str
    
router = APIRouter(prefix="/servers", tags=["Servers"])

@router.get("", response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def find_all():
    return server_cruds.find_all()

# 同じホスト内のサーバが動いているかをプロセス名から確認する
@router.get("/{server_name}/status", status_code=status.HTTP_200_OK)
async def get_status_by_name(server_name: str=Path()):
    host = "127.0.0.1"  # = localhost
    status = ""
    if(server_name == "valheim"):
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True
        )

        # ps aux の結果から valheim_server を検索
        is_running = any(
            "valheim_server" in line.lower()
            for line in result.stdout.splitlines()
        )

        if is_running:
            status = "running"
        else:
            status = "stopped"

        return ServerStatus(
            status=status,
            host="valheim"
        )
    raise HTTPException(status_code=404, detail="Server not found")
