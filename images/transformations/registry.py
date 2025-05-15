from typing import Dict

from .transformation_abstract import Transformation

_registry: Dict[str, Transformation] = {}


def register_transform(cls):
    """
    Class decorator: Instantiates cls, grabs its .key(),
    and stores the instance in registry dict under that key.
    """
    inst = cls()
    key = inst.key()
    if key in _registry:
        raise RuntimeError(f"Duplicate transform key: {key!r}")
    _registry[key] = inst
    return cls


def get_transform_map() -> Dict[str, Transformation]:
    """Return a fresh dict of key → instance."""
    return dict(_registry)
