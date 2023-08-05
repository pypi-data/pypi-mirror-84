from os import environ as env

import click

from ._client import browser_authenticate, poll_opaque_token_service
from ._crypto import decrypt, generate_keys
from ._pgpass import update_pgpass


@click.command(name="gimme_db_token")
@click.option(
    "--tenant",
    required=True,
    envvar="CYRAL_TENANT",
    show_envvar=True,
    help="Tenant Name",
)
@click.option(
    "--timeout",
    default=5 * 60,
    envvar="CYRAL_DB_TOKEN_TIMEOUT",
    type=click.INT,
    show_envvar=True,
    help="Number of seconds to wait for Cyral server to respond before timeout",
)
@click.version_option(version="0.1.4")
def update_token(tenant, timeout):
    private_key, public_key = generate_keys()
    browser_authenticate(tenant, public_key)
    msg = poll_opaque_token_service(tenant, public_key, timeout)
    access_token = decrypt(msg["EncryptedAccessToken"], private_key)
    if "SidecarEndpoints" not in msg or not msg['SidecarEndpoints']:
        print("No sidecar endpoints received.")
        return
    sidecars = [decrypt(m, private_key) for m in msg["SidecarEndpoints"]]
    update_pgpass(access_token, sidecars)
    print("Success!")
    print("Updated token for the following endpoints:")
    for endpoint in sidecars:
        print(f"- {endpoint}")


def run_silent(*args, **kwargs):
    try:
        update_token(*args, **kwargs)
    except Exception as e:
        # don't print exceptions unless in debug mode
        if env.get("DEBUG"):
            raise e
        else:
            click.Abort()


if __name__ == "__main__":
    update_token(prog_name="gimme_db_token")
