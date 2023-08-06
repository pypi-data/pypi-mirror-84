from typing import Any, Dict, Generic, TypeVar

T = TypeVar("T")


class CounterTypeRegistration(Generic[T]):
    def __init__(self, *, item: T, tags: Dict[str, Any]) -> None:
        self.item = item
        self.tags = tags
