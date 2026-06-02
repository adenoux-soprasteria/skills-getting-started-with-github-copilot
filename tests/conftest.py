"""Shared pytest fixtures for FastAPI backend tests.

AAA convention for all tests:
- Arrange: prepare input/state/fixtures
- Act: execute exactly one API call
- Assert: validate status, payload, and state effects
"""

from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(scope="function")
def client():
    """Yield a fresh test client with deterministic activity state."""
    original_activities = deepcopy(activities)

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        activities.clear()
        activities.update(deepcopy(original_activities))
