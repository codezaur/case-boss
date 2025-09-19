from core.errors import ERROR_NOT_DICT, ERROR_UNKNOWN_CASE_TYPE, ERROR_WRONG_TYPE_CASE_TYPE
from core.types import CaseType


def validate_is_dict(source) -> None:
    if not isinstance(source, dict):
      raise ValueError(ERROR_NOT_DICT.format(type_=type(source).__name__))


def normalize_type(case: CaseType | str) -> CaseType:
    """
    Normalize a case type input to a CaseType enum member.

    Accepts either a CaseType enum member or a string (e.g., "snake", "camel").
    Returns the corresponding CaseType enum.

    Args:
        type_input (CaseType | str): Input case format. Must be a CaseType member or valid string value.

    Returns:
        CaseType: The normalized enum member.

    Raises:
        ValueError: If the input is neither a valid CaseType nor a recognized string.
    """
    if isinstance(case, CaseType):
        return case
    if isinstance(case, str):
        try:
            return CaseType(case)
        except ValueError:
            raise ValueError(ERROR_UNKNOWN_CASE_TYPE.format(type_=type(case), allowed=[t.value for t in CaseType]))
    raise TypeError(ERROR_WRONG_TYPE_CASE_TYPE.format(type_= type(case).__name__))
