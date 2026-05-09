import json
from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import services
from models import Base, Task


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)
    s = Session()
    try:
        yield s
    finally:
        s.close()
        engine.dispose()


def test_create_list_and_task(session):
    lst = services.create_list(session, "Inbox")
    assert lst.id is not None
    assert lst.name == "Inbox"

    task = services.add_task(session, lst.id, "Write tests", date(2026, 6, 1), "high")
    assert task.id is not None
    assert task.list_id == lst.id
    assert task.content == "Write tests"
    assert task.priority == "high"
    assert task.status == "open"
    assert task.completed_at is None
    assert task.due_date.date() == date(2026, 6, 1)


def test_toggle_status_sets_and_clears_completed_at(session):
    lst = services.create_list(session, "Work")
    task = services.add_task(session, lst.id, "Ship VibeDo", None, "medium")
    assert task.status == "open"

    services.set_task_status(session, task.id, True)
    refreshed = session.get(Task, task.id)
    assert refreshed.status == "done"
    assert refreshed.completed_at is not None

    services.set_task_status(session, task.id, False)
    refreshed = session.get(Task, task.id)
    assert refreshed.status == "open"
    assert refreshed.completed_at is None


def test_clear_completed_only_removes_done(session):
    lst = services.create_list(session, "Chores")
    keep = services.add_task(session, lst.id, "Keep me", None, "low")
    drop = services.add_task(session, lst.id, "Drop me", None, "low")
    services.set_task_status(session, drop.id, True)

    deleted = services.clear_completed(session, lst.id)
    assert deleted == 1

    remaining = services.list_tasks(session, lst.id)
    assert [t["id"] for t in remaining] == [keep.id]


def test_list_tasks_sort_by_priority(session):
    lst = services.create_list(session, "Mixed")
    services.add_task(session, lst.id, "low one", None, "low")
    services.add_task(session, lst.id, "high one", None, "high")
    services.add_task(session, lst.id, "medium one", None, "medium")

    rows = services.list_tasks(session, lst.id, sort="priority")
    assert [t["priority"] for t in rows] == ["high", "medium", "low"]


def test_list_tasks_sort_by_due_date_nulls_last(session):
    lst = services.create_list(session, "Deadlines")
    services.add_task(session, lst.id, "no date", None, "medium")
    services.add_task(session, lst.id, "later", date(2026, 12, 1), "medium")
    services.add_task(session, lst.id, "soon", date(2026, 5, 10), "medium")

    rows = services.list_tasks(session, lst.id, sort="due_date")
    assert [t["content"] for t in rows] == ["soon", "later", "no date"]


def test_export_all_round_trips_through_json(session):
    lst = services.create_list(session, "Inbox")
    services.add_task(session, lst.id, "Hello", date(2026, 1, 1), "medium")

    payload = services.export_all(session)
    assert "exported_at" in payload
    assert len(payload["lists"]) == 1
    assert payload["lists"][0]["name"] == "Inbox"
    assert len(payload["lists"][0]["tasks"]) == 1
    assert payload["lists"][0]["tasks"][0]["content"] == "Hello"
    assert payload["lists"][0]["tasks"][0]["due_date"] == "2026-01-01T00:00:00"

    reloaded = json.loads(json.dumps(payload))
    assert reloaded["lists"][0]["tasks"][0]["content"] == "Hello"
