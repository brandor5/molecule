#  Copyright (c) 2015-2018 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

from typing import Any
from unittest.mock import Mock

from click.testing import CliRunner
from pytest import LogCaptureFixture
from pytest_mock import MockerFixture

from molecule import config
from molecule.command import converge
from molecule.shell import main


# NOTE(retr0h): The use of the `patched_config_validate` fixture, disables
# config.Config._validate from executing.  Thus preventing odd side-effects
# throughout patched.assert_called unit tests.
def test_execute(
    mocker: MockerFixture,
    caplog: LogCaptureFixture,
    patched_ansible_converge: Mock,
    patched_config_validate: Any,
    config_instance: config.Config,
) -> None:
    c = converge.Converge(config_instance)
    c.execute()

    assert "default" in caplog.text
    assert "converge" in caplog.text

    patched_ansible_converge.assert_called_once_with()

    assert config_instance.state.converged


def test_ansible_args_passed_to_scenarios_get_configs(mocker: MockerFixture) -> None:
    # Scenarios patch is needed to safely invoke CliRunner
    # in the test environment and block scenario execution
    mocker.patch("molecule.scenarios.Scenarios")
    patched_get_configs = mocker.patch("molecule.command.base.get_configs")

    runner = CliRunner()
    args = ("converge", "--", "-e", "testvar=testvalue")
    ansible_args = args[2:]
    runner.invoke(main, args, obj={})

    # call index [0][2] is the 3rd positional argument to get_configs,
    # which should be the tuple of parsed ansible_args from the CLI
    assert patched_get_configs.call_args[0][2] == ansible_args
