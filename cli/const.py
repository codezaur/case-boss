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
HELP_EXCLUDE = "Comma-separated list of keys to skip entirely (stopping recursion)."
HELP_VERSION = "Show version and exit"

ERROR_MUTUALLY_EXCLUSIVE = "Error: Cannot use both --json and source argument."
ERROR_NO_INPUT = "Error: Provide either a source (file/-) or --json."
ERROR_FILE_NOT_FOUND = "Error: File '{source}' not found"
ERROR_INVALID_JSON = "Error: Invalid JSON - {msg}"
ERROR_OUTPUT_INPLACE = "Error: --output and --inplace cannot be used together"
ERROR_VALUE = "Error: {msg}"

WARN_FILE_NOT_JSON = "Warning: Input file does not have a .json extension. Ensure content is valid JSON."

INFO_NEW_FILE = "Info: created new file '{file}'"
INFO_UPDATED_INPLACE = "Info: modified file: '{file}' in place"
INFO_BENCHMARK = "Info: transformation completed in {seconds} seconds"