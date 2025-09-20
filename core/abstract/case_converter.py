from abc import ABC, abstractmethod
from typing import Any, Dict, Hashable, List


class CaseConverter(ABC):
    def __init__(self, preservables: List[str] | None = None):
        self.preservables = { p.upper() for p in (preservables or []) }


    def convert(
        self,
        source: Dict[Hashable, Any],
    ) -> None:
        items = list(source.items())
        source.clear()

        for key, value in items:
            new_key = self._convert_key(key) if isinstance(key, str) else key
            if isinstance(value, dict):
                self.convert(source=value)
            source[new_key] = value


    @abstractmethod
    def _convert_key(self, key: str) -> str:
        pass
