"""Console script for fcust."""
import click
from pathlib import PosixPath
from fcust.fcust import CommonFolder


@click.group()
def main(args=None):
    """Folder Custodian main command"""
    click.echo("Welcome to Fedora Folder Custodian")


@click.command()
@click.argument("folder_path")
def run(
    folder_path: str,
    help="Path where the common foler is located",
):
    fpath = PosixPath(folder_path)
    if not fpath.exists():
        raise FileNotFoundError(f"Specified folder {folder_path} does not exist!")

        # assume common folder itself has been created with proper group and permissions.
    click.echo(f"Initiating maintenance on {folder_path}")
    cf = CommonFolder(folder_path=fpath)
    cf.enforce_permissions()
    click.echo("Common folder maintenance completed.")


main.add_command(run)
