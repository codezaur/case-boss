from case_boss.abstract.case_converter import CaseConverter
from case_boss.utils import split_to_words


class PascalCaseConverter(CaseConverter):
    """Converts to PascalCase, eg: 'ExampleDictKey'"""

    def _convert_key(self, key: str) -> str:
        words = split_to_words(key=key)
        words_result = ""

        for word in words:
            preserve = False
            if self._preserve_tokens:
                acronym = word.upper()
                preserve = acronym in self._preserve_tokens
            w = acronym if preserve else word.capitalize()
            words_result += w
        return words_result
