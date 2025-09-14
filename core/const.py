from core.converters.kebab_converter import KebabCaseConverter
from core.types import CaseType


CASE_TYPE_CONVERTER_MAPPING = {
    CaseType.SNAKE.value: KebabCaseConverter,  # replace later
    CaseType.CAMEL.value: KebabCaseConverter,  # replace later
    CaseType.PASCAL.value: KebabCaseConverter,  # replace later
    CaseType.KEBAB.value: KebabCaseConverter,
    CaseType.SPACE.value: KebabCaseConverter,  # replace later
}
