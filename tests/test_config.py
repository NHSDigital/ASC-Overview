import json
import pytest
import asc_overview


@pytest.fixture(scope="session", autouse=True)
def patch_testing(monkeypatch):
    with open("./params_json/2020-21.json") as params_file:
        patched_params = json.load(params_file)

    monkeypatch.setattr(asc_overview, "params", patched_params)
