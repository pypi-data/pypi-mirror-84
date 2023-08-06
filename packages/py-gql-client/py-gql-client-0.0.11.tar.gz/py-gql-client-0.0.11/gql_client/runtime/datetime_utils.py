#!/usr/bin/env python3
from dataclasses import field
from datetime import datetime

from marshmallow import fields as marshmallow_fields


DATETIME_FIELD = field(
    metadata={
        "dataclasses_json": {
            "encoder": datetime.isoformat,
            "decoder": datetime.fromisoformat,
            "mm_field": marshmallow_fields.DateTime(format="iso"),
        }
    }
)
