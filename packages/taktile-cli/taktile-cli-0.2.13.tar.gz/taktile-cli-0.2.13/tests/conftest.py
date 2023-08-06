import os

import pytest

from tktl.login import login, logout

pytest_plugins = [
    "tests.cli",
    "tests.sdk",
    "tests.clients",
    "tests.managers",
    "tests.commands",
]


@pytest.fixture
def user_key():
    return os.environ["TEST_USER"], os.environ["TEST_USER_API_KEY"]


@pytest.fixture
def test_user_repos():
    return "tktl-admin/sample-project", "tktl-admin/other-project", "tktl-admin/integ-testing"


@pytest.fixture(scope='module')
def logged_in_context():
    yield login(os.environ["TEST_USER_API_KEY"])
    logout()


