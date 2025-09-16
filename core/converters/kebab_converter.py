import re

from core.abstract.case_converter import CaseConverter


class KebabCaseConverter(CaseConverter):
    """Converts to KebabCase, eg: 'example-dict-key' """

    @staticmethod
    def _convert_key(key: str) -> str:
        key = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", key)
        key = key.replace("_", "-")
        key = key.replace(" ", "-")
        return key.lower()
