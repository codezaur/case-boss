import re
from core.abstract.case_converter import CaseConverter
from core.utils import split_to_words



class StartCaseConverter(CaseConverter):
    """Converts to Start Case, eg: 'Example Dict Key' """

    def _convert_key(self, key: str):
        words = split_to_words(key=key)
        words_result: list[str] = []
        for word in words:
            preserve = False
            if self._preserve_tokens:
                acronym = word.upper()
                preserve = acronym in self._preserve_tokens 
            w = acronym if preserve else word.capitalize()
            words_result.append(w)
        return " ".join(words_result)