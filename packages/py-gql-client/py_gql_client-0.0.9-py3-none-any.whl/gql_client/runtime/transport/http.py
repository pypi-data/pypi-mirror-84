#!/usr/bin/env python3

from typing import Dict, Optional

from .transport import Transport


class HTTPTransport(Transport):
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None) -> None:
        self.url: str = url
        self.headers = headers


class HTTPException(Exception):
    def __init__(self, status_code: int, text: str) -> None:
        message = (
            f"Http request failed with status_code={status_code} and message: {text}"
        )
        super(HTTPException, self).__init__(message)
        self.status_code = status_code
        self.text = text
