import importlib.metadata as im
import json
import sys
import time

from case_boss.const import CASE_DESCRIPTIONS, CLI
from case_boss.types import CaseType

try:
    import typer
except ImportError:
    app = None

    def main():
        raise ImportError(CLI.Error.ERROR_TYPER_NOT_FOUND)

else:
    app = typer.Typer(help=CLI.Help.HELP_APP)

    def _version(value: bool) -> None:
        if value:
            typer.echo(f"case-boss version: {im.version('case-boss')}")
            raise typer.Exit()

    @app.callback()
    def _root(
        version: bool = typer.Option(
            None,
            "--version",
            "-v",
            help=CLI.Help.HELP_VERSION,
            callback=_version,
            is_eager=True,
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
            typer.echo(CLI.Warn.WARN_FILE_NOT_JSON, err=False)
        if source and json_input:
            typer.echo(CLI.Error.ERROR_MUTUALLY_EXCLUSIVE, err=True)
            raise typer.Exit(code=1)
        if source is None and json_input is None:
            typer.echo(CLI.Error.ERROR_NO_INPUT, err=True)
            raise typer.Exit(code=1)
        if output and inplace:
            typer.echo(CLI.Error.ERROR_OUTPUT_INPLACE, err=True)
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
                typer.echo(
                    CLI.Error.ERROR_FILE_NOT_FOUND.format(source=source), err=True
                )
                raise typer.Exit(code=1)

    @app.command()
    def cases() -> None:
        """List all supported case types with examples."""
        output = "\n".join(
            f"{c.value}: {CASE_DESCRIPTIONS.get(c.value)}" for c in CaseType
        )
        typer.echo(output)

    @app.command()
    def transform(
        source: str | None = typer.Argument(None, help=CLI.Help.HELP_SOURCE),
        input_json: str | None = typer.Option(None, "--json", help=CLI.Help.HELP_JSON),
        case: CaseType = typer.Option("snake", "--to", help=CLI.Help.HELP_TO),
        output: str | None = typer.Option(
            None, "--output", "-o", help=CLI.Help.HELP_OUTPUT
        ),
        inplace: bool = typer.Option(
            False, "--inplace", "-i", help=CLI.Help.HELP_INPLACE
        ),
        benchmark: bool = typer.Option(
            False, "--benchmark", "-b", help=CLI.Help.HELP_BENCHMARK
        ),
        preserve: str | None = typer.Option(
            None, "--preserve", help=CLI.Help.HELP_PRESERVE
        ),
        exclude: str | None = typer.Option(
            None, "--exclude", help=CLI.Help.HELP_EXCLUDE
        ),
        limit: int = typer.Option(0, "--limit", help=CLI.Help.HELP_LIMIT),
    ) -> None:
        """Transform JSON object keys to the given case type."""

        _validate_args(
            source=source, json_input=input_json, output=output, inplace=inplace
        )
        preserve_tokens = preserve.split(",") if preserve else []
        exclude_keys = exclude.split(",") if exclude else []
        data = _get_input_json(source=source, json_input=input_json)

        from case_boss.case_boss import CaseBoss

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
            typer.echo(CLI.Error.ERROR_INVALID_JSON.format(msg=er.msg), err=True)
            raise typer.Exit(code=1)
        except ValueError as er:
            typer.echo(CLI.Error.ERROR_VALUE.format(msg=str(er)), err=True)
            raise typer.Exit(code=1)

        if output:
            with open(output, "w") as file:
                file.write(result)
                typer.echo(CLI.Info.INFO_NEW_FILE.format(file=output), err=False)
        elif inplace:
            with open(source, "w") as file:
                file.write(result)
                typer.echo(CLI.Info.INFO_UPDATED_INPLACE.format(file=source), err=False)
        else:
            typer.echo(result)

        if benchmark and elapsed is not None:
            typer.echo(CLI.Info.INFO_BENCHMARK.format(seconds=elapsed), err=False)

    if __name__ == "__main__":
        app()

    def main():
        app()
