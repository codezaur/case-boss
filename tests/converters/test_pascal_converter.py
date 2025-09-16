from core.converters.pascal_converter import PascalCaseConverter
import pytest


@pytest.mark.parametrize("input_str,expected", [
    ("example_dict_key", "ExampleDictKey"),
    ("Example Dict Key", "ExampleDictKey"),
    ("example-dict-key", "ExampleDictKey"),
    ("exampleDictKey", "ExampleDictKey"),
    ("", ""),
])
def test_pascal_case_converter(input_str, expected):
    assert PascalCaseConverter._convert_key(input_str) == expected

def test_simple_flat_dict():
    data = {"simpleKey": 1, "another_key": 2, "with space": 3}
    PascalCaseConverter.convert(source=data)
    assert data == {"SimpleKey": 1, "AnotherKey": 2, "WithSpace": 3}

def test_nested_dict():
    data = {"outerKey": {"inner_key": 5, "InnerCamel": 6}}
    PascalCaseConverter.convert(source=data)
    assert data == {"OuterKey": {"InnerKey": 5, "InnerCamel": 6}}

def test_non_string_keys():
    data = {1: "a", "normalKey": "b"}
    PascalCaseConverter.convert(source=data)
    assert data == {1: "a", "NormalKey": "b"}

def test_empty_dict():
    data = {}
    PascalCaseConverter.convert(source=data)
    assert data == {}

def test_multiple_formats():
    data = {"snake_caseKey": 1, "CamelCaseKey": 2, "with space_key": 3, "mixedTypeKey": 4}
    PascalCaseConverter.convert(source=data)
    assert data == {"SnakeCaseKey": 1, "CamelCaseKey": 2, "WithSpaceKey": 3, "MixedTypeKey": 4}

def test_value_none():
    data = {"normalItem": 1, "noneItem": None}
    PascalCaseConverter.convert(source=data, ignore_malformed=True)
    assert data == {"NormalItem": 1, "NoneItem": None}
