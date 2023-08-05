from typing import Any, Dict


class CounterTypeRegistration:
    def __init__(self, *, item: Any, tags: Dict[str, Any]) -> None:
        self.item = item
        self.tags = tags
