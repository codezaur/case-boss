import re
from core.abstract.case_converter import CaseConverter



class CamelCaseConverter(CaseConverter):
    """Converts to camelCase, eg: 'exampleDictKey' """

    @staticmethod
    def _convert_key(key):
        # Split on underscores, hyphens, spaces, and camelCase boundaries
        key = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', key)
        key = re.sub(r'[_\- ]+', ' ', key)
        words = key.split()
        if not words:
            return ''
        # Lowercase first word, capitalize the rest
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
