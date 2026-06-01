from src.workers import dispatch
import pytest


def setup_function():
    dispatch._results.clear()


def test_run_task_happy_path(monkeypatch):
    monkeypatch.setattr(dispatch, "fetch_from_broker", lambda tid: {"n": 21})
    result = dispatch.run_task(lambda p: p["n"] * 2, "t1")
    assert result == 42


def test_retries_on_broker_error(monkeypatch):
    calls = {"n": 0}
    sleeps = []

    def flaky_fetch(_task_id):
        calls["n"] += 1
        if calls["n"] < 3:
            raise dispatch.BrokerError("transient")
        return {"n": 5}

    monkeypatch.setattr(dispatch, "fetch_from_broker", flaky_fetch)
    result = dispatch.run_task(lambda p: p["n"] * 2, "t-retry", sleep=sleeps.append)

    assert result == 10
    assert calls["n"] == 3
    assert sleeps == [0.1, 0.2]


def test_gives_up_after_max_retries(monkeypatch):
    calls = {"n": 0}
    sleeps = []

    def always_fail(_task_id):
        calls["n"] += 1
        raise dispatch.BrokerError("still failing")

    monkeypatch.setattr(dispatch, "fetch_from_broker", always_fail)

    with pytest.raises(dispatch.BrokerError):
        dispatch.run_task(lambda p: p, "t-fail", max_retries=3, sleep=sleeps.append)

    assert calls["n"] == 4
    assert sleeps == [0.1, 0.2, 0.4]


def test_idempotent(monkeypatch):
    fetch_calls = {"n": 0}
    handler_calls = {"n": 0}

    def fetch_once(_task_id):
        fetch_calls["n"] += 1
        return {"n": 7}

    def handler(payload):
        handler_calls["n"] += 1
        return payload["n"] + 1

    monkeypatch.setattr(dispatch, "fetch_from_broker", fetch_once)

    first = dispatch.run_task(handler, "t-idem")
    second = dispatch.run_task(handler, "t-idem")

    assert first == 8
    assert second == 8
    assert fetch_calls["n"] == 1
    assert handler_calls["n"] == 1