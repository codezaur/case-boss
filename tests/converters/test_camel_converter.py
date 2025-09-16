import pytest
from core.converters.camel_converter import CamelCaseConverter

@pytest.mark.parametrize("input_str,expected", [
    ("example_dict_key", "exampleDictKey"),
    ("Example Dict Key", "exampleDictKey"),
    ("example-dict-key", "exampleDictKey"),
    ("exampleDictKey", "exampleDictKey"),
    ("", ""),
])
def test_camel_case_converter(input_str, expected):
    assert CamelCaseConverter._convert_key(input_str) == expected

def test_simple_flat_dict():
    data = {"simple_key": 1, "another-key": 2, "with space": 3}
    CamelCaseConverter.convert(source=data)
    assert data == {"simpleKey": 1, "anotherKey": 2, "withSpace": 3}

def test_nested_dict():
    data = {"outer_key": {"inner-key": 5, "Inner Space": 6}}
    CamelCaseConverter.convert(source=data)
    assert data == {"outerKey": {"innerKey": 5, "innerSpace": 6}}

def test_non_string_keys():
    data = {1: "a", "normal_key": "b"}
    CamelCaseConverter.convert(source=data)
    assert data == {1: "a", "normalKey": "b"}

def test_empty_dict():
    data = {}
    CamelCaseConverter.convert(source=data)
    assert data == {}

def test_multiple_formats():
    data = {"snake_case-key": 1, "PascalCaseKey": 2, "with space_key": 3}
    CamelCaseConverter.convert(source=data)
    assert data == {"snakeCaseKey": 1, "pascalCaseKey": 2, "withSpaceKey": 3}

def test_value_none():
    data = {"normal_item": 1, "none_item": None}
    CamelCaseConverter.convert(source=data)
    assert data == {"normalItem": 1, "noneItem": None}
