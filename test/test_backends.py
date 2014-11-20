import pytest
import mock


import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, '../src'))


@pytest.fixture
def redmine():
    redmine = mock.MagicMock()
    return redmine


def test_redmine_api_backend(redmine):
    from macaca.backends import RedmineApiBackend
    backend = RedmineApiBackend('http://dummy/', project='test', key='dummy')
    backend.redmine = redmine

    backend.create_new_issue("My test issue")
    assert backend.redmine.issue.create.called, "Issue creation not called"
