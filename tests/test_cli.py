from click.testing import CliRunner

from soupdemo.cli import greeting, main


def test_greeting():
    assert greeting("Ada") == "Hello, Ada!"


def test_command_function():
    result = CliRunner().invoke(main, ["--name", "Ada"])
    assert result.exit_code == 0
    assert result.output == "Hello, Ada!\n"
