import pytest
from core.converters.kebab_converter import KebabCaseConverter
from core.converters.case_converter import CaseConverter

def test_convert_basic():
    data = {"simpleKey": 1, "another_key": 2}
    KebabCaseConverter.convert(data)
    assert data == {"simple-key": 1, "another-key": 2}

def test_convert_wrong_type():
    data = ["not", "a", "dict"]
    with pytest.raises(AttributeError):
        KebabCaseConverter.convert(data)

