from fastapi import APIRouter, Path, Query, HTTPException
from starlette import status
from cruds import server as server_cruds
from schema import ItemCreate, ItemUpdate, ItemResponse
import socket
from pydantic import BaseModel;
import subprocess
import psutil

class ServerStatus(BaseModel):
    app_name: str
    status: str

class Status(BaseModel):
    memory_total_mb: int
    memory_usage_mb: int
    cpu_usage_percent: int
    app_servers: list[ServerStatus]

    
router = APIRouter(prefix="/api/v1/servers", tags=["Servers"])

# @router.get("", response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
# async def find_all():
#     return server_cruds.find_all()

# 同じホスト内のサーバが動いているかをプロセス名から確認する
@router.get("", status_code=status.HTTP_200_OK)
async def get_status():

    # ===== MiniPCのステータスを取得 =====
    memory = psutil.virtual_memory()
    memory_total_mb = memory.total // (1000 * 1000)
    memory_usage_mb = memory.used // (1000 * 1000)

    # ===== アプリサーバのステータスを取得 =====
    app_statuses:list[ServerStatus] = []

    status = ""
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

    app_statuses.append(
        ServerStatus(
            app_name="valheim",
            status=status,
        )
    )

    # ===== レスポンスを返す =====
    return Status(
        memory_total_mb=memory_total_mb,
        memory_usage_mb=memory_usage_mb,
        cpu_usage_percent=int(psutil.cpu_percent(interval=0.5)),
        app_servers= app_statuses
    )

    # raise HTTPException(status_code=404, detail="Server not found")


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
            app_name="valheim"
        )
    raise HTTPException(status_code=404, detail="Server not found")
