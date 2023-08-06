from abc import ABC, abstractmethod
from typing import Union
from sqlalchemy.inspection import inspect


class _IntrospectorInterface(ABC):
    def __init__(self, obj) -> None:
        self.schema = obj
        self.name = obj.__tablename__

    @abstractmethod
    def primary_keys(self) -> list:
        pass

    @abstractmethod
    def unique_keys(self) -> list:
        pass

    @abstractmethod
    def foreign_keys(self, columns_only: bool = False) -> Union[list, dict]:
        pass


class _declBaseIntrospector(_IntrospectorInterface):
    def primary_keys(self, retrieve_constraint: bool = False) -> list:
        constraints = inspect(self.schema).primary_key
        if retrieve_constraint:
            return constraints
        return [c.key for c in constraints.columns]

    def unique_keys(self) -> list:
        return [
            c.name for c in self.schema.__table__.columns if any(
                [c.primary_key, c.unique]
            )
        ]

    def foreign_keys(self, columns_only: bool = False) -> Union[list, dict]:
        foreign_keys = [c for c in self.schema.c if c.foreign_keys]
        fk_names = [key.name for key in foreign_keys]
        if columns_only:
            return fk_names
        fk_targets = [
            list(key.foreign_keys)[0].target_fullname for key in foreign_keys
        ]
        return {
            name: target for name, target in zip(fk_names, fk_targets)
        }


def SQLAIntrospector(o):
    """ Factory for returning a matching introspector class """
    return _declBaseIntrospector(o)


__all__ = ["SQLAIntrospector"]
