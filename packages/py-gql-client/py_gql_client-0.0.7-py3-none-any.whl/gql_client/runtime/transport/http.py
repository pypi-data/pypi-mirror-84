#!/usr/bin/env python3

from typing import Dict, Optional

from http import HTTPStatus
from .transport import Transport


class HTTPTransport(Transport):
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None) -> None:
        self.url: str = url
        self.headers = headers


class HttpException(Exception):
    def __init__(self, status_code: HTTPStatus, text: str) -> None:
        message = (
            f"Http request failed with status_code={status_code} and message: {text}"
        )
        super(HttpException, self).__init__(message)
        self.status_code = status_code
        self.text = text
