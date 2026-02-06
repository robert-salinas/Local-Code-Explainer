import pytest
from typer.testing import CliRunner
from explainer.cli import app
from unittest.mock import patch

runner = CliRunner()


@patch("explainer.cli.CodeExplainer")
def test_cli_explain_success(mock_explainer_class, tmp_path):
    # Setup mock
    mock_instance = mock_explainer_class.return_value
    mock_instance.explain.return_value = {
        "analysis": {
            "file_name": "test.py",
            "language": "python",
            "imports": [],
            "total_lines": 1,
            "functions": [],
            "classes": [],
        },
        "explanation": "Test explanation",
        "cached": False,
    }

    file_path = tmp_path / "test.py"
    file_path.write_text("print('hello')")

    result = runner.invoke(app, ["explain", str(file_path)])

    assert result.exit_code == 0
    assert "test.py" in result.stdout
    assert "Test explanation" in result.stdout


def test_cli_explain_file_not_found():
    result = runner.invoke(app, ["explain", "non_existent_file.py"])
    assert result.exit_code == 1
    assert "Error" in result.stderr
