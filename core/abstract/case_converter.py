from abc import ABC, abstractmethod
from typing import Any, Dict, Hashable, List


class CaseConverter(ABC):
    def __init__(
            self,
            preserve_tokens: List[str] | None = None, 
            exclude_keys: List[str] | None = None
        ):
        self._preserve_tokens = { p.upper() for p in (preserve_tokens or []) }
        self._exclude_keys = { p for p in (exclude_keys or []) }


    def convert(
        self,
        source: Dict[Hashable, Any],
    ) -> None:
        items = list(source.items())
        source.clear()

        for key, value in items:
            should_skip = key in self._exclude_keys
            should_convert = (not should_skip and isinstance(key, str))
            should_go_deeper = (not should_skip and isinstance(value, dict))
            
            new_key = self._convert_key(key) if should_convert else key
            if should_go_deeper:
                self.convert(source=value)
            source[new_key] = value


    @abstractmethod
    def _convert_key(self, key: str) -> str:
        pass
