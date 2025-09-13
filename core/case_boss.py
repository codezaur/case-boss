from typing import Any, Dict, Hashable
from core.types import CaseType


class CaseBoss:

    def transform(
        self, source: Dict[Hashable, Any], type: CaseType
    ) -> Dict[Hashable, Any]:
        """
        Transforms input dict keys to specified case type.
        Non-string keys (e.g., int, tuple, Enum) are preserved unchanged.

        Args:
            source (dict): The data to process.
            type (CaseType): Target key case format (e.g., CaseType.SNAKE, CaseType.CAMEL)

        Returns:
            dict: The same dict object as passed, but with string keys transformed to the specified case

        Raises:
            ValueError: If data is invalid.
        """
        return source

    def transform_from_json(self, source: str, type: CaseType) -> str:
        """
        Transforms input JSON keys to specified case-type, and returns the result as a JSON string.

        Args:
            source (str): The data to process.
            type (CaseType): Target key case format (e.g., CaseType.SNAKE, CaseType.CAMEL)

        Returns:
            str: A JSON string with all string keys transformed to the specified case

        Raises:
            ValueError: If the input is not valid JSON or contains invalid data.
            json.JSONDecodeError: If the input string is not valid JSON.
        """
        # try:
        #     config = json.loads(source)
        # except json.JSONDecodeError as e:
        #     raise json.JSONDecodeError(
        #         f"Invalid JSON provided to transform_from_json: {e.msg}",
        #         e.doc,
        #         e.pos,
        #     ) from e
        # return self.transform(config)
        return source
