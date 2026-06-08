from copy import deepcopy

import pytest
from fastapi.testclient import TestClient
from src import app as app_module

baseline_activities = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(deepcopy(baseline_activities))
    yield


@pytest.fixture
def client():
    return TestClient(app_module.app)
