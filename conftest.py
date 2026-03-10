import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
THRESHOLD = int(os.getenv("RESPONSE_TIME_THRESHOLD_MS", "2000"))


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def response_threshold() -> int:
    return THRESHOLD


@pytest.fixture(scope="session")
def api_client(base_url: str) -> requests.Session:
    """
    Shared requests.Session for the whole test run.
    Sets common headers and base URL prefix.
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    session.base_url = base_url  # type: ignore[attr-defined]
    return session


@pytest.fixture
def existing_post_id() -> int:
    """Returns a known valid post ID."""
    return 1


@pytest.fixture
def new_post_payload() -> dict:
    return {
        "title": "QA Automation Post",
        "body": "Created by pytest test suite",
        "userId": 1,
    }


@pytest.fixture
def new_comment_payload() -> dict:
    return {
        "postId": 1,
        "name": "QA Test Comment",
        "email": "qa@bmontes.dev",
        "body": "This is an automated test comment",
    }
