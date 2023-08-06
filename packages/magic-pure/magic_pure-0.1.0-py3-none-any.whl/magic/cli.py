import click

import magic


@click.command()
@click.argument("filename")
def entry_point(filename: str):
    print(f"{filename}: {magic.from_file(filename)}")
