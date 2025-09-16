from core.converters import (
    CamelCaseConverter,
    KebabCaseConverter,
    PascalCaseConverter,
    SnakeCaseConverter,
    SpaceCaseConverter,
    StartCaseConverter,
)
from core.types import CaseType

CASE_TYPE_CONVERTER_MAPPING = {
    CaseType.SNAKE.value: SnakeCaseConverter,
    CaseType.CAMEL.value: CamelCaseConverter,
    CaseType.PASCAL.value: PascalCaseConverter,
    CaseType.KEBAB.value: KebabCaseConverter,
    CaseType.SPACE.value: SpaceCaseConverter,
    CaseType.START.value: StartCaseConverter,
}
