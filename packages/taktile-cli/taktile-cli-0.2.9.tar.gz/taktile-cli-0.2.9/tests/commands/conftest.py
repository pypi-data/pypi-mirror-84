import os

import pytest


@pytest.fixture
def user_key():
    return (
        os.environ["TEST_USER"],
        os.environ["TEST_USER_API_KEY"],
    )
