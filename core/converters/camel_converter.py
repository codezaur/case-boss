import re
from core.abstract.case_converter import CaseConverter
from core.utils import split_to_words



class CamelCaseConverter(CaseConverter):
    """Converts to camelCase, eg: 'exampleDictKey' """

    def _convert_key(self, key: str):
        words = split_to_words(key=key)
        words_result = ""

        for i, word in enumerate(words):
            preserve = False
            if self.preservables:
                acronym = word.upper()
                preserve = acronym in self.preservables 
            word = word.capitalize() if i > 0 else word.lower()
            w = acronym if preserve else word
            words_result += w
        return words_result
