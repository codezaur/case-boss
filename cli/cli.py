import importlib.metadata as im
import json
import sys
import time

from case_boss.case_boss import CaseBoss
from case_boss.const import CASE_DESCRIPTIONS
from case_boss.types import CaseType
from cli.const import (
    ERROR_FILE_NOT_FOUND,
    ERROR_INVALID_JSON,
    ERROR_MUTUALLY_EXCLUSIVE,
    ERROR_NO_INPUT,
    ERROR_OUTPUT_INPLACE,
    ERROR_TYPER_NOT_FOUND,
    ERROR_VALUE,
    HELP_APP,
    HELP_BENCHMARK,
    HELP_EXCLUDE,
    HELP_INPLACE,
    HELP_JSON,
    HELP_LIMIT,
    HELP_OUTPUT,
    HELP_PRESERVE,
    HELP_SOURCE,
    HELP_TO,
    HELP_VERSION,
    INFO_BENCHMARK,
    INFO_NEW_FILE,
    INFO_UPDATED_INPLACE,
    WARN_FILE_NOT_JSON,
)

try:
    import typer
except ImportError:

    def main():
        raise ImportError(ERROR_TYPER_NOT_FOUND)

else:
    app = typer.Typer(help=HELP_APP)

    def _version(value: bool) -> None:
        if value:
            typer.echo(f"case-boss version: {im.version('case-boss')}")
            raise typer.Exit()

    @app.callback()
    def main(
        version: bool = typer.Option(
            None, "--version", "-v", help=HELP_VERSION, callback=_version, is_eager=True
        )
    ) -> None:
        pass


def _validate_args(
    source: str | None,
    json_input: str | None,
    output: str = "",
    inplace: bool = False,
) -> None:
    if source and source != "-" and not source.endswith(".json"):
        typer.echo(WARN_FILE_NOT_JSON, err=False)
    if source and json_input:
        typer.echo(ERROR_MUTUALLY_EXCLUSIVE, err=True)
        raise typer.Exit(code=1)
    if source is None and json_input is None:
        typer.echo(ERROR_NO_INPUT, err=True)
        raise typer.Exit(code=1)
    if output and inplace:
        typer.echo(ERROR_OUTPUT_INPLACE, err=True)
        raise typer.Exit(code=1)


def _get_input_json(source: str | None, json_input: str | None) -> str:
    if json_input:
        return json_input
    elif source == "-":
        return sys.stdin.read()
    else:
        try:
            with open(source, "r") as file:
                return file.read()
        except FileNotFoundError:
            typer.echo(ERROR_FILE_NOT_FOUND.format(source=source), err=True)
            raise typer.Exit(code=1)


@app.command()
def cases() -> None:
    """List all supported case types with examples."""
    output = "\n".join(f"{c.value}: {CASE_DESCRIPTIONS.get(c.value)}" for c in CaseType)
    typer.echo(output)


@app.command()
def transform(
    source: str | None = typer.Argument(None, help=HELP_SOURCE),
    input_json: str | None = typer.Option(None, "--json", help=HELP_JSON),
    case: CaseType = typer.Option("snake", "--to", help=HELP_TO),
    output: str | None = typer.Option(None, "--output", "-o", help=HELP_OUTPUT),
    inplace: bool = typer.Option(False, "--inplace", "-i", help=HELP_INPLACE),
    benchmark: bool = typer.Option(False, "--benchmark", "-b", help=HELP_BENCHMARK),
    preserve: str | None = typer.Option(None, "--preserve", help=HELP_PRESERVE),
    exclude: str | None = typer.Option(None, "--exclude", help=HELP_EXCLUDE),
    limit: int = typer.Option(0, "--limit", help=HELP_LIMIT),
) -> None:
    """Transform JSON object keys to the given case type."""

    _validate_args(source=source, json_input=input_json, output=output, inplace=inplace)
    preserve_tokens = preserve.split(",") if preserve else []
    exclude_keys = exclude.split(",") if exclude else []
    data = _get_input_json(source=source, json_input=input_json)

    boss = CaseBoss()

    try:
        start = time.perf_counter() if benchmark else None
        result = boss.transform_from_json(
            source=data,
            case=case,
            preserve_tokens=preserve_tokens,
            exclude_keys=exclude_keys,
            recursion_limit=limit,
        )
        elapsed = (time.perf_counter() - start) if benchmark else None
    except json.JSONDecodeError as er:
        typer.echo(ERROR_INVALID_JSON.format(msg=er.msg), err=True)
        raise typer.Exit(code=1)
    except ValueError as er:
        typer.echo(ERROR_VALUE.format(msg=str(er)), err=True)
        raise typer.Exit(code=1)

    if output:
        with open(output, "w") as file:
            file.write(result)
            typer.echo(INFO_NEW_FILE.format(file=output), err=False)
    elif inplace:
        with open(source, "w") as file:
            file.write(result)
            typer.echo(INFO_UPDATED_INPLACE.format(file=source), err=False)
    else:
        typer.echo(result)

    if benchmark and elapsed is not None:
        typer.echo(INFO_BENCHMARK.format(seconds=elapsed), err=False)


if __name__ == "__main__":
    app()
