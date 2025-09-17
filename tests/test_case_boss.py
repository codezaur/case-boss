import os
import json
import pytest

from core.case_boss import CaseBoss
from core.types import CaseType


def test_transform_kebab():
    boss = CaseBoss()
    data = {"simpleKey": 1, "another_key": 2}
    result = boss.transform(source=data, type=CaseType.KEBAB.value)
    assert result == {"simple-key": 1, "another-key": 2}


def test_transform_clone():
    boss = CaseBoss()
    data = {"simpleKey": 1}
    result = boss.transform(source=data, type=CaseType.KEBAB.value, clone=True)
    assert result == {"simple-key": 1}
    assert data == {"simpleKey": 1}  # original unchanged


def test_transform_wrong_type():
    boss = CaseBoss()
    data = {"simpleKey": 1}
    with pytest.raises(ValueError) as exc:
        boss.transform(source=data, type="not_a_type")
    assert "Unknown case type" in str(exc.value)

# JSON  

def test_transform_from_json_valid():
    boss = CaseBoss()
    json_str = '{"simpleKey": 1, "another_key": 2}'
    result = boss.transform_from_json(source=json_str, type=CaseType.SNAKE.value)
    expected = '{"simple_key": 1, "another_key": 2}'
    assert result == expected

def test_transform_from_json_invalid_json():
    boss = CaseBoss()
    invalid_json = '{"simpleKey": 1, invalid}'
    with pytest.raises(json.JSONDecodeError):
        boss.transform_from_json(source=invalid_json, type=CaseType.SNAKE.value)

def test_transform_from_json_invalid_type():
    boss = CaseBoss()
    json_str = '{"simpleKey": 1}'
    with pytest.raises(ValueError) as exc:
        boss.transform_from_json(source=json_str, type="not_a_type")
    assert "Unknown case type" in str(exc.value)

def test_transform_from_json_nested():
    boss = CaseBoss()
    json_str = '{"simpleKey": {"nestedKey": 1}, "another_key": [1, 2]}'
    result = boss.transform_from_json(source=json_str, type=CaseType.CAMEL.value)
    expected = '{"simpleKey": {"nestedKey": 1}, "anotherKey": [1, 2]}'
    assert result == expected


def test_transform_from_json_from_file():
    boss = CaseBoss()
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'sample.json')
    with open(fixture_path, 'r') as f:
        json_str = f.read()
    result = boss.transform_from_json(source=json_str, type=CaseType.KEBAB.value)
    expected = '{"simple-key": 1, "another-key": 2}'
    assert result == expected