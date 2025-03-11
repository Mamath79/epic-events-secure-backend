import click
from crm.controllers.login_controller import EnterCrm
import config


@click.group()
def cli():
    """Application CLI Epic Events"""
    pass


cli.add_command(EnterCrm)

if __name__ == "__main__":
    EnterCrm()
