import copy
import json
from typing import Any, Dict, Hashable, List, Type

from core.const import CASE_TYPE_CONVERTER_MAPPING
from core.errors import ERROR_UNKNOWN_CASE_TYPE, ERROR_INVALID_JSON
from core.abstract.case_converter import CaseConverter
from core.types import CaseType
from core.utils import normalize_type, validate_is_dict


class CaseBoss:


    def transform(
        self,
        source: Dict[Hashable, Any],
        case: CaseType,
        clone: bool = False,
        preserve_tokens: List[str] | None = None,
        exclude_keys: List[str] | None = None,
        recursion_limit: int = 0,
    ) -> Dict[Hashable, Any]:
        """
        Transforms input dict keys to specified case type.
        Non-string keys (e.g., int, tuple) are preserved unchanged.

        Args:
            source (dict): The data to process.
            type (CaseType): Target key case format (e.g., CaseType.SNAKE, CaseType.CAMEL)
            clone (bool): Will return clone, leaving original object untouched (defaults to False)
            preserve_tokens (List[str]): List of preservable strings, eg. acronyms like HTTP, ID
            exclude_keys (List[str]): Keys to skip (together with their children); excluded keys are not transformed and recursion does not descend into their values.
            recursion_limit: (int): How deep will recursion go for nested dicts, defaults to 0 (no limit),

        Returns:
            dict: The same dict object as passed (unless clone arg is set to True),
            but with string keys transformed to the specified case.

        Raises:
            ValueError: If data is invalid.
        """

        validate_is_dict(source=source)
        case = normalize_type(case=case)

        if clone:
            source = copy.deepcopy(source)

        converter_cls: Type[CaseConverter] = CASE_TYPE_CONVERTER_MAPPING.get(case.value, None)
        if not converter_cls:
            raise ValueError(ERROR_UNKNOWN_CASE_TYPE.format(type_=type(case).__name__, allowed=[t.value for t in CaseType]))

        converter: CaseConverter = converter_cls(
            preserve_tokens=preserve_tokens, 
            exclude_keys=exclude_keys,
            recursion_limit=recursion_limit)
        converter.convert(source=source)

        return source


    def transform_from_json(
            self, source: str, 
            case: CaseType, 
            preserve_tokens: List[str] | None = None,
            exclude_keys: List[str] | None = None,
            recursion_limit: int = 0,
        ) -> str:
        """
        Transforms input JSON keys to specified case-type, and returns the result as a JSON string.

        Args:
            source (str): The data to process.
            type (CaseType): Target key case format (e.g., CaseType.SNAKE, CaseType.CAMEL)
            preserve_tokens (List[str]): List of preservable strings, eg. acronyms like HTTP, ID
            exclude_keys (List[str]): Keys to skip (together with their children); excluded keys are not transformed and recursion does not descend into their values.
            recursion_limit: (int): How deep will recursion go for nested dicts, defaults to 0 (no limit),

        Returns:
            str: A JSON string with all string keys transformed to the specified case

        Raises:
            ValueError: If the input is not valid JSON or contains invalid data.
            json.JSONDecodeError: If the input string is not valid JSON.
        """

        case = normalize_type(case=case)

        try:
            data = json.loads(source)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(ERROR_INVALID_JSON.format(msg=e.msg), e.doc, e.pos) from e

        return  json.dumps(self.transform(
            source=data, 
            case=case, 
            preserve_tokens=preserve_tokens, 
            exclude_keys=exclude_keys,
            recursion_limit=recursion_limit))
