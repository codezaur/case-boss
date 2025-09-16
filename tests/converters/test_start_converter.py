import pytest
from core.converters.start_converter import StartCaseConverter


def test_simple_flat_dict():
    data = {"simpleKey": 1, "another_key": 2, "with space": 3}
    StartCaseConverter.convert(source=data)
    assert data == {"Simple Key": 1, "Another Key": 2, "With Space": 3}

def test_nested_dict():
    data = {"outerKey": {"inner_key": 5, "InnerCamel": 6}}
    StartCaseConverter.convert(source=data)
    assert data == {"Outer Key": {"Inner Key": 5, "Inner Camel": 6}}

def test_non_string_keys():
    data = {1: "a", "normalKey": "b"}
    StartCaseConverter.convert(source=data)
    assert data == {1: "a", "Normal Key": "b"}

def test_empty_dict():
    data = {}
    StartCaseConverter.convert(source=data)
    assert data == {}

def test_multiple_formats():
    data = {"snake_caseKey": 1, "CamelCaseKey": 2, "with space_key": 3}
    StartCaseConverter.convert(source=data)
    assert data == {"Snake Case Key": 1, "Camel Case Key": 2, "With Space Key": 3}

def test_value_none():
    data = {"normalItem": 1, "noneItem": None}
    StartCaseConverter.convert(source=data)
    assert data == {"Normal Item": 1, "None Item": None}
