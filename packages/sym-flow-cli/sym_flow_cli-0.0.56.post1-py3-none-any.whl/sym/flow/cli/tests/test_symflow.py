from contextlib import contextmanager

import pytest
from click.testing import CliRunner

from sym.flow.cli.symflow import symflow as click_command
from sym.flow.cli.version import __version__


@pytest.fixture
def click_setup():
    @contextmanager
    def context():
        runner = CliRunner()
        with runner.isolated_filesystem():
            yield runner

    return context


def test_version(click_setup):
    with click_setup() as runner:
        result = runner.invoke(click_command, ["version"])
        assert result.exit_code == 0
        assert result.output == f"{__version__}\n"
