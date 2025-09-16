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
