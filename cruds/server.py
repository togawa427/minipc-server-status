from typing import Optional
from schema import ItemCreate, ItemStatus, ItemUpdate

class Server: 
    def __init__(
            self,
            id: int,
            name: str,
            price: int,
            description: Optional[str],
            status: ItemStatus
    ):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.status = status

servers = [
    Server(1, "PC", 100000, "美品です", ItemStatus.ON_SALE),
    Server(2, "スマートフォン", 50000, None, ItemStatus.ON_SALE),
    Server(3, "Python本", 1000, "使用感あり", ItemStatus.SOLD_OUT),
]

def find_all():
    return servers