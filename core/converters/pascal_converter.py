import re
from core.abstract.case_converter import CaseConverter
from core.utils import split_to_words



class PascalCaseConverter(CaseConverter):
    """Converts to PascalCase, eg: 'ExampleDictKey' """

    def _convert_key(self, key: str) -> str:
        words = split_to_words(key=key)
        words_result = ""

        for word in words:
            preserve = False
            if self.preservables:
                acronym = word.upper()
                preserve = acronym in self.preservables
            w = acronym if preserve else word.capitalize()
            words_result += w
        return words_result