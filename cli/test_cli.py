import io
import json
import sys
from cli.const import ERROR_NO_INPUT, ERROR_OUTPUT_INPLACE, WARN_FILE_NOT_JSON
import pytest
from typer.testing import CliRunner

from .cli import app

runner = CliRunner()

def test_transform_with_json_input():
    input_json = '{"simpleKey": 1, "another_key": 2}'
    result = runner.invoke(app, ["transform", "--json", input_json])
    assert result.exit_code == 0
    assert '"simple_key": 1' in result.output

def test_transform_with_json_and_to_option():
    input_json = '{"simpleKey": 1, "another_key": 2}'
    result = runner.invoke(app, ["transform", "--json", input_json, "--to", "kebab"])
    assert result.exit_code == 0
    assert '"simple-key": 1' in result.output

def test_transform_with_json_and_output_file(tmp_path):
    input_json = '{"simpleKey": 1, "another_key": 2}'
    out_file = tmp_path / "out.json"
    result = runner.invoke(app, ["transform", "--json", input_json, "--output", str(out_file)])
    assert result.exit_code == 0
    assert f"Info: created new file '{out_file}'" in result.output
    with open(out_file) as f:
        data = f.read()
    assert '"simple_key": 1' in data

def test_transform_with_file_input(tmp_path):
    in_file = tmp_path / "in.json"
    in_file.write_text('{"simple_key": 1, "another_key": 2}')
    result = runner.invoke(app, ["transform", str(in_file), "--to", "camel", "--inplace"])
    assert result.exit_code == 0
    assert f"Info: modified file: '{in_file}' in place" in result.output
    with open(in_file) as f:
        data = f.read()
    assert '"simpleKey": 1' in data

def test_transform_with_file_input_stdout(tmp_path):
    in_file = tmp_path / "in.json"
    in_file.write_text('{"simple_key": 1, "another_key": 2}')
    result = runner.invoke(app, ["transform", str(in_file), "--to", "camel"])
    assert result.exit_code == 0
    # Should output to stdout, not modify file
    assert '"simpleKey": 1' in result.output
    # Input file should remain unchanged
    with open(in_file) as f:
        data = f.read()
    assert '"simple_key": 1' in data

def test_transform_with_file_input_inplace(tmp_path):
    in_file = tmp_path / "in.json"
    in_file.write_text('{"simple_key": 1, "another_key": 2}')
    result = runner.invoke(app, ["transform", str(in_file), "--to", "camel", "--inplace"])
    assert result.exit_code == 0
    assert f"Info: modified file: '{in_file}' in place" in result.output
    # Input file should be changed
    with open(in_file) as f:
        data = f.read()
    assert '"simpleKey": 1' in data

def test_transform_with_file_input_txt(tmp_path):
    in_file = tmp_path / "in.txt"
    in_file.write_text('{"simple_key": 1, "another_key": 2}')
    result = runner.invoke(app, ["transform", str(in_file), "--to", "camel"])
    assert WARN_FILE_NOT_JSON in result.output
    assert result.exit_code == 0
    assert '"simpleKey": 1' in result.output

def test_transform_with_benchmark():
    input_json = '{"simpleKey": 1, "another_key": 2}'
    result = runner.invoke(app, ["transform", "--json", input_json, "--benchmark"])
    assert result.exit_code == 0
    assert "Info: transformation completed in" in result.output

def test_transform_with_stdin():
    input_json = '{"simpleKey": 1, "another_key": 2}'
    result = runner.invoke(app, ["transform", "-"], input=input_json)
    assert result.exit_code == 0
    assert '"simple_key": 1' in result.output

def test_transform_path_json_error():
    input_json = '{"simpleKey": 1}'
    result = runner.invoke(app, ["transform", "file.json", "--json", input_json])
    assert result.exit_code == 1
    assert "Cannot use both" in result.output or "mutually exclusive" in result.output

def test_transform_output_inplace_error(tmp_path):
    in_file = tmp_path / "in.json"
    in_file.write_text('{"simple_key": 1, "another_key": 2}')
    result = runner.invoke(app, ["transform", str(in_file), "--output", "result.json", "--inplace"])
    assert result.exit_code == 1
    assert ERROR_OUTPUT_INPLACE.strip() == result.output.strip()

def test_transform_missing_input_error():
    result = runner.invoke(app, ["transform"])
    assert result.exit_code == 1
    assert ERROR_NO_INPUT.strip() == result.output.strip()

def test_transform_invalid_json():
    input_json = '{"simpleKey": 1, invalid}'
    result = runner.invoke(app, ["transform", "--json", input_json])
    assert result.exit_code == 1
    assert "Invalid JSON" in result.output or "Expecting property name" in result.output

def test_transform_invalid_case_type():
    input_json = '{"simpleKey": 1}'
    result = runner.invoke(app, ["transform", "--json", input_json, "--to", "not_a_type"])
    assert result.exit_code == 2
    assert "Invalid value for '--to'" in result.output

def test_cli_preserve(tmp_path):
    input_data = '{"SQLAlchemy": 1, "userID": 1, "default-http-router": 1, "Atomic_http_server": 1}'
    input_file = tmp_path / "input.json"
    input_file.write_text(input_data)

    result = runner.invoke(app, ["transform", str(input_file), "--to", "kebab", "--preserve", "SQL,HTTP,ID"])
    assert result.exit_code == 0
    assert 'SQL-alchemy' in result.output
    assert 'user-ID' in result.output
    assert 'default-HTTP-router' in result.output
    assert 'atomic-HTTP-server' in result.output

def test_cli_exclude(tmp_path):
    input_data = '{"simpleKey": 1, "metaData": 1}'
    input_file = tmp_path / "input.json"
    input_file.write_text(input_data)

    result = runner.invoke(app, ["transform", str(input_file), "--to", "kebab", "--exclude", "metaData,test"])
    assert result.exit_code == 0
    assert 'simple-key' in result.output
    assert 'metaData' in result.output

def test_cli_transform_nested_dict_with_recursion(tmp_path):
    input_data = '{"simpleKey": 1, "metaData": {"nestedKey": 2, "anotherNested": 3}}'
    input_file = tmp_path / "input.json"
    input_file.write_text(input_data)

    result = runner.invoke(app, ["transform", str(input_file), "--to", "kebab"])

    assert result.exit_code == 0
    # Nested keys should be converted
    output_json = json.loads(result.output)
    assert "simple-key" in output_json
    assert "meta-data" in output_json
    assert isinstance(output_json["meta-data"], dict)
    assert "nested-key" in output_json["meta-data"]
    assert "another-nested" in output_json["meta-data"]

def test_cli_transform_nested_dict_exclude_keys_stops_recursion(tmp_path):
    input_data = '{"simpleKey": 1, "metaData": {"nestedKey": 2, "anotherNested": 3}}'
    input_file = tmp_path / "input.json"
    input_file.write_text(input_data)

    result = runner.invoke(app, ["transform", str(input_file), "--to", "kebab", "--exclude", "metaData"])

    assert result.exit_code == 0
    # metaData should not be converted and should stop recursion
    output_json = json.loads(result.output)
    assert "simple-key" in output_json
    assert "metaData" in output_json
    assert isinstance(output_json["metaData"], dict)
    assert "nestedKey" in output_json["metaData"]
    assert "anotherNested" in output_json["metaData"]
