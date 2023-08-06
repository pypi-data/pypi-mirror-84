import argparse
import sys
from pathlib import Path

import requests
import toml

from gql import Client
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport

from .rely import (
    Rely,
    format_for_terminal,
    format_table_for_terminal,
    output_error,
    CliException,
)


def check_auth(email, password, url, impersonate):
    pass


class GqlClientConnectionError(Exception):
    def __init__(self, body):
        super().__init__(body["errors"][0]["message"])
        self.body = body


def gql_client(email, password, url, impersonate):
    transport = RequestsHTTPTransport(
        url=url,
        verify=True,
        retries=3,
        auth=(email, password),
        headers={"IMPERSONATE": impersonate},
    )
    try:
        return Client(transport=transport, fetch_schema_from_transport=True)
    except TypeError:
        # Probably an authorisation error
        response = requests.post(
            url, auth=(email, password), headers={"IMPERSONATE": impersonate}
        )

        try:
            body = response.json()
        except:
            body = {
                "errors": [
                    {"message": f"Unknown error, status code {response.status_code}"}
                ]
            }

        raise GqlClientConnectionError(body)


def main():

    # Lookup config from config file
    config = {}

    folders = [Path(".").resolve()]
    while folders[-1] != Path("/"):
        folders.append(folders[-1].parent)

    for folder in folders:
        config_path = folder / ".rely.toml"
        if config_path.exists():
            with open(config_path, "r") as f:
                config = toml.load(f)
            break

    parser = argparse.ArgumentParser()
    parser.add_argument("type")
    parser.add_argument("action")
    parser.add_argument("--auth", default=config.get("auth"))
    parser.add_argument("--host", default=config.get("host"))
    parser.add_argument("--impersonate", default=config.get("impersonate"))

    # TODO: Implement this
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--toml", action="store_true")
    group.add_argument("--json", action="store_true")
    group.add_argument("--yaml", action="store_true")
    group.add_argument("--csv", action="store_true")

    set_args, other_args = parser.parse_known_args()

    try:

        try:
            client = gql_client(
                *set_args.auth.split(":"),
                url=set_args.host,
                impersonate=set_args.impersonate,
            )
        except GqlClientConnectionError as e:
            raise CliException(str(e))

        action = set_args.action

        kwargs = [part for part in other_args if part.startswith("--")]

        try:
            kwargs = dict(part[2:].split("=", 1) for part in kwargs)
        except ValueError:
            raise CliException(
                "Keyword arguments must be of the form '--<key>=<value>'."
            )

        straight_args = [part for part in other_args if not part.startswith("--")]

        if not straight_args:
            filename = None
        elif len(straight_args) == 1:
            filename = straight_args[0]
        else:
            raise CliException("Too many input filename arguments")

        kwargs["filename"] = filename

        if action == "list":
            output = format_table_for_terminal
        else:
            output = format_for_terminal

        result = Rely(client, set_args.type, action, **kwargs).act()

        print(output(result))

    except TransportQueryError as e:
        output_error("[Error]")
        packet = eval(str(e))
        output_error(packet["message"])
        exit(1)

    except CliException as e:
        output_error("[Command Line Exception]")
        output_error(e)
        exit(1)


if __name__ == "__main__":
    main()
