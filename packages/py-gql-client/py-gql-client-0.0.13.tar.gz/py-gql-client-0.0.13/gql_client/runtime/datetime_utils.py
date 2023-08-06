#!/usr/bin/env python3
from typing import Optional

from dataclasses import field
from datetime import datetime, timedelta, tzinfo

from marshmallow import fields as marshmallow_fields


class simple_utc(tzinfo):
    def tzname(self, dt: Optional[datetime]) -> Optional[str]:
        return "UTC"

    def utcoffset(self, dt: Optional[datetime]) -> Optional[timedelta]:
        return timedelta(0)


def isoformat(time: datetime) -> str:
    return datetime.isoformat(time.replace(tzinfo=simple_utc()))


DATETIME_FIELD = field(
    metadata={
        "dataclasses_json": {
            "encoder": isoformat,
            "decoder": datetime.fromisoformat,
            "mm_field": marshmallow_fields.DateTime(format="iso"),
        }
    }
)
