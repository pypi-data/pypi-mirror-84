import datetime
import json
from typing import Any

from sqlalchemy.ext.declarative import DeclarativeMeta

from . import SQLAIntrospector


class SqlaDeclarativeEncoder(json.JSONEncoder):
    """
    A custom JSON encoder for serializing SQLAlchemy
    declarative base instances.

    Will convert datetime formats to ISO8601 compliant strings.
    """
    datetypes = (
        datetime.date,
        datetime.datetime,
        datetime.timedelta
    )

    def default(self, o: Any) -> Any:
        # Check if the class is an SQLAlchemy declarative table instance
        if isinstance(o.__class__, DeclarativeMeta):
            fields = {}
            # Get all columns of the table
            for field in [c.key for c in SQLAIntrospector(o).columns]:
                # Obtain the value of the field
                data = getattr(o, field)
                if data.__class__ in self.datetypes:
                    data = self.serialize_datetypes_to_iso(data)
                try:  # Try JSON encoding the field
                    json.dumps(data)
                    fields[field] = data
                except TypeError as exc:  # if it fails resort to failure hook
                    self.handle_failure(exc, data)
            return fields
        # If it is not an SQLAlchemy table use the default encoder
        return super(SqlaDeclarativeEncoder, self).default(o)

    # noinspection PyMethodMayBeStatic
    def serialize_datetypes_to_iso(self, v: datetypes) -> str:
        if isinstance(v, datetime.timedelta):
            return (datetime.datetime.min + v).time().isoformat()
        return v.isoformat()

    def handle_failure(self, exc: Exception, value: Any):
        """ Can be overridden to provide handling for custom fields """
        # Simply re-raise the exception by default
        raise exc


__all__ = ["SqlaDeclarativeEncoder"]
