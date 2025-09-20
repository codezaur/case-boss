from collections import OrderedDict, defaultdict
import os
import json
import pytest

from core.case_boss import CaseBoss
from core.types import CaseType

@pytest.fixture
def boss():
    return CaseBoss()

def test_transform_kebab(boss):
    data = {"simpleKey": 1, "another_key": 2}
    result = boss.transform(source=data, case=CaseType.KEBAB)
    assert result == {"simple-key": 1, "another-key": 2}


def test_transform_clone(boss):
    data = {"simpleKey": 1}
    result = boss.transform(source=data, case=CaseType.KEBAB, clone=True)
    assert result == {"simple-key": 1}
    assert data == {"simpleKey": 1}  # original unchanged

def test_transform_literal(boss):
    data = {"simpleKey": 1}
    result = boss.transform(source=data, case="kebab")
    assert result == {"simple-key": 1}

def test_transform_source_not_dict(boss):
    data = ["simpleKey", 1]
    with pytest.raises(ValueError) as exc:
        boss.transform(source=data, case=CaseType.KEBAB)
    assert "Expected dict to transform" in str(exc)

def test_transform_wrong_case(boss):
    data = {"simpleKey": 1}
    with pytest.raises(ValueError) as exc:
        boss.transform(source=data, case="not_a_type")
    assert "Unknown case type" in str(exc)

def test_transform_wrong_case_type(boss):
    data = {"simpleKey": 1}
    with pytest.raises(TypeError) as exc:
        boss.transform(source=data, case=5)
    assert "Expected CaseType or str" in str(exc)

def test_default_dict(boss):
    data =  defaultdict(lambda: "MISSING", {"simpleKey": 1})
    result = boss.transform(source=data, case=CaseType.KEBAB)
    assert result == {"simple-key": 1}

def test_ordered_dict(boss):
    data = OrderedDict()
    data["simpleKey"] = 1
    data["anotherKey"] = 2
    result = boss.transform(source=data, case=CaseType.KEBAB)
    assert result == {"simple-key": 1, "another-key": 2}

def test_preservables_acronyms_kebab(boss):
    data = {"SQLAlchemy": 1, "HTTPRequest": 1, "userID": 1}
    preservables = ["SQL", "HTTP", "ID"]
    result = boss.transform(source=data, case=CaseType.KEBAB, preservables=preservables)
    assert result == {"SQL-alchemy": 1, "HTTP-request": 1, "user-ID": 1}


# JSON  

def test_transform_from_json_valid(boss):
    json_str = '{"simpleKey": 1, "another_key": 2}'
    result = boss.transform_from_json(source=json_str, case=CaseType.SNAKE)
    expected = '{"simple_key": 1, "another_key": 2}'
    assert result == expected

def test_transform_from_json_invalid_json(boss):
    invalid_json = '{"simpleKey": 1, invalid}'
    with pytest.raises(json.JSONDecodeError):
        boss.transform_from_json(source=invalid_json, case=CaseType.SNAKE)

def test_transform_from_json_invalid_type(boss):
    json_str = '{"simpleKey": 1}'
    with pytest.raises(ValueError) as exc:
        boss.transform_from_json(source=json_str, case="not_a_type")
    assert "Unknown case type" in str(exc)

def test_transform_from_json_nested(boss):
    json_str = '{"simpleKey": {"nestedKey": 1}, "another_key": [1, 2]}'
    result = boss.transform_from_json(source=json_str, case=CaseType.CAMEL)
    expected = '{"simpleKey": {"nestedKey": 1}, "anotherKey": [1, 2]}'
    assert result == expected


def test_transform_from_json_from_file(boss):
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'sample.json')
    with open(fixture_path, 'r') as f:
        json_str = f.read()
    result = boss.transform_from_json(source=json_str, case=CaseType.KEBAB)
    expected = '{"simple-key": 1, "another-key": 2}'
    assert result == expected