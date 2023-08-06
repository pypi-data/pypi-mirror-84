import os
import pathlib
import shutil
from typing import Union, Optional, Iterable
from uuid import UUID


def get_application_root() -> str:
    return os.environ.get("PYTHONPATH").split(os.pathsep)[0]


def is_dunder(name: str) -> bool:
    if (name[:2] and name[-2:]) in ("__",):
        return True
    return False


def all_items_equal(iterable: Iterable) -> bool:
    if isinstance(iterable, (list, tuple)):
        return True if len(set(iterable)) == 1 else False
    raise TypeError("Only list and tuples may be processed")


def all_nested_zipped_equal(iterable: Iterable[Iterable]) -> bool:
    return all(
        [all_items_equal(subiter) for subiter in zip(*iterable)]
    )


def uuid4_is_valid(uuid: str) -> bool:
    try:
        val = UUID(uuid, version=4)
    except ValueError:
        return False
    return val.hex == uuid


def exclude_keys(dictionary: dict, keys: Iterable) -> dict:
    return {
        k: v for k, v in dictionary.items() if k not in keys
    }


def all_keys_present(dictionary: dict, keys: Iterable) -> bool:
    return all(k in dictionary.keys() for k in keys)


def uri_is_http(uri: str) -> bool:
    return True if uri.startswith("http") else False


class AttrDict(dict):
    __slots__ = []
    __doc__ = ""

    def __getattr__(self, item):
        return super(AttrDict, self).__getitem__(item)


class _TfvarsParser:
    def __init__(self, path: pathlib.Path) -> None:
        self.path = path

    def read(self) -> dict:
        with open(self.path, "r") as fin:
            c = fin.readlines()
        extract = lambda i: [
            el.strip() for el in [line.split("=")[i] for line in c]
        ]
        keys = extract(0)
        vals = [line[1:-1] for line in extract(1)]
        kvpairs = {k: v for k, v in zip(keys, vals)}
        return kvpairs


class Tfvars:
    def __init__(self, /, path: Union[str, pathlib.Path]) -> None:
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        if not path.exists():
            raise FileNotFoundError(f"The directory {path} does not exist")
        self.path = path
        self.vars = AttrDict(**_TfvarsParser(path).read())


# this is necessary because we can only subclass the concrete implementation
class Path(type(pathlib.Path())):
    def rmdir(self, recursive: Optional[bool] = True) -> None:
        if recursive:
            shutil.rmtree(self)
        else:
            super(Path, self).rmdir()


__all__ = [
    "is_dunder", "get_application_root", "uuid4_is_valid",
    "all_items_equal", "all_nested_zipped_equal",
    "exclude_keys", "all_keys_present", "uri_is_http",
    "AttrDict", "Tfvars", "Path"
]
