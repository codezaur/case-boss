import pytest
from core.converters.kebab_converter import KebabCaseConverter


@pytest.fixture
def converter():
    return KebabCaseConverter()

@pytest.mark.parametrize("input_str,expected", [
    ("exampleDictKey", "example-dict-key"),
    ("Example_Dict_Key", "example-dict-key"),
    ("example-dict-key", "example-dict-key"),
    ("example dict key", "example-dict-key"),
    ("", ""),
])
def test_kebab_case_converter(input_str, expected, converter):
    assert converter._convert_key(input_str) == expected


def test_simple_flat_dict(converter):
    data = {"simpleKey": 1, "another_key": 2, "with space": 3}
    converter.convert(source=data)
    assert data == {"simple-key": 1, "another-key": 2, "with-space": 3}


def test_nested_dict(converter):
    data = {"outerKey": {"inner_key": 5, "InnerCamel": 6}}
    converter.convert(source=data)
    assert data == {"outer-key": {"inner-key": 5, "inner-camel": 6}}


def test_non_string_keys(converter):
    data = {1: "a", "normalKey": "b"}
    converter.convert(source=data)
    assert data == {1: "a", "normal-key": "b"}


def test_empty_dict(converter):
    data = {}
    converter.convert(source=data)
    assert data == {}


def test_multiple_formats(converter):
    data = {"snake_caseKey": 1, "CamelCaseKey": 2, "with space_key": 3}
    converter.convert(source=data)
    assert data == {"snake-case-key": 1, "camel-case-key": 2, "with-space-key": 3}


def test_value_none(converter):
    data = {"normalItem": 1, "noneItem": None}
    converter.convert(source=data)
    assert data == {"normal-item": 1, "none-item": None}

def test_preservables_acronyms():
    data = {
        "SQLAlchemy": 1,  
        "userID": 1,
        "default-http-router": 1, 
        "Atomic_http_server": 1
        }
    preservables = ["SQL", "HTTP", "ID"]
    converter = KebabCaseConverter(preservables=preservables)
    converter.convert(source=data)
    assert data == {
        "SQL-alchemy": 1, 
        "user-ID": 1,
        "default-HTTP-router": 1, 
        "atomic-HTTP-server": 1
        }

