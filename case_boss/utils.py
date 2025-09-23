from typing import Literal

from case_boss.errors import (
    ERROR_NOT_DICT,
    ERROR_UNKNOWN_CASE_TYPE,
    ERROR_WRONG_TYPE_CASE_TYPE,
)
from case_boss.types import CaseType


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
            raise ValueError(
                ERROR_UNKNOWN_CASE_TYPE.format(
                    type_=type(case), allowed=[t.value for t in CaseType]
                )
            )
    raise TypeError(ERROR_WRONG_TYPE_CASE_TYPE.format(type_=type(case).__name__))


def split_to_words(key: str) -> list[str]:
    """
    Splits a key into words, handling separators (_,-,space), camel/Pascal humps, and acronyms.
    Returns words with their original casing preserved.
    """
    words: list[str] = []
    current = ""
    for char in key:
        if char in "_- ":
            if current:
                words.append(current)
            current = ""
            continue
        if not current:
            current = char
            continue
        prev = current[-1]
        if prev.islower() and char.isupper():
            words.append(current)
            current = char
        elif prev.isupper() and char.islower() and len(current) > 1:
            words.append(current[:-1])
            current = current[-1] + char
        else:
            current += char
    if current:
        words.append(current)
    return words


def convert_key_with_separator(
    key: str,
    preserve_tokens: set[str] | None = None,
    separator: Literal["-", "_", " "] = "_",
) -> str:

    if preserve_tokens is None:
        preserve_tokens = set()

    words = split_to_words(key=key)
    words_result: list[str] = []
    for word in words:
        preserve = False
        if preserve_tokens:
            acronym = word.upper()
            preserve = acronym in preserve_tokens
        w = acronym if preserve else word.lower()
        words_result.append(w)
    return separator.join(words_result)
