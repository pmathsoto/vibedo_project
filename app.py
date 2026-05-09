import json
from datetime import date, datetime

import streamlit as st

import services
from db import get_session, init_db

st.set_page_config(page_title="VibeDo", page_icon="✅", layout="wide")

init_db()

PRIORITIES = ["low", "medium", "high"]
STATUS_OPEN = "open"
STATUS_DONE = "done"

PRIORITY_EMOJI = {"high": "🔴", "medium": "🟡", "low": "🟢"}
PRIORITY_COLOR = {"high": "red", "medium": "orange", "low": "green"}

SORT_LABELS = {
    "default": "Newest",
    "priority": "Priority",
    "due_date": "Due date",
    "content": "A → Z",
}


def priority_label(p: str) -> str:
    return f"{PRIORITY_EMOJI[p]} :{PRIORITY_COLOR[p]}[**{p.title()}**]"


def due_label(d, status: str) -> str:
    if d is None:
        return "📅 Set date"
    if status != STATUS_DONE and d < date.today():
        return f":red[⚠ {d.isoformat()}]"
    return f"📅 {d.isoformat()}"


# --- Data helpers (thin wrappers around services) ---


def load_lists():
    with get_session() as s:
        return services.list_lists(s)


def create_list(name: str):
    with get_session() as s:
        services.create_list(s, name)


def load_tasks(list_id: int, sort: str = "default"):
    with get_session() as s:
        return services.list_tasks(s, list_id, sort=sort)


def add_task(list_id: int, content: str, due, priority: str):
    with get_session() as s:
        services.add_task(s, list_id, content, due, priority)


def update_task(task_id: int, **fields):
    with get_session() as s:
        services.update_task(s, task_id, **fields)


def delete_task(task_id: int):
    with get_session() as s:
        services.delete_task(s, task_id)


def clear_completed(list_id: int):
    with get_session() as s:
        services.clear_completed(s, list_id)


def toggle_status(task_id: int, checkbox_key: str):
    checked = st.session_state.get(checkbox_key, False)
    with get_session() as s:
        services.set_task_status(s, task_id, checked)


def commit_edit(task_id: int, edit_key: str):
    new_content = st.session_state.get(edit_key, "").strip()
    if new_content:
        with get_session() as s:
            services.update_task(s, task_id, content=new_content)


def commit_notes(task_id: int, notes_key: str):
    with get_session() as s:
        services.update_task(s, task_id, notes=st.session_state.get(notes_key, ""))


def completion_counts(list_id: int, days: int = 7):
    with get_session() as s:
        return services.completion_counts(s, list_id, days)


def export_all() -> dict:
    with get_session() as s:
        return services.export_all(s)


# --- Sidebar: list picker, create, backup ---

with st.sidebar:
    st.header("VibeDo")
    lists = load_lists()

    if lists:
        selected = st.radio(
            "Lists",
            options=[lid for lid, _ in lists],
            format_func=lambda lid: dict(lists)[lid],
            key="selected_list",
        )
    else:
        selected = None
        st.caption("No lists yet — create one below.")

    with st.expander("➕ Create New List", expanded=not lists):
        with st.form("new_list_form", clear_on_submit=True):
            new_name = st.text_input("List name")
            if st.form_submit_button("Create") and new_name.strip():
                create_list(new_name)
                st.rerun()

    st.divider()
    st.download_button(
        "💾 Backup (JSON)",
        data=json.dumps(export_all(), indent=2),
        file_name=f"vibedo-backup-{date.today().isoformat()}.json",
        mime="application/json",
        use_container_width=True,
    )

# --- Main pane ---

st.title("VibeDo")

if selected is None:
    st.info("Create a list from the sidebar to get started.")
    st.stop()

list_name = dict(lists)[selected]
tasks_tab, insights_tab = st.tabs(["📋 Tasks", "📊 Insights"])

