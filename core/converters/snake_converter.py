import re
from core.abstract.case_converter import CaseConverter



class SnakeCaseConverter(CaseConverter):
    """Converts to snake_case, eg: 'example_dict_key' """

    @staticmethod
    def _convert_key(key: str) -> str:
        # Split camelCase and PascalCase boundaries
        key = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', key)
        # Replace hyphens and spaces with underscores
        key = re.sub(r'[- ]+', '_', key)
        # Replace multiple underscores with a single underscore
        key = re.sub(r'_+', '_', key)
        return key.lower()
