import click

@click.command()
def hello():
    """Say hello."""
    print("Hello, world!")

command = hello
