import os
import sys

import click
import requests

from ..helpers.global_options import GlobalOptions
from ..helpers.login.token import get_auth_header
from .symflow import symflow


@symflow.command("get", short_help="Get a resource via Sym API")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument("resource_type", type=click.Choice(["flow"]))
@click.argument("resource_id")
@click.argument("dest_proto_file")
def get(
    options: GlobalOptions, resource_type: str, resource_id: str, dest_proto_file: str
) -> None:
    if resource_type == "flow":
        if not os.path.exists(dest_proto_file):
            print(f"dest_proto_file ({dest_proto_file}) does not exist", file=sys.stderr)
            sys.exit(1)
        with open(dest_proto_file, "wb") as f:
            res = requests.get(
                f"{options.api_url}/v1/flows/{resource_id}",
                headers={
                    "Content-Type": "application/x-protobuf",
                    "accept": "application/x-protobuf",
                    "Authorization": get_auth_header(),
                },
                stream=True,
            )
            f.write(res.raw.read())
            if res.ok:
                print(f"Got {resource_type} with id {resource_id}", file=sys.stderr)
            else:
                print(
                    f"Failed to get {resource_type} with id {resource_id}",
                    file=sys.stderr,
                )
                print(res.text, file=sys.stderr)
                sys.exit(2)
