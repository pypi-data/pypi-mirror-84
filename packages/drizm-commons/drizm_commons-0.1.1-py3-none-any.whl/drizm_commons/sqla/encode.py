import json
from typing import Any

from sqlalchemy.ext.declarative import DeclarativeMeta
from ..utils import is_dunder


class AlchemyEncoder(json.JSONEncoder):
    """
    A custom JSON encoder for working with SQLAlchemy
    declarative base instances.
    """

    def default(self, o: Any) -> Any:
        # Check if the class is an SQLAlchemy declarative table instance
        if isinstance(o.__class__, DeclarativeMeta):
            fields = {}
            # Get all columns of the table
            for field in [
                f for f in dir(o) if not is_dunder(f) and f != "metadata"
            ]:
                # Obtain the value of the field
                data = getattr(o, field)
                try:  # Try JSON encoding the field
                    json.dumps(data)
                    fields[field] = data
                except TypeError as exc:  # if it fails resort to failure hook
                    self.handle_failure(exc, data)
            return fields

        # If it is not an SQLAlchemy table use the default encoder
        return super(AlchemyEncoder, self).default(o)

    def handle_failure(self, exc: Exception, value: Any):
        """ Can be overridden to provide handling for custom fields """
        # Simply re-raise the exception by default
        raise exc
