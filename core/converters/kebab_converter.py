import re
from core.converters.case_converter import CaseConverter


class KebabCaseConverter(CaseConverter):

    @staticmethod
    def _convert_key(key: str) -> str:
        key = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", key)
        key = key.replace("_", "-")
        key = key.replace(" ", "-")
        return key.lower()