with tasks_tab:
    h_left, h_sort, h_clear = st.columns([3, 1.5, 1.2])

    with h_sort:
        st.write("")
        sort_key = st.selectbox(
            "Sort",
            options=list(SORT_LABELS.keys()),
            format_func=lambda k: SORT_LABELS[k],
            key=f"sort_{selected}",
            label_visibility="collapsed",
        )

    tasks = load_tasks(selected, sort=sort_key)
    total = len(tasks)
    done = sum(1 for t in tasks if t["status"] == STATUS_DONE)
    pct = (done / total) if total else 0.0

    with h_left:
        st.subheader(list_name)
        st.progress(pct, text=f"{done}/{total} done ({pct * 100:.0f}%)")

    with h_clear:
        st.write("")
        if st.button("🧹 Clear Completed", disabled=done == 0, use_container_width=True):
            clear_completed(selected)
            st.rerun()

    with st.form("new_task_form", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns([5, 2, 2, 1])
        content = c1.text_input(
            "Task", placeholder="What needs doing?", label_visibility="collapsed"
        )
        due = c2.date_input("Due", value=None, label_visibility="collapsed")
        priority = c3.selectbox("Priority", PRIORITIES, index=1, label_visibility="collapsed")
        submitted = c4.form_submit_button("Add", use_container_width=True)
        if submitted and content.strip():
            add_task(selected, content, due, priority)
            st.rerun()

    st.divider()

    if not tasks:
        st.caption("No tasks yet. Add one above.")
    else:
        for t in tasks:
            check_key = f"check_{t['id']}"
            edit_key = f"edit_{t['id']}"
            prio_key = f"prio_{t['id']}"
            due_key = f"due_{t['id']}"
            notes_key = f"notes_{t['id']}"

            c_check, c_text, c_meta, c_del = st.columns([0.5, 5, 3, 0.7])

            with c_check:
                st.checkbox(
                    "done",
                    value=t["status"] == STATUS_DONE,
                    key=check_key,
                    label_visibility="collapsed",
                    on_change=toggle_status,
                    args=(t["id"], check_key),
                )

            with c_text:
                if t["status"] == STATUS_DONE:
                    st.markdown(f"~~{t['content']}~~")
                else:
                    st.text_input(
                        "content",
                        value=t["content"],
                        key=edit_key,
                        label_visibility="collapsed",
                        on_change=commit_edit,
                        args=(t["id"], edit_key),
                    )

            with c_meta:
                mc1, mc2 = st.columns(2)

                with mc1.popover(priority_label(t["priority"]), use_container_width=True):
                    new_prio = st.radio(
                        "Priority",
                        PRIORITIES,
                        index=PRIORITIES.index(t["priority"]),
                        key=prio_key,
                        horizontal=True,
                    )
                    if new_prio != t["priority"]:
                        update_task(t["id"], priority=new_prio)
                        st.rerun()

                with mc2.popover(due_label(t["due_date"], t["status"]), use_container_width=True):
                    new_due = st.date_input(
                        "Due date",
                        value=t["due_date"],
                        key=due_key,
                    )
                    new_due_dt = datetime.combine(new_due, datetime.min.time()) if new_due else None
                    current_due_dt = (
                        datetime.combine(t["due_date"], datetime.min.time())
                        if t["due_date"]
                        else None
                    )
                    if new_due_dt != current_due_dt:
                        update_task(t["id"], due_date=new_due_dt)
                        st.rerun()
                    if t["due_date"] and st.button(
                        "Clear date", key=f"cleardate_{t['id']}", use_container_width=True
                    ):
                        update_task(t["id"], due_date=None)
                        st.rerun()

            with c_del:
                if st.button("🗑", key=f"del_{t['id']}", help="Delete task"):
                    delete_task(t["id"])
                    st.rerun()

            notes_label = "📝 Notes" + (" •" if t["notes"] else "")
            with st.expander(notes_label):
                view_tab, edit_tab = st.tabs(["View", "Edit"])
                with view_tab:
                    if t["notes"]:
                        st.markdown(t["notes"])
                    else:
                        st.caption("No notes yet. Switch to Edit.")
                with edit_tab:
                    st.text_area(
                        "Notes (markdown supported)",
                        value=t["notes"],
                        key=notes_key,
                        on_change=commit_notes,
                        args=(t["id"], notes_key),
                        height=140,
                        label_visibility="collapsed",
                    )
                    st.caption("Supports markdown — links, **bold**, `code`, code blocks, lists.")

with insights_tab:
    st.subheader(f"Last 7 days — {list_name}")
    counts = completion_counts(selected, days=7)
    ordered_dates = sorted(counts)
    chart_data = {
        "date": [d.isoformat() for d in ordered_dates],
        "completed": [counts[d] for d in ordered_dates],
    }
    st.bar_chart(chart_data, x="date", y="completed", height=280)

    total_done = sum(counts.values())
    best_day = max(counts.items(), key=lambda kv: kv[1]) if counts else (None, 0)
    m1, m2, m3 = st.columns(3)
    m1.metric("Completed (7d)", total_done)
    m2.metric("Daily average", f"{total_done / 7:.1f}")
    m3.metric(
        "Best day",
        best_day[0].isoformat() if best_day[0] and best_day[1] else "—",
        f"{best_day[1]} done" if best_day[1] else None,
    )
    st.caption(
        "Counts only completions tracked after this feature was added "
        "(tasks completed earlier have no timestamp)."
    )
