from abc import ABC, abstractmethod
from typing import Any, Dict, Hashable


class CaseConverter(ABC):

    @classmethod
    def convert(
        cls,
        source: Dict[Hashable, Any],
        ignore_malformed: bool = False,
    ) -> None:
        items = list(source.items())
        source.clear()

        for key, value in items:
            new_key = cls._convert_key(key) if isinstance(key, str) else key
            if isinstance(value, dict):
                cls.convert(source=value, ignore_malformed=ignore_malformed)
            source[new_key] = value

    @staticmethod
    @abstractmethod
    def _convert_key(key: str) -> str:
        pass
