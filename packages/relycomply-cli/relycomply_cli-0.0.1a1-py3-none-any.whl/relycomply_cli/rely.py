import json
import sys
import textwrap
from base64 import b64encode
from pathlib import Path

import toml
from gql import gql
from graphql.error.syntax_error import GraphQLSyntaxError
from graphql.type.definition import (
    GraphQLEnumType,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLScalarType,
)
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import TOMLLexer
from tabulate import tabulate
from termcolor import cprint

from . import cleartoml
from .generate_gql import filter_list_fields, generate_endpoint
from .helpers import first_value


class CliException(Exception):
    """
    Exceptions thrown by the CLI
    """


gql_folder = Path(__file__).parent / "gql"


def pluralise_type(type):
    return type[0].lower() + type[1:] + "s"


def format_toml(value):
    return cleartoml.dumps(value)


def cell_output_for_table(value):
    if isinstance(value, dict):
        return json.dumps(value, indent=2)
    elif isinstance(value, list):
        return "\n".join(["- " + cell_output_for_table(child) for child in value])
    else:
        return "\n".join(textwrap.wrap(str(value), 40))


def collapse_edges(value):

    if isinstance(value, list):
        return [collapse_edges(child) for child in value]

    if isinstance(value, dict):
        replacement = {}
        for key, child in value.items():

            if (
                isinstance(child, dict)
                and len(child) == 1
                and "edges" in child
                and isinstance(child["edges"], list)
            ):
                replacement[key] = [
                    collapse_edges(edge["node"]) for edge in child["edges"]
                ]
            else:
                replacement[key] = collapse_edges(child)
        return replacement
    else:
        return value


def format_for_terminal(value):
    code = format_toml(collapse_edges(value))
    if sys.stdout.isatty():
        return highlight(code, TOMLLexer(), TerminalFormatter())
    else:
        return code


def format_table_for_terminal(nodes):
    nodes = collapse_edges(nodes)
    if nodes:
        columns = nodes[0].keys()
        headers = [key.replace(".", "\n") for key in columns]
        rows = [
            [cell_output_for_table(node.get(key)) for key in columns] for node in nodes
        ]
        return tabulate(rows, headers=headers, tablefmt="fancy_grid")

    else:
        return f"No matching items"


class Rely:
    def __init__(self, client, typ, action, filename=None, **kwargs):
        self.client = client
        self.type = typ
        self.action = action
        self.filename = filename
        self.kwargs = kwargs

    def act(self):
        if self.type.lower() == "mutation":
            return self.general_mutation()
        elif self.action == "retrieve":
            return self.retrieve()
        elif self.action == "list":
            return self.list()
        elif self.action == "template":
            return self.template()
        elif self.action == "delete":
            return self.delete()
        else:
            return self.crud_mutation()

    def _execute(self, graphql, operation_name, wrap_variables=False):
        try:
            query = gql(graphql)
        except GraphQLSyntaxError:
            output_error("[Bad GraphQL Error]")
            output_error(graphql)
            sys.exit(1)

        variable_values = self.kwargs
        if self.filename:
            with open(self.filename) as f:
                variable_values = {**toml.load(f), **variable_values}

        for key in list(variable_values):
            if key[0] == "@":
                new_key = key[1:]
                value = variable_values.pop(key)
                with open(value, "rb") as f:
                    new_value = b64encode(f.read()).decode("ascii")
                variable_values[new_key] = new_value

        if wrap_variables:
            variable_values = {"input": variable_values}

        return self.client.execute(
            query, operation_name=operation_name, variable_values=variable_values
        )

    def get_type_mutation_name(self):

        with open(gql_folder / "aliases.toml") as f:
            alias_mappings = toml.load(f)

        mutations = self.client.schema.mutation_type.fields

        aliases = [
            *(
                (alias_action + alias_type, mutation_name)
                for alias_type, alias_actions in alias_mappings.items()
                for alias_action, mutation_name in alias_actions.items()
            ),
            *((mutation_name, mutation_name) for mutation_name in mutations.keys()),
        ]

        given_name = (self.action + self.type).lower()
        for alias, mutation_name in aliases:
            if alias.lower() == given_name:
                return mutation_name

        possible_actions = [
            mutation_name[: -len(self.type.lower())]
            for _, mutation_name in aliases
            if mutation_name.lower().endswith(self.type.lower())
        ]

        if possible_actions:
            message = f"Action '{self.action}' not recognised for type '{self.type}', possible actions are:\n"
            raise CliException(
                message + "\n".join([f"  - {action}" for action in possible_actions])
            )
        else:
            raise CliException(f"Type '{self.type}' is not recognised")

    def get_query_name_and_type(self):
        plural_name_lower = pluralise_type(self.type).lower()
        query_keys = {
            key: value for key, value in self.client.schema.query_type.fields.items()
        }

        plural_name = None
        for query_key, field in query_keys.items():
            if plural_name_lower == query_key.lower():
                query_type = (
                    field.type.fields["edges"].type.of_type.of_type.fields["node"].type
                )
                return query_key, query_type.name

        if not plural_name:
            raise CliException(f"Query type '{self.type}' not recognised.")

    def crud_mutation(self):

        operation_name = self.get_type_mutation_name()

        graphql = generate_endpoint("mutation", self.client, operation_name)

        gql_result = self._execute(graphql, operation_name, wrap_variables=True)

        result = gql_result[operation_name]

        return first_value(result)

    def general_mutation(self):
        graphql = generate_endpoint("mutation", self.client, self.action)
        gql_result = self._execute(graphql, self.action, wrap_variables=True)
        return first_value(first_value(gql_result))

    def retrieve(self):
        query_key, _ = self.get_query_name_and_type()
        graphql = generate_endpoint("retrieve", self.client, query_key)
        gql_result = self._execute(graphql, query_key)
        result = first_value(gql_result)

        edges = result["edges"]

        if len(edges) == 1:
            return edges[0]["node"]
        elif len(edges) == 0:
            raise CliException(f"No matching {self.type} found")
        else:
            raise CliException(f"Multiple matching {self.type} items found")

    def list(self):
        query_key, query_type = self.get_query_name_and_type()
        graphql = generate_endpoint("list", self.client, query_key)
        gql_result = self._execute(graphql, query_key)
        result = first_value(gql_result)
        return filter_list_fields(result, query_type)

    def delete(self):
        graphql = f"""
        mutation delete($id: ID!) {{
            delete{self.type}(input:{{
                id: $id
            }}) {{
                ok
            }}
        }}
        """
        return self._execute(graphql, "delete")

    def template(self):
        payload = (
            self.client.schema.mutation_type.fields["create" + self.type]
            .args["input"]
            .type.of_type
        )
        template = gql_type_to_template(payload)
        del template["clientMutationId"]

        if self.filename:
            with open(self.filename, "w") as f:
                output = format_toml(template)
                f.write(output)
        return template


def gql_type_to_template(obj):
    if isinstance(obj, GraphQLInputObjectType):
        return {k: gql_type_to_template(v) for k, v in obj.fields.items()}
    elif isinstance(obj, GraphQLInputField):
        return gql_type_to_template(obj.type)
    elif isinstance(obj, GraphQLList):
        return [gql_type_to_template(obj.of_type)]
    elif isinstance(obj, GraphQLNonNull):
        return gql_type_to_template(obj.of_type)
    elif isinstance(obj, GraphQLScalarType):
        return obj.name
    elif isinstance(obj, GraphQLEnumType):
        return "|".join([value for value in obj.values])
    else:
        raise CliException(f"Unknown type to template {obj}")


def output_error(message):
    cprint(message, "red", file=sys.stderr)
