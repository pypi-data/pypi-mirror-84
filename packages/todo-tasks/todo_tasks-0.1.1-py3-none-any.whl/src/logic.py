import json
import yaml
from typing import List

from .editor import Editor
from .models import Data, Item, ItemState


class Logic:
    def __init__(self, data: Data) -> None:
        self._data = data

    def list_all(self) -> List[Item]:
        return self._data.items

    def add(self, title: str, new_id: int, state: str) -> Data:
        self._data.items.append(Item(id=new_id, title=title, state=ItemState(state)))
        return self._data

    def remove(self, task_id: int) -> None:
        self._data.items = [i for i in self._data.items if i.id != task_id]
        return self._data

    def edit(self, task_id: int) -> Item:
        item_id = next(i for i, item in enumerate(self._data.items) if item.id == task_id)
        item = self._data.items[item_id]
        editor = Editor(yaml.dump(item.dict(include={"title", "state", "tags"})))
        new_item_dict = yaml.safe_load(editor.edit())
        self._data.items[item_id] = Item(**{**item.dict(), **new_item_dict})
        return self._data
