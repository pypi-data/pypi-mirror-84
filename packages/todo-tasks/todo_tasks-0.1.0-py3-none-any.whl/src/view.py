from typing import List

from rich import print
from rich.table import Table
from rich.console import Console

from .models import Data, Item
from .time import get_time_difference


class ListView:
    def __init__(self, items: List[Item]) -> None:
        self._items = items

    def print(self) -> str:
        console = Console()
        table = Table()

        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Tags", style="red")
        table.add_column("Status")
        table.add_column("Created", justify="right", style="green")

        for item in self._items:
            table.add_row(*self.get_row(item))

        console.print(table)

    def get_row(self, item: Item) -> str:
        return (f"#{item.id}", item.title, self.get_tags(item.tags), item.state, get_time_difference(item.created_at))

    def get_tags(self, tags: List[str]) -> str:
        return " ".join(map(lambda i: f"+{i}", tags))
