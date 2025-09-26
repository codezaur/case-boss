from dataclasses import dataclass

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


@dataclass(frozen=True)
class CLI:
    @dataclass(frozen=True)
    class Help:
        HELP_APP = "CaseBoss: dict key case converter"
        HELP_TRANSFORM = "Transform dict keys in a JSON file to the given case type."
        HELP_SOURCE = "Path to JSON file"
        HELP_JSON = "Direct JSON string input (alternative to file/stdin)"
        HELP_TO = "Target case type"
        HELP_OUTPUT = "Write output to a file (expects a filename)."
        HELP_INPLACE = "Modify the input file in place, instead of creating new one (cannot be used with --output or stdin)."
        HELP_BENCHMARK = "Report transformation time in seconds"
        HELP_PRESERVE = (
            "Comma-separated list of tokens (e.g., 'ID,SQL,URL') whose original casing should be preserved "
            "within converted values. For example, preserving 'SQL' in SQLAlchemy will return 'SQL_alchemy', "
            "leaving 'SQL' unchanged."
        )
        HELP_EXCLUDE = (
            "Comma-separated list of keys to skip entirely (stopping recursion)."
        )
        HELP_LIMIT = (
            "Set the maximum recursion depth for nested JSON key transformation. "
            "For example, setting to 1 will only transform top level keys. Defaults to 0 (unlimited)."
        )
        HELP_VERSION = "Show version and exit"

    @dataclass(frozen=True)
    class Error:
        ERROR_TYPER_NOT_FOUND = "The CaseBoss CLI requires 'typer'. Install with 'pip install case-boss[cli]'."
        ERROR_MUTUALLY_EXCLUSIVE = "Error: Cannot use both --json and source argument."
        ERROR_NO_INPUT = "Error: Provide either a source (file/-) or --json."
        ERROR_FILE_NOT_FOUND = "Error: File '{source}' not found"
        ERROR_INVALID_JSON = "Error: Invalid JSON - {msg}"
        ERROR_OUTPUT_INPLACE = "Error: --output and --inplace cannot be used together"
        ERROR_VALUE = "Error: {msg}"

    @dataclass(frozen=True)
    class Warn:
        WARN_FILE_NOT_JSON = "Warning: Input file does not have a .json extension. Ensure content is valid JSON."

    @dataclass(frozen=True)
    class Info:
        INFO_NEW_FILE = "Info: created new file '{file}'"
        INFO_UPDATED_INPLACE = "Info: modified file: '{file}' in place"
        INFO_BENCHMARK = "Info: transformation completed in {seconds} seconds"
