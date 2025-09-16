import re
from core.abstract.case_converter import CaseConverter



class PascalCaseConverter(CaseConverter):
    """Converts to PascalCase, eg: 'ExampleDictKey' """

    @staticmethod
    def _convert_key(key: str) -> str:
        # Split on underscores, hyphens, spaces, and camelCase boundaries
        key = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', key)
        key = re.sub(r'[_\- ]+', ' ', key)
        words = key.split()
        return ''.join(word.capitalize() for word in words)
