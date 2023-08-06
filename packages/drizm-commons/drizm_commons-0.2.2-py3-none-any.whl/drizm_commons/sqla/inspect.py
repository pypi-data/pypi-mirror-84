from abc import ABC, abstractmethod
from inspect import isclass
from typing import Union

from sqlalchemy import Table
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.orm.util import class_mapper


def is_mapped_class(cls) -> bool:
    if not isclass(cls):
        return False
    try:
        class_mapper(cls)
    except UnmappedClassError:
        return False
    else:
        return True


class _IntrospectorInterface(ABC):
    tablename: str
    columns: dict
    __table__: Table

    def __init__(self, obj) -> None:
        self.schema = obj

    @property
    @abstractmethod
    def classname(self):
        pass

    def primary_keys(self, retrieve_constraint: bool = False) -> list:
        constraints = inspect(self.__table__).primary_key
        if retrieve_constraint:
            return constraints
        return [c.key for c in constraints.columns]

    def unique_keys(self) -> list:
        return [
            c.name for c in self.columns if any(
                [c.primary_key, c.unique]
            )
        ]

    def foreign_keys(self, columns_only: bool = False) -> Union[list, dict]:
        foreign_keys = [c for c in self.columns if c.foreign_keys]
        fk_names = [key.name for key in foreign_keys]
        if columns_only:
            return fk_names
        fk_targets = [
            list(key.foreign_keys)[0].target_fullname for key in foreign_keys
        ]
        return {
            name: target for name, target in zip(fk_names, fk_targets)
        }


class _declBaseIntrospector(_IntrospectorInterface):
    """
    Inspect Declarative Base class instances.
    These are objects you may get back when querying,
    using a Session or when constructing an instance yourself
    """
    def __init__(self, obj) -> None:
        super().__init__(obj)
        self.tablename = obj.__tablename__
        self.columns = obj.__table__.c
        self.__table__ = obj.__table__

    @property
    def classname(self) -> str:
        return self.schema.__class__.__name__


class _declClassIntrospector(_IntrospectorInterface):
    def __init__(self, obj) -> None:
        super().__init__(obj)
        self.tablename = obj.__tablename__
        self.columns = obj.__table__.c
        self.__table__ = obj.__table__

    @property
    def classname(self) -> str:
        return self.schema.__name__


class _tblIntrospector(_IntrospectorInterface):
    def __init__(self, obj: Table) -> None:
        super().__init__(obj)
        self.tablename = obj.name
        self.columns = obj.c  # noqa false-positive write only property
        self.__table__ = obj

    @property
    def classname(self):
        raise NotImplementedError(
            f"Class {self.__class__.__name__} does not support "
            f"declarative base features"
        )


def SQLAIntrospector(o):
    """ Factory returning a matching introspector class """
    err_msg = "Class of type {0} is not supported for introspection"
    if isinstance(o, Table):
        return _tblIntrospector(o)

    if isclass(o):
        if is_mapped_class(o):
            return _declClassIntrospector(o)
        raise TypeError(err_msg.format(type(o)))
    else:
        if is_mapped_class(o.__class__):
            return _declBaseIntrospector(o)
        raise TypeError(err_msg.format(type(o.__class__)))


__all__ = ["SQLAIntrospector", "is_mapped_class"]
