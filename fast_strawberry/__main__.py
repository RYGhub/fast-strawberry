import click
import httpx
import time


@click.command()
@click.option(
    "-s", "--server", "server",
    required=True,
    help="The server where impressive-strawberry is hosted on, with no trailing slash."
)
@click.option(
    "-t", "--application-token", "application_token",
    required=True,
    help="The token of the application to authenticate as."
)
@click.option(
    "-g", "--group", "group",
    required=True,
    help="The group to interact with.",
)
@click.option(
    "-a", "--achievement", "achievement",
    required=True,
    help="The achievement to award to the specified users.",
)
@click.argument(
    "users",
    nargs=-1,
)
def mass_award(server: str, application_token: str, group: str, achievement: str, users: list[str]):
    click.secho("Unlocking achievement for ", nl=False, fg="blue")
    click.secho(f"{len(users)}", nl=False, fg="brightblue")
    click.secho("...", nl=True, fg="blue")
    with httpx.Client(headers={
        "Authorization": f"Bearer {application_token}",
    }) as h:
        for user in users:
            unlock = h.post(f"{server}/api/unlock/v1/", params={
                "achievement": achievement,
                "group": group,
                "user": user,
            })
            if unlock.status_code == 201:
                click.secho("Unlock successful for ", nl=False, fg="green")
                click.secho(f"{user}", nl=False, fg="brightgreen")
                click.secho("!", nl=True, fg="green")
            else:
                click.secho("Unlock failed for", nl=False, fg="red")
                click.secho(f"{user}", nl=False, fg="brightred")
                click.secho("!", nl=True, fg="red")
            time.sleep(0.5)


if __name__ == "__main__":
    mass_award()
