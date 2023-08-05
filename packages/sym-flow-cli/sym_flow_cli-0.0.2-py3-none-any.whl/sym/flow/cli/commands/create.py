import os
import sys

import click
import requests

from sym.flow.cli.helpers.login.token import get_auth_header

from ..helpers.global_options import GlobalOptions
from .symflow import symflow

# from swagger_client.api.default_api import DefaultApi as SymApi
# from swagger_client.api_client import ApiClient as SymApiClient
# from swagger_client.configuration import Configuration as SymConfiguration


@symflow.command("create", short_help="Create a resource via Sym API")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument("resource_type", type=click.Choice(["flow"]))
@click.argument("resource_proto_file")
def create(options: GlobalOptions, resource_type: str, resource_proto_file: str) -> None:

    if resource_type == "flow":
        if not os.path.exists(resource_proto_file):
            print(
                f"resource_proto_file ({resource_proto_file}) does not exist",
                file=sys.stderr,
            )
            sys.exit(1)
        with open(resource_proto_file, "rb") as f:
            res = requests.post(
                f"{options.api_url}/v1/flows",
                data=f.read(),
                headers={
                    "Content-Type": "application/x-protobuf",
                    "Authorization": get_auth_header(),
                },
            )
            if res.ok:
                print("Created flow", file=sys.stderr)
                print(res.json()["uuid"])
            else:
                print("Failed to create flow", file=sys.stderr)
                print(res.text, file=sys.stderr)
                sys.exit(2)
            # This does not work because the generated swagger client doesn't like bytes
            # client.flows_post(f.read())
