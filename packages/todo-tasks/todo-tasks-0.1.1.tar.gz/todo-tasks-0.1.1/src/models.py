from __future__ import annotations

from enum import Enum
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field


class GlobalConfig(BaseModel):
    all_tasks_files: List[str] = []
    items_counter: int = 0

    def increase_items_counter(self) -> None:
        self.items_counter += 1


class ItemState(str, Enum):
    NEW = "NEW"
    TODO = "TODO"
    DONE = "DONE"


class Item(BaseModel):
    id: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    state: ItemState = ItemState.NEW
    tags: List[str] = []
    title: str

    class Config:
        use_enum_values = True


class Data(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    items: List[Item] = []
