from core.converters.pascal_converter import PascalCaseConverter
import pytest


@pytest.fixture
def converter():
    return PascalCaseConverter()

@pytest.mark.parametrize("input_str,expected", [
    ("example_dict_key", "ExampleDictKey"),
    ("Example Dict Key", "ExampleDictKey"),
    ("example-dict-key", "ExampleDictKey"),
    ("exampleDictKey", "ExampleDictKey"),
    ("", ""),
])
def test_pascal_case_converter(input_str, expected, converter):
    assert converter._convert_key(input_str) == expected

def test_simple_flat_dict(converter):
    data = {"simpleKey": 1, "another_key": 2, "with space": 3}
    converter.convert(source=data)
    assert data == {"SimpleKey": 1, "AnotherKey": 2, "WithSpace": 3}

def test_nested_dict(converter):
    data = {"outerKey": {"inner_key": 5, "InnerCamel": 6}}
    converter.convert(source=data)
    assert data == {"OuterKey": {"InnerKey": 5, "InnerCamel": 6}}

def test_non_string_keys(converter):
    data = {1: "a", "normalKey": "b"}
    converter.convert(source=data)
    assert data == {1: "a", "NormalKey": "b"}

def test_empty_dict(converter):
    data = {}
    converter.convert(source=data)
    assert data == {}

def test_multiple_formats(converter):
    data = {"snake_caseKey": 1, "CamelCaseKey": 2, "with space_key": 3, "mixedTypeKey": 4}
    converter.convert(source=data)
    assert data == {"SnakeCaseKey": 1, "CamelCaseKey": 2, "WithSpaceKey": 3, "MixedTypeKey": 4}

def test_value_none(converter):
    data = {"normalItem": 1, "noneItem": None}
    converter.convert(source=data)
    assert data == {"NormalItem": 1, "NoneItem": None}

def test_preserve_tokens():
    data = {
        "SQLAlchemy": 1,  
        "userID": 1,
        "default-http-router": 1, 
        "Atomic_http_server": 1
        }
    preserve_tokens = ["SQL", "HTTP", "ID"]
    converter = PascalCaseConverter(preserve_tokens=preserve_tokens)
    converter.convert(source=data)
    assert data == {
        "SQLAlchemy": 1, 
        "UserID": 1,
        "DefaultHTTPRouter": 1, 
        "AtomicHTTPServer": 1
        }
