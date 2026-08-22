from fastapi import APIRouter, Path, Query, HTTPException
from starlette import status
from cruds import server as server_cruds
from schema import ItemCreate, ItemUpdate, ItemResponse
import socket
from pydantic import BaseModel;

class ServerStatus(BaseModel):
    status: str
    host: str
    port: int

router = APIRouter(prefix="/servers", tags=["Servers"])

@router.get("", response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def find_all():
    return server_cruds.find_all()

# 同じホスト内のサーバが動いているかをポート確認する
@router.get("/{server_name}/status", status_code=status.HTTP_200_OK)
async def get_status_by_name(server_name: str=Path()):
    host = "127.0.0.1"  # = localhost
    status = ""
    if(server_name == "valheim"):
        # ポート検索
        port = 3030
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
        if(result == 0):
            status = "running"
        else:
            status = "stopped"
        return ServerStatus(
            status=status,
            host=host,
            port=port
        )
    raise HTTPException(status_code=404, detail="Server not found")