from datetime import date, datetime, timedelta

from sqlalchemy import case
from sqlalchemy.orm import Session

from models import List as TodoList
from models import Task

STATUS_OPEN = "open"
STATUS_DONE = "done"

SORT_KEYS = ("default", "priority", "due_date", "content")


def _ordering(sort: str):
    """Build an ORDER BY tuple for list_tasks.

    Open tasks always come before done; the chosen sort is the secondary key.
    """
    primary = Task.status.asc()
    if sort == "priority":
        rank = case(
            (Task.priority == "high", 0),
            (Task.priority == "medium", 1),
            (Task.priority == "low", 2),
            else_=3,
        )
        return (primary, rank, Task.created_at.desc())
    if sort == "due_date":
        # NULL due dates last, then ascending by date.
        null_last = case((Task.due_date.is_(None), 1), else_=0)
        return (primary, null_last, Task.due_date.asc(), Task.created_at.desc())
    if sort == "content":
        return (primary, Task.content.asc())
    return (primary, Task.created_at.desc())


def list_lists(session: Session):
    rows = session.query(TodoList).order_by(TodoList.id.asc()).all()
    return [(r.id, r.name) for r in rows]


def create_list(session: Session, name: str) -> TodoList:
    lst = TodoList(name=name.strip())
    session.add(lst)
    session.flush()
    return lst


def list_tasks(session: Session, list_id: int, sort: str = "default"):
    rows = session.query(Task).filter(Task.list_id == list_id).order_by(*_ordering(sort)).all()
    return [
        {
            "id": t.id,
            "content": t.content,
            "notes": t.notes or "",
            "due_date": t.due_date.date() if t.due_date else None,
            "status": t.status,
            "priority": t.priority,
        }
        for t in rows
    ]


def add_task(
    session: Session,
    list_id: int,
    content: str,
    due,
    priority: str = "medium",
) -> Task:
    t = Task(
        list_id=list_id,
        content=content.strip(),
        due_date=datetime.combine(due, datetime.min.time()) if due else None,
        priority=priority,
        status=STATUS_OPEN,
    )
    session.add(t)
    session.flush()
    return t


def update_task(session: Session, task_id: int, **fields):
    task = session.get(Task, task_id)
    if task is None:
        return None
    for k, v in fields.items():
        setattr(task, k, v)
    return task


def set_task_status(session: Session, task_id: int, done: bool):
    return update_task(
        session,
        task_id,
        status=STATUS_DONE if done else STATUS_OPEN,
        completed_at=datetime.utcnow() if done else None,
    )


def delete_task(session: Session, task_id: int) -> bool:
    task = session.get(Task, task_id)
    if not task:
        return False
    session.delete(task)
    return True


def clear_completed(session: Session, list_id: int) -> int:
    return (
        session.query(Task)
        .filter(Task.list_id == list_id, Task.status == STATUS_DONE)
        .delete(synchronize_session=False)
    )


def completion_counts(session: Session, list_id: int, days: int = 7):
    today = date.today()
    start = today - timedelta(days=days - 1)
    rows = (
        session.query(Task.completed_at)
        .filter(
            Task.list_id == list_id,
            Task.status == STATUS_DONE,
            Task.completed_at.isnot(None),
            Task.completed_at >= datetime.combine(start, datetime.min.time()),
        )
        .all()
    )
    buckets = {start + timedelta(days=i): 0 for i in range(days)}
    for (dt,) in rows:
        d = dt.date()
        if d in buckets:
            buckets[d] += 1
    return buckets


def export_all(session: Session) -> dict:
    lists_data = []
    for lst in session.query(TodoList).order_by(TodoList.id.asc()).all():
        lists_data.append(
            {
                "id": lst.id,
                "name": lst.name,
                "tasks": [
                    {
                        "id": t.id,
                        "content": t.content,
                        "notes": t.notes,
                        "due_date": t.due_date.isoformat() if t.due_date else None,
                        "status": t.status,
                        "priority": t.priority,
                        "created_at": t.created_at.isoformat() if t.created_at else None,
                        "completed_at": t.completed_at.isoformat() if t.completed_at else None,
                    }
                    for t in lst.tasks
                ],
            }
        )
    return {"exported_at": datetime.utcnow().isoformat() + "Z", "lists": lists_data}
