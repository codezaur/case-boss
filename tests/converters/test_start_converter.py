import pytest

from case_boss.converters.start_converter import StartCaseConverter


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("example_dict_key", "Example Dict Key"),
        ("Example Dict Key", "Example Dict Key"),
        ("example-dict-key", "Example Dict Key"),
        ("exampleDictKey", "Example Dict Key"),
        ("", ""),
    ],
)
def test_start_case_converter(input_str, expected, converter):
    assert converter._convert_key(input_str) == expected


@pytest.fixture
def converter():
    return StartCaseConverter()


def test_simple_flat_dict(converter):
    data = {"simpleKey": 1, "another_key": 2, "with space": 3}
    converter.convert(source=data)
    assert data == {"Simple Key": 1, "Another Key": 2, "With Space": 3}


def test_nested_dict(converter):
    data = {"outerKey": {"inner_key": 5, "InnerCamel": 6}}
    converter.convert(source=data)
    assert data == {"Outer Key": {"Inner Key": 5, "Inner Camel": 6}}


def test_non_string_keys(converter):
    data = {1: "a", "normalKey": "b"}
    converter.convert(source=data)
    assert data == {1: "a", "Normal Key": "b"}


def test_empty_dict(converter):
    data = {}
    converter.convert(source=data)
    assert data == {}


def test_multiple_formats(converter):
    data = {"snake_caseKey": 1, "CamelCaseKey": 2, "with space_key": 3}
    converter.convert(source=data)
    assert data == {"Snake Case Key": 1, "Camel Case Key": 2, "With Space Key": 3}


def test_value_none(converter):
    data = {"normalItem": 1, "noneItem": None}
    converter.convert(source=data)
    assert data == {"Normal Item": 1, "None Item": None}


def test_preserve_tokens():
    data = {
        "SQLAlchemy": 1,
        "userID": 1,
        "default-http-router": 1,
        "Atomic_http_server": 1,
    }
    preserve_tokens = ["SQL", "HTTP", "ID"]
    converter = StartCaseConverter(preserve_tokens=preserve_tokens)
    converter.convert(source=data)
    assert data == {
        "SQL Alchemy": 1,
        "User ID": 1,
        "Default HTTP Router": 1,
        "Atomic HTTP Server": 1,
    }
