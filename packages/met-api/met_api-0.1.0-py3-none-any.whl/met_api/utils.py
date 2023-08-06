from typing import Any


def logical_xnor(a: Any, b: Any) -> bool:
    return (bool(a) or not bool(b)) and (not bool(a) or bool(b))
