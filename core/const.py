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

CASE_DESCRIPTIONS = {
    CaseType.CAMEL.value: "camel case (eg. 'youShallNotPass')",
    CaseType.KEBAB.value: "kebab case (eg. 'you-shall-not-pass')",
    CaseType.PASCAL.value: "pascal case (eg. 'YouShallNotPass')",
    CaseType.SNAKE.value: "snake case (eg. 'you_shall_not_pass')",
    CaseType.SPACE.value: "space case (eg. 'you shall not pass')",
    CaseType.START.value: "start case (eg. 'You Shall Not Pass')",
}