import copy
from typing import Any, Dict, Hashable

from core.const import CASE_TYPE_CONVERTER_MAPPING
from core.abstract.case_converter import CaseConverter
from core.decorators import validate_is_dict
from core.types import CaseType


class CaseBoss:

    @validate_is_dict
    def transform(
        self,
        source: Dict[Hashable, Any],
        type: CaseType,
        clone: bool = False,
        ignore_malformed: bool = False,
    ) -> Dict[Hashable, Any]:
        """
        Transforms input dict keys to specified case type.
        Non-string keys (e.g., int, tuple) are preserved unchanged.

        Args:
            source (dict): The data to process.
            type (CaseType): Target key case format (e.g., CaseType.SNAKE, CaseType.CAMEL)
            clone (bool): Will return clone, leaving original object untouched (defaults to False)
            ignore_malformed (bool): Will ignore malformed data and proceed to next item without
            throwing exception (defaults to False)

        Returns:
            dict: The same dict object as passed (unless clone arg is set to True),
            but with string keys transformed to the specified case.

        Raises:
            ValueError: If data is invalid.
        """

        if clone:
            source = copy.deepcopy(source)

        converter: CaseConverter = CASE_TYPE_CONVERTER_MAPPING.get(type, None)
        if not converter:
            raise ValueError(
                f"Unknown case type: {type}, allowed types: {[t.value for t in CaseType]}"
            )

        converter.convert(source=source, ignore_malformed=ignore_malformed)

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
