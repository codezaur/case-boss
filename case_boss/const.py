from case_boss.converters import (
    CamelCaseConverter,
    KebabCaseConverter,
    PascalCaseConverter,
    SnakeCaseConverter,
    SpaceCaseConverter,
    StartCaseConverter,
)
from case_boss.types import CaseType

CASE_TYPE_CONVERTER_MAPPING = {
    CaseType.SNAKE.value: SnakeCaseConverter,
    CaseType.CAMEL.value: CamelCaseConverter,
    CaseType.PASCAL.value: PascalCaseConverter,
    CaseType.KEBAB.value: KebabCaseConverter,
    CaseType.SPACE.value: SpaceCaseConverter,
    CaseType.START.value: StartCaseConverter,
}

CASE_DESCRIPTIONS = {
    CaseType.CAMEL.value: "camel case (e.g., 'youShallNotPass')",
    CaseType.KEBAB.value: "kebab case (e.g., 'you-shall-not-pass')",
    CaseType.PASCAL.value: "pascal case (e.g., 'YouShallNotPass')",
    CaseType.SNAKE.value: "snake case (e.g., 'you_shall_not_pass')",
    CaseType.SPACE.value: "space case (e.g., 'you shall not pass')",
    CaseType.START.value: "start case (e.g., 'You Shall Not Pass')",
}
