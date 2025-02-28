import click
from crm.controllers.user_controller import login

@click.group()
def cli():
    """Application CLI Epic Events"""
    pass

cli.add_command(login)

if __name__ == "__main__":
    cli()
