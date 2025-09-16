import re
from core.abstract.case_converter import CaseConverter



class StartCaseConverter(CaseConverter):
    """Converts to Start Case, eg: 'Example Dict Key' """

    @staticmethod
    def _convert_key(key):
        # Split camelCase and PascalCase boundaries
        key = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', key)
        # Replace underscores and hyphens with spaces
        key = re.sub(r'[_\-]+', ' ', key)
        # Collapse multiple spaces to a single space and strip
        key = re.sub(r'\s+', ' ', key).strip()
        # Capitalize each word
        return ' '.join(word.capitalize() for word in key.split())
