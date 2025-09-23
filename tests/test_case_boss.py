import json
import os
from collections import OrderedDict, defaultdict

import pytest

from case_boss.case_boss import CaseBoss
from case_boss.types import CaseType


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
    data = defaultdict(lambda: "MISSING", {"simpleKey": 1})
    result = boss.transform(source=data, case=CaseType.KEBAB)
    assert result == {"simple-key": 1}


def test_ordered_dict(boss):
    data = OrderedDict()
    data["simpleKey"] = 1
    data["anotherKey"] = 2
    result = boss.transform(source=data, case=CaseType.KEBAB)
    assert result == {"simple-key": 1, "another-key": 2}


def test_preserve_tokens_kebab(boss):
    data = {"SQLAlchemy": 1, "HTTPRequest": 1, "userID": 1}
    preserve_tokens = ["SQL", "HTTP", "ID"]
    result = boss.transform(
        source=data, case=CaseType.KEBAB, preserve_tokens=preserve_tokens
    )
    assert result == {"SQL-alchemy": 1, "HTTP-request": 1, "user-ID": 1}


def test_skip_excluded_key(boss):
    data = {"simpleKey": 1, "metaData": 1}
    exclude_keys = ["metaData"]
    result = boss.transform(source=data, case=CaseType.KEBAB, exclude_keys=exclude_keys)
    assert result == {"simple-key": 1, "metaData": 1}


def test_transform_nested_dict_with_recursion(boss):
    data = {"simpleKey": 1, "metaData": {"nestedKey": 2, "anotherNested": 3}}
    result = boss.transform(source=data, case=CaseType.KEBAB)
    # Nested keys should be converted
    assert result == {
        "simple-key": 1,
        "meta-data": {"nested-key": 2, "another-nested": 3},
    }


def test_transform_nested_dict_exclude_keys_stops_recursion(boss):
    data = {"simpleKey": 1, "metaData": {"nestedKey": 2, "anotherNested": 3}}
    exclude_keys = ["metaData"]
    result = boss.transform(source=data, case=CaseType.KEBAB, exclude_keys=exclude_keys)
    # metaData should not be converted and should stop recursion
    assert result == {"simple-key": 1, "metaData": {"nestedKey": 2, "anotherNested": 3}}


def test_transform_nested_dict_recursion_limit_0(boss):
    data = {"levelOne": {"levelTwo": {"levelThree": "value"}}}
    result = boss.transform(source=data, case=CaseType.KEBAB)

    # No recursion_limit, all levels should be converted
    assert result == {"level-one": {"level-two": {"level-three": "value"}}}


def test_transform_nested_dict_recursion_limit_1(boss):
    data = {"levelOne": {"levelTwo": {"levelThree": "value"}}}
    result = boss.transform(source=data, case=CaseType.KEBAB, recursion_limit=1)

    # Only levelOne should be converted
    assert result == {"level-one": {"levelTwo": {"levelThree": "value"}}}


def test_transform_nested_dict_recursion_limit_2(boss):
    data = {"levelOne": {"levelTwo": {"levelThree": "value"}}}
    result = boss.transform(source=data, case=CaseType.KEBAB, recursion_limit=2)

    # Only levelOne and levelTwo should be converted
    assert result == {"level-one": {"level-two": {"levelThree": "value"}}}


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
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "sample.json")
    with open(fixture_path, "r") as f:
        json_str = f.read()
    result = boss.transform_from_json(source=json_str, case=CaseType.KEBAB)
    expected = '{"simple-key": 1, "another-key": 2}'
    assert result == expected
