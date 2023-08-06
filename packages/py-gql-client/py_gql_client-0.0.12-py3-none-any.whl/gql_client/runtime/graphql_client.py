#!/usr/bin/env python3

from typing import Any, Dict, Optional, Union

from gql import gql, Client
from dataclasses_json import DataClassJsonMixin
from datetime import datetime, timedelta, tzinfo
from enum import Enum

from .reporter import DUMMY_REPORTER, Reporter


class simple_utc(tzinfo):
    def tzname(self, dt: Optional[datetime]) -> Optional[str]:
        return "UTC"

    def utcoffset(self, dt: Optional[datetime]) -> Optional[timedelta]:
        return timedelta(0)


class MissingEnumException(Exception):
    def __init__(self, variable: Enum) -> None:
        self.enum_type = str(type(variable))

    def __str__(self) -> str:
        return f"Try to encode missing value of enum {self.enum_type}"


def encode_value(
    value: Union[DataClassJsonMixin, datetime, Enum]
) -> Union[Dict[str, Any], str]:
    if isinstance(value, DataClassJsonMixin):
        return encode_variables(value.to_dict())
    elif isinstance(value, datetime):
        return datetime.isoformat(value.replace(tzinfo=simple_utc()))
    elif isinstance(value, Enum):
        if value.value == "":
            raise MissingEnumException(value)
        return value.value
    return value


def encode_variables(variables: Dict[str, Any]) -> Dict[str, Any]:
    new_variables: Dict[str, Any] = {}
    for key, value in variables.items():
        if (
            isinstance(value, DataClassJsonMixin)
            or isinstance(value, datetime)
            or isinstance(value, Enum)
        ):
            new_variables[key] = encode_value(value)
        elif isinstance(value, list):
            new_list = []
            for val in value:
                if (
                    isinstance(val, DataClassJsonMixin)
                    or isinstance(val, datetime)
                    or isinstance(val, Enum)
                ):
                    new_list.append(encode_value(val))
                else:
                    new_list.append(val)
            new_variables[key] = new_list
        else:
            new_variables[key] = value
    return new_variables


class GraphqlClient:
    def __init__(
        self,
        client: Client,
        reporter: Reporter = DUMMY_REPORTER,
    ) -> None:

        """This is the class to use for working with graphql server

        Args:
            client (Client): Graphql client
            reporter (Reporter, optional): Use reporter.InventoryReporter to
                       store reports on all successful and failed mutations
                       in inventory. The default is DummyReporter that
                       discards reports

        """

        self.client = client
        self.reporter = reporter

    def call(self, query: str, variables: Dict[str, Any]) -> str:
        new_variables = encode_variables(variables)
        return self.client.execute(gql(query), variable_values=new_variables)
