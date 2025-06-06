

from collections.abc import Callable
from typing import IO, Any, TypeVar

def name(name: str) -> Callable[..., Callable[..., Any]]:
    """
    Set the name of a test case.
    """

    T = TypeVar("T")

    def decorator(f: Callable[..., T]) -> Callable[..., T]:
        f.__dict__["name"] = name
        return f

    return decorator


def points(points: float) -> Callable[..., Callable[..., Any]]:
    """
    Set the number of points that a test case should award.
    """
    T = TypeVar("T")

    def decorator(f: Callable[..., T]) -> Callable[..., T]:
        f.__dict__["points"] = points
        return f

    return decorator

def not_repeated():
    pass