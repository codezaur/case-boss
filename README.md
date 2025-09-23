# case-boss

[![PyPI version](https://img.shields.io/pypi/v/case-boss.svg)](https://pypi.org/project/case-boss/)
[![Python versions](https://img.shields.io/pypi/pyversions/case-boss.svg)](https://pypi.org/project/case-boss/)
[![License](https://img.shields.io/github/license/codezaur/case-boss.svg)](https://github.com/codezaur/case-boss/blob/main/LICENSE)

A Python package for string case conversion and manipulation, featuring a flexible CLI and extensible core.

## Features

- Convert dictionary/JSON keys between camelCase, snake_case, kebab-case, PascalCase, and more
- Easy to use cli (command-line interface)

## Installation

```bash
pip install case-boss
```

## Usage

### ⌨️ CLI (Command Line Interface)

#### basic commands

```bash
case-boss -v      # show version
case-boss --help  # show options and usage
case-boss cases   # show available target case types

# minimal transform command example; passing only file path, will convert to snake_case and print to standard output (stdout)

case-boss transform path-to/file.json
```

#### options for transform command
```bash
# passing path and selected target case type 
case-boss transform path-to/file.json --to pascal
```

```bash
# passing path and name of result file (will save to file instead of stdout)
case-boss transform path-to/file.json -o result.json
case-boss transform path-to/file.json --output result.json
case-boss transform path-to/file.json > result.json
```

```bash
# modifying file inplace instead of creating new one or printing to stdout
case-boss transform path-to/file.json --inplace
case-boss transform path-to/file.json -i
```

```bash
# using standard input (stdin), passing '-' as the source and piping JSON data.
echo '{"youShallNotPass": "ok"}' | case-boss transform - --to pascal
# output: {"YouShallNotPass": "ok"}
```

```bash
# passing --json directly instead of path to file
case-boss transform --json '{"youShallNotPass": "ok"}' --to pascal
```

```bash
# printing transformation time in seconds
case-boss transform path-to/file.json --benchmark
case-boss transform path-to/file.json -b
```

```bash
# preserving acronyms or custom words (e.g., keep 'ID' or 'HTTP' uppercase):
case-boss transform path-to/file.json --preserve ID,HTTP
```

```bash
# limiting recursion depth (e.g., only transform top-level keys)
case-boss transform path-to/file.json --limit 1
```

```bash
# excluding specific keys from transformation (stopping recursion on those keys)
case-boss transform path-to/file.json --exclude someKey,anotherKey
```

```bash
# rich example; passing path, selected target case type, name of result file and benchmark
case-boss transform path-to/file.json --to pascal --output result.json --benchmark --preserve ID,SQL
```

```bash
# help
case-boss transform --help  # show options and usage for the transform command
```

> **Note:**  
> You must choose only one input source: 
>  
> - use `-` for stdin,
> - use file path to pass file
> - use `--json` to pass JSON directly as arg
>
> You can only use one, either `--inplace` or `--output`


### 🐍 Python API

```python
from case_boss import CaseBoss

boss = CaseBoss()
```

```python
# Basic usage
result = boss.transform(source=my_dict, case="camel")
# assuming my_dict = { "you_shall_not_pass": True }, result will be: { "youShallNotPass": True }
```

```python
# Clone mode: return a new dict, leaving the original untouched
result = boss.transform(source=my_dict, case="camel", clone=True)
```

```python
# Preserving acronyms or custom words (e.g., keep 'ID' or 'HTTP' uppercase):
result = boss.transform(source=my_dict, case="camel", preserve_tokens=["ID", "HTTP"])
# assuming my_dict = { "user_ID": 1, "http_status": "ok" }, result will be: { "userID": 1, "HTTPStatus": "ok" }
```

```python
# Limiting recursion depth (e.g., '1' only transform top-level keys):
result = boss.transform(source=my_dict, case="camel", recursion_limit=1)
```

```python
# Excluding specific keys from transformation (stopping recursion on those keys):
result = boss.transform(source=my_dict, case="camel", exclude_keys=["metaData", "anotherKey"])
```

```python
# For JSON strings (also returns JSON):
json_result = boss.transform_from_json(source=my_json_str, case="camel")
```


#### About `clone`

The `clone` argument (Python API only) determines whether the transformation mutates the original dictionary or returns a new, transformed copy. If `clone=True`, the original input is left unchanged and a new dict is returned. By default, `clone=False` and the input dict is modified in place.

#### About `preserve_tokens`

The `--preserve` CLI option and `preserve_tokens` Python argument allow you to specify a comma-separated list (CLI) or list of strings (Python) of words/acronyms to preserve in their original or uppercase form during case conversion. This is useful for things like `ID`, `HTTP`, etc., so they remain as intended (e.g., `userID` instead of `userId`).

#### About `recursion_limit`

The `--limit` CLI option and `recursion_limit` Python argument set the maximum recursion depth for nested JSON key transformation. For example, setting it to 1 will only transform top-level keys. Defaults to 0 (unlimited recursion).

#### About `exclude_keys`

The `--exclude` CLI option (comma-separated list) and `exclude_keys` Python argument (list of strings) let you specify keys to skip entirely during transformation, halting recursion on those keys and their nested values.

## Supported Case Types

The following case types are supported:

| Type   | Example Output          | Description                |
|--------|-------------------------|----------------------------|
| snake  | you_shall_not_pass      | Snake case                 |
| camel  | youShallNotPass         | Camel case                 |
| pascal | YouShallNotPass         | Pascal case                |
| kebab  | you-shall-not-pass      | Kebab case                 |
| space  | you shall not pass      | Space separated            |
| start  | You Shall Not Pass      | Start case (title case)    |


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
