import sys
import typer
import time
import json
from cli.const import ERROR_FILE_NOT_FOUND, ERROR_INVALID_JSON, ERROR_MUTUALLY_EXCLUSIVE, ERROR_NO_INPUT, ERROR_OUTPUT_INPLACE, ERROR_VALUE, HELP_APP, HELP_BENCHMARK, HELP_INPLACE, HELP_JSON, HELP_OUTPUT, HELP_PRESERVABLES, HELP_SOURCE, HELP_TO, HELP_VERSION, INFO_BENCHMARK, INFO_NEW_FILE, INFO_UPDATED_INPLACE, WARN_FILE_NOT_JSON
from core.case_boss import CaseBoss
from core.const import CASE_DESCRIPTIONS
from core.types import CaseType
from core import __version__


app = typer.Typer(help=HELP_APP)


def _version(value: bool) -> None:
  if value:
    typer.echo(f"case-boss version: {__version__}")
    raise typer.Exit()


def _validate_args(
    source: str | None, 
    json_input: str = "",
    output: str = "",
    inplace: bool = False,

    ) -> None:
  if source and source != "-" and not source.endswith(".json"):
    typer.echo(WARN_FILE_NOT_JSON, err=False)
  if source and json_input:
    typer.echo(ERROR_MUTUALLY_EXCLUSIVE, err=True)
    raise typer.Exit(code=1)
  if source is None and not json_input:
    typer.echo(ERROR_NO_INPUT, err=True)
    raise typer.Exit(code=1)
  if output and inplace:
    typer.echo(ERROR_OUTPUT_INPLACE, err=True)
    raise typer.Exit(code=1)


def _get_input_json(source: str | None, json_input: str = "") -> str:
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


@app.callback()
def main(version: bool = typer.Option(
  None, 
  "--version", 
  "-v", 
  help=HELP_VERSION, 
  callback=_version, 
  is_eager=True)) -> None:
  pass


@app.command()
def cases() -> None:
  """List all supported case types with examples."""
  output = "\n".join(f"{c.value}: {CASE_DESCRIPTIONS.get(c.value)}" for c in CaseType)
  typer.echo(output)


@app.command()
def transform(
  source: str = typer.Argument(None, help=HELP_SOURCE),
  input_json: str = typer.Option(None, "--json", help=HELP_JSON),
  case: CaseType = typer.Option('snake', "--to", help=HELP_TO),
  output: str = typer.Option(None, "--output", "-o", help=HELP_OUTPUT),
  inplace: bool = typer.Option(False, "--inplace", "-i", help=HELP_INPLACE),
  benchmark: bool = typer.Option(False, "--benchmark", "-b", help=HELP_BENCHMARK),
  preservables: str = typer.Option(None, "--preservables", help=HELP_PRESERVABLES)
) -> None:
  """Transform JSON object keys to the given case type."""

  _validate_args(source=source, json_input=input_json, output=output, inplace=inplace)
  preservables_list = preservables.split(",") if preservables else []
  data = _get_input_json(source=source, json_input=input_json)

  boss = CaseBoss()
  
  try:
    start = time.perf_counter() if benchmark else None
    result = boss.transform_from_json(source=data, case=case, preservables=preservables_list)
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