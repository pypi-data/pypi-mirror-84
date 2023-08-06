import click
from rich import print

from .data import DataLoader
from .view import ListView
from .logic import Logic


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail("Too many matches: %s" % ", ".join(sorted(matches)))


@click.group(cls=AliasedGroup)
def cli() -> None:
    pass


@click.command()
def init() -> None:
    data_loader = DataLoader()
    data_loader.create_global_config_if_not_exists()

    if data_loader.exists():
        print("Init file already exists :thumbs_up:")
    else:
        print("Tasks succesfully initialized :thumbs_up:")
        data_loader.init()


@click.command()
def list_all() -> None:
    data_loader = DataLoader()
    data = data_loader.load()
    logic = Logic(data)
    items = logic.list_all()
    view = ListView(items)
    view.print()


@click.command()
@click.confirmation_option(prompt="Are you sure you want to drop all your tasks there?")
def drop() -> None:
    data_loader = DataLoader()
    data_loader.drop()
    print("Local tasks lost forever :sad_panda:")


@click.command()
@click.option("-s", "--state", default="NEW", type=str)
@click.argument("title", type=str, nargs=-1)
def add(state: str, title: str) -> None:
    data_loader = DataLoader()
    data = data_loader.load()
    global_config = data_loader.load_global_config()

    logic = Logic(data)
    new_data = logic.add(" ".join(title), global_config.items_counter, state)
    data_loader.save(new_data)

    global_config.increase_items_counter()
    data_loader.save_global_config(global_config)

    print("Task saved", ":vampire:")


@click.command()
@click.argument("task_id", type=int)
def remove(task_id: str) -> None:
    data_loader = DataLoader()
    data = data_loader.load()

    logic = Logic(data)
    new_data = logic.remove(task_id)
    data_loader.save(new_data)

    print("Task removed :sad_panda:")


@click.command()
@click.argument("task_id", type=int)
def edit(task_id: str) -> None:
    data_loader = DataLoader()
    data = data_loader.load()

    logic = Logic(data)
    new_data = logic.edit(task_id)
    data_loader.save(new_data)

    print("Task removed :sad_panda:")


cli.add_command(add)
cli.add_command(edit)
cli.add_command(remove)
cli.add_command(list_all)
cli.add_command(init)
cli.add_command(drop)
