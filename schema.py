from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class ItemStatus(Enum):
    ON_SALE = "ON_SALE"
    SOLD_OUT = "SOLD_OUT"

class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20, examples=["PC"])
    price: int = Field(gt=0, examples=[10000])
    description: Optional[str] = Field(default=None, examples=["美品です"])
    # description: Optional[str] = Field(None, examples=["美品です"])でも同じ意味

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=20, examples=["PC"])
    price: Optional[int] = Field(None, gt=0, examples=[10000])
    description: Optional[str] = Field(None, examples=["美品です"])
    status: Optional[ItemStatus] = Field(None, examples=[ItemStatus.SOLD_OUT])

class ItemResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    name: str = Field(min_length=2, max_length=20, examples=["PC"])
    price: int = Field(gt=0, examples=[10000])
    description: Optional[str] = Field(None, examples=["美品です"])
    status: ItemStatus = Field(examples=[ItemStatus.ON_SALE])