"""Show Command.

Provides information about services.
"""
import typer
from tabulate import tabulate

from ..enums import Service
from ..services import DockerHub, Github
from ..settings import EPILOG, SABALCORE_NODES

app = typer.Typer(
    name="show", help="Show information about external services.", epilog=EPILOG
)
dh_openbcl_fds = DockerHub("openbcl", "fds")
gh_firemodels_fds = Github("firemodels", "fds")


@app.command(
    help="Show avaliable tags for docker images or fds versions.", epilog=EPILOG
)
def versions(
    service: Service = typer.Argument(
        Service.FDS, case_sensitive=False, help="Service to show"
    ),
    latest: bool = typer.Option(False, help="Only show latest tag."),
) -> None:
    if service == Service.DOCKER:
        if latest:
            typer.echo(dh_openbcl_fds.latest_tag())
        else:
            typer.echo(", ".join(dh_openbcl_fds.tag_list()))
    elif service == Service.FDS:
        if latest:
            typer.echo(gh_firemodels_fds.latest_tag())
        else:
            typer.echo(", ".join(gh_firemodels_fds.tag_list()))


@app.command(help="Show avaliable nodes for sabalcore.", epilog=EPILOG)
def nodes() -> None:
    columns = list(list(SABALCORE_NODES.values())[0].keys())
    data = [
        [name] + [node[column] for column in columns]
        for name, node in SABALCORE_NODES.items()
    ]
    columns.insert(0, "node")

    typer.echo(tabulate(data, headers=columns))
