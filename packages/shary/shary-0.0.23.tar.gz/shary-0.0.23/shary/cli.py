# cli.py

import click # cli
import os # path and file handling

# import all hosting services


@click.group()
def cli():
    pass

@cli.command()
@click.option("--service", "-s", required=True, type=str, help="Choose a Hosting service")
@click.option("--file", "-f", required=True, type=str, help="Path to file")
def upload(service, file):
    """Uploads a file

    Args:
        service (str): define the service
        file (str): path to file
    """
    click.echo("work in progress :)")

if __name__ == "__main__":
    cli()