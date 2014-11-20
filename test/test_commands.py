"""
File: test_commands.py
Author: Rinat F Sabitov
Description:
"""

import os
import sys

import mock
import pytest

from macaca.alfa import CommandsDispatcher

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, '../src'))


@pytest.fixture
def redmine():
    redmine = mock.MagicMock()
    return redmine


@pytest.fixture
def user():
    user = mock.MagicMock()
    return user


def test_empty_dispatcher(redmine, user):
    dispatcher = CommandsDispatcher(redmine, {})
    assert dispatcher.handle(user, "!HELP")
    assert dispatcher.handle(user, "!help")
    assert dispatcher.handle(user, "!help random stuff")

    assert dispatcher.handle(user, "!unknownkommand")
