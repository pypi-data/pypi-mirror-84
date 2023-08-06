#!/usr/bin/env python3

from dataclasses import field
from enum import Enum
from functools import partial
from typing import Type


class MissingEnumException(Exception):
    def __init__(self, variable: Enum) -> None:
        self.enum_type = str(type(variable))

    def __str__(self) -> str:
        return f"Try to encode missing value of enum {self.enum_type}"


def enum_field(enum_type: Type[Enum]):
    def encode_enum(value: Enum) -> str:
        if value.value == "":
            raise MissingEnumException(value)
        return value.value

    def decode_enum(t: Type[Enum], value: str) -> Enum:
        return t(value)

    return field(
        metadata={
            "dataclasses_json": {
                "encoder": encode_enum,
                "decoder": partial(decode_enum, enum_type),
            }
        }
    )
