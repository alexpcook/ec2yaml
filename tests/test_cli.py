import pytest

import cli

def test_parser_without_file():
    """
    When no file is given, the CLI will exit with a non-zero status.
    """

    with pytest.raises(SystemExit):
        parser = cli.get_parser()
        args = parser.parse_args([])


def test_parser_with_file():
    """
    When a file argument is given, the CLI will not exit.
    """

    parser = cli.get_parser()
    args = parser.parse_args(['/some/path'])

    assert args.file == '/some/path'
