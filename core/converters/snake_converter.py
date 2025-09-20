from core.abstract.case_converter import CaseConverter
from core.utils import convert_key_with_separator



class SnakeCaseConverter(CaseConverter):
    """Converts to snake_case, eg: 'example_dict_key' """

    def _convert_key(self, key: str) -> str:
        return convert_key_with_separator(key=key, preserve_tokens=self._preserve_tokens, separator="_")
