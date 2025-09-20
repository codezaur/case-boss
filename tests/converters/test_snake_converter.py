import pytest
from core.converters.snake_converter import SnakeCaseConverter

@pytest.fixture
def converter():
    return SnakeCaseConverter()

@pytest.mark.parametrize("input_str,expected", [
    ("exampleDictKey", "example_dict_key"),
    ("Example Dict Key", "example_dict_key"),
    ("example-dict-key", "example_dict_key"),
    ("example_dict_key", "example_dict_key"),
    ("", ""),
])
def test_snake_case_converter(input_str, expected, converter):
    assert converter._convert_key(input_str) == expected

def test_simple_flat_dict(converter):
    data = {"simpleKey": 1, "another_key": 2, "with space": 3}
    converter.convert(source=data)
    assert data == {"simple_key": 1, "another_key": 2, "with_space": 3}

def test_nested_dict(converter):
    data = {"outerKey": {"inner_key": 5, "InnerCamel": 6}}
    converter.convert(source=data)
    assert data == {"outer_key": {"inner_key": 5, "inner_camel": 6}}

def test_non_string_keys(converter):
    data = {1: "a", "normalKey": "b"}
    converter.convert(source=data)
    assert data == {1: "a", "normal_key": "b"}

def test_empty_dict(converter):
    data = {}
    converter.convert(source=data)
    assert data == {}

def test_multiple_formats(converter):
    data = {"snake_caseKey": 1, "CamelCaseKey": 2, "with space_key": 3}
    converter.convert(source=data)
    assert data == {"snake_case_key": 1, "camel_case_key": 2, "with_space_key": 3}

def test_value_none(converter):
    data = {"normalItem": 1, "noneItem": None}
    converter.convert(source=data)
    assert data == {"normal_item": 1, "none_item": None}

def test_preserve_tokens():
    data = {
        "SQLAlchemy": 1, 
        "userID": 1,
        "default-http-router": 1, 
        "Atomic_http_server": 1
        }
    preserve_tokens = ["SQL", "HTTP", "ID"]
    converter = SnakeCaseConverter(preserve_tokens=preserve_tokens)
    converter.convert(source=data)
    assert data == {
        "SQL_alchemy": 1, 
        "user_ID": 1,
        "default_HTTP_router": 1,
        "atomic_HTTP_server": 1
        }