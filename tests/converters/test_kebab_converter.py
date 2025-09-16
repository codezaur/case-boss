import pytest
from core.converters.kebab_converter import KebabCaseConverter


@pytest.mark.parametrize("input_str,expected", [
    ("exampleDictKey", "example-dict-key"),
    ("Example_Dict_Key", "example-dict-key"),
    ("example-dict-key", "example-dict-key"),
    ("example dict key", "example-dict-key"),
    ("", ""),
])
def test_kebab_case_converter(input_str, expected):
    assert KebabCaseConverter._convert_key(input_str) == expected


def test_simple_flat_dict():
    data = {"simpleKey": 1, "another_key": 2, "with space": 3}
    KebabCaseConverter.convert(source=data)
    assert data == {"simple-key": 1, "another-key": 2, "with-space": 3}


def test_nested_dict():
    data = {"outerKey": {"inner_key": 5, "InnerCamel": 6}}
    KebabCaseConverter.convert(source=data)
    assert data == {"outer-key": {"inner-key": 5, "inner-camel": 6}}


def test_non_string_keys():
    data = {1: "a", "normalKey": "b"}
    KebabCaseConverter.convert(source=data)
    assert data == {1: "a", "normal-key": "b"}


def test_empty_dict():
    data = {}
    KebabCaseConverter.convert(source=data)
    assert data == {}


def test_multiple_formats():
    data = {"snake_caseKey": 1, "CamelCaseKey": 2, "with space_key": 3}
    KebabCaseConverter.convert(source=data)
    assert data == {"snake-case-key": 1, "camel-case-key": 2, "with-space-key": 3}


def test_value_none():
    data = {"normalItem": 1, "noneItem": None}
    KebabCaseConverter.convert(source=data)
    assert data == {"normal-item": 1, "none-item": None}
