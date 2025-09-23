from case_boss.abstract.case_converter import CaseConverter
from case_boss.utils import convert_key_with_separator


class KebabCaseConverter(CaseConverter):
    """Converts to KebabCase, eg: 'example-dict-key'"""

    def _convert_key(self, key: str) -> str:
        return convert_key_with_separator(
            key=key, preserve_tokens=self._preserve_tokens, separator="-"
        )
