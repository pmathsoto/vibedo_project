# VibeDo — Build Transcript

A faithful transcript of the prompts and responses that produced VibeDo in 60 minutes of coding with **Claude Opus 4.7**, preceded by 3 minutes of prompt engineering with **Gemini Pro (reasoning)** to refine the meta-prompt that drove the build.

User prompts are quoted verbatim. Assistant responses are condensed for readability — tool-call narration is trimmed, but the substantive explanations and the actual code that was produced are preserved.

---

# Pre-build phase — Prompt engineering with Gemini

The 57-minute coding sprint was preceded by ~3 minutes of meta-prompt engineering with **Gemini**. The goal was to refine the prompt that would later produce the per-phase Master Prompts driving the actual build with Claude. Two Gemini sessions were used: a quick pass with **Gemini 3 Fast** to sharpen the meta-prompt, and a longer pass with **Gemini 3 Pro** to generate (and then revise) the action plan.

---

## Gemini Turn G1 — Gemini 3 Fast: sharpen the meta-prompt

### Prompt

> help me improve this prompt:
>
> You are a project structuring expert tasked with creating an action plan for a web app. Based on the instructions provided, you will generate the best prompts for top-tier AIs for each section, aiming to support building the app using 'vibe-coding.' Note that you the team have a limited timeframe of 60 minutes to complete the app construction and you need to wait the instructions to create the action plan.

### Response

Gemini reframed the prompt as a "World-Class Project Architect and Prompt Engineer" role with explicit Vibe-Coding scope, and returned an improved version:

> **Role:** You are a World-Class Project Architect and Prompt Engineer specializing in "Vibe-Coding" (rapid, natural language-driven development using tools like Replit Agent, Lovable, or Cursor).
>
> **Objective:** Create a high-velocity 60-minute action plan for building a web app. You will break the project into 4-5 logical phases (e.g., Wireframing, Core Logic, Styling, Deployment).
>
> **Requirements for the Action Plan:**
> - **Phase Breakdown:** For each phase, provide a timestamp (e.g., 0-10 mins).
> - **Optimized AI Prompts:** For every phase, write a "Master Prompt" designed for a top-tier LLM. These prompts must be specific, use technical shorthand to save tokens/time, and focus on generating "MVP" (Minimum Viable Product) code.
> - **Vibe-Coding Strategy:** Include instructions on how to iterate quickly—specifically what to tell the AI when bugs occur or when the "vibe" isn't hitting the mark.
> - **Constraints:** Assume a total build time of 60 minutes. Prioritize functionality over perfect polish.
>
> **Process:** Acknowledge this role. I will then provide the App Concept. Once received, you will generate the full Action Plan and the specific prompts.

**Key improvements Gemini called out:**

- **Defined "Vibe-Coding"** as natural-language-driven development to stop the AI from interpreting "vibe" literally as visual styling.
- **Structured phases** with explicit timestamps to enforce the 60-minute budget.
- **"Master Prompts"** instead of "best prompts" — specific, technical-shorthand, MVP-focused.
- **Iteration logic** — explicit guidance for when bugs hit or the vibe drifts.
- **Acknowledge-then-wait pattern** — the AI confirms its role first, then waits for the App Concept.

Closing pro-tip: *"specify which stack you prefer (e.g., 'React with Tailwind' or 'Python/Streamlit') ... this prevents the AI from wasting 10 minutes suggesting a stack you aren't comfortable with."*

---

## Gemini Turn G2 — Gemini 3 Pro: role acknowledgement

### Prompt

The full improved prompt from Turn G1 above.

### Response

> Acknowledged. Architect mode: Engaged.
>
> Vibe-coding isn't about writing code; it's about orchestrating intent. When we have 60 minutes, we don't have time for boilerplate or bikeshedding over button gradients. We move fast, leverage "Happy Path" logic, and pivot the moment the AI drifts.
>
> My methodology focuses on Context-Stacking: providing the AI with enough architectural "flavor" to make smart decisions without overwhelming the token limit.
>
> I am ready to architect your MVP. What is the App Concept?

---

## Gemini Turn G3 — Gemini 3 Pro: app concept → 60-minute action plan

### Prompt

> Your objective is to create a TODO or Checklist app, for personal use by an individual locally on one machine. It should have functionality similar to Microsoft ToDo, RememberTheMilk, etc., but you should feel free to be creative with any features you might find useful. Don't spend time on graphics or the slickness of the UI. It should be a "real" app in the sense of, e.g., having a persistent data store of some kind, such that a real person could use it over a period of time.
>
> Our preference would be for a webapp using a Python backend or a Python-based full-stack framework like Streamlit. However, you are free to use any language or architecture you like (e.g. a C#-based desktop app).
>
> Your app should be runnable at minimum on a Linux/OSX-based machine. Supporting additional platforms like Windows is great too. You may assume that the user has access to Docker and any other common tools you might want to use.
>
> Note that you are certainly allowed to hand-edit any files (e.g. to conform filenames to the expectations below), but it's expected that most of the code will be written by the AI.
>
> **Deliverables**
>
> You should send a single Zip file containing:
>
> - A `metadata.txt` listing
>   - How long you spent on the exercise
>   - What AI tool(s) you used
>   - Any other information relevant to the evaluation. For example, further changes you were intending to make but ran out of time to do.
> - The transcript of your conversation with the AI. (You may edit this to remove any sensitive information like passwords, but note where you do so.)
> - The codebase, which should contain
>   - The app code itself, including tests
>   - a `README.md` explaining how to run and use the app. You should list any prerequisites (e.g. Docker), but need not describe how to install them.
>   - a `.github/workflows/CI.yml` file, which runs all the available linting and tests upon branch push. This should run on a standard Github ubuntu runner.
>
> (Alternatively, you can set up an actual Github repo and provide the link to it.)
>
> **Evaluation**
>
> Your output will be evaluated based on
>
> - Amount of functionality
> - Lack of bugs
> - Architecture & code quality
> - Amount/quality of linting/tests
> - Clarity/completeness of documentation
> - Effective use of AI (e.g. prompt quality).

### Response

Gemini chose **Streamlit + SQLite** as the stack — *"fastest path from 'idea' to 'UI + Database' without getting bogged down in CSS or complex state management"* — and produced a 4-phase plan:

| Phase | Time | Focus |
|---|---|---|
| 1: Scaffolding | 0–10m | DB Schema (SQLAlchemy) & basic Streamlit layout |
| 2: Core CRUD | 10–30m | Create, Read, Update, Delete + List Management |
| 3: The "Vibe" | 30–45m | Smart features (NL dates, priority tagging) |
| 4: Ship-Ready | 45–60m | Dockerfile, CI/CD, Unit Tests |

**Master Prompts (initial version):**

> **Phase 1 — Data Foundation (0-10 mins):**
> "Build a Python Streamlit app called 'VibeDo'. Use SQLAlchemy with SQLite for persistence. Create a schema for Lists (id, name) and Tasks (id, list_id, content, due_date, status, priority, created_at). Setup a db.py for session handling and app.py for the UI. The UI should have a sidebar to switch between Lists and a 'Create New List' button. Output the file structure and the initial connection code. Keep it MVP."
>
> **Phase 2 — Core Logic & CRUD (10-30 mins):**
> "Inside app.py, implement full CRUD for tasks. Users should be able to: 1. Add tasks to the current list. 2. Mark tasks as complete (checkbox). 3. Delete tasks. 4. Edit task content inline. Use st.expander or st.columns for a clean layout. Ensure that checking a box immediately updates the SQLite DB. Add a 'Clear Completed' button. Show a progress bar for the current list (% of tasks done)."
>
> **Phase 3 — Feature Injection (30-45 mins):**
> "Let's add 'Smart' features. 1. Add a priority dropdown (Low, Medium, High) with color-coding. 2. Implement a simple search bar at the top to filter tasks across all lists. 3. Feature: 'Daily Focus'—a special view that pulls all tasks due today. 4. If a user types a date like 'Friday' in the task input, use python-dateutil to parse it into the due_date field automatically. Refactor app.py to handle these."
>
> **Phase 4 — Hardening & Devops (45-60 mins):**
> "Finalize for production. 1. Create a requirements.txt. 2. Write a Dockerfile using python:3.11-slim. 3. Write a test_db.py using pytest to verify task creation and completion logic. 4. Generate a .github/workflows/CI.yml that installs deps, runs black linting, and executes pytest. 5. Write a README.md with setup instructions. Ensure all files are ready for a Zip export."

**Vibe-Coding Strategy** (mid-build tactical "Vibe-Shifters"):

- **Bug:** *"Fix [Error Name] in db.py. It's likely a session state conflict. Keep the fix minimal."*
- **UI looks off:** *"The layout is too cluttered. Move the list management to a modal or use st.sidebar more effectively. Clean up the padding."*
- **Context Reset:** *"Act as a Senior Python Architect. Strip the boilerplate. We are using Streamlit—use its native state management (st.session_state) instead of over-engineering."*

**Deliverable preparation:**

- Linting: *"Review all generated code for PEP8 compliance and add docstrings to the main functions."*
- Tests: ensure a `conftest.py` exists for DB mocks so CI doesn't fail on a locked file.

---

## Gemini Turn G4 — Gemini 3 Pro: revise feature set

### Prompt

> change the features 1 and 3 of the feature injection master prompt. Add other simple coding functionalities

### Response

Gemini swapped the original "Priority dropdown" and "Daily Focus" for **Cross-List Tagging** and **Visual Productivity Analytics**, and added **Markdown Notes** and **JSON Export** as power-user coding utilities. The revised Phase-3 Master Prompt:

> **Phase 3 — Revised Feature Injection (30-45 mins):**
> "Upgrade VibeDo with these 'Power User' features:
> 1. **Multi-Tagging:** Add a text input for comma-separated tags (stored as a string/JSON). Create a sidebar filter to show tasks with specific tags across all lists.
> 2. **Markdown Notes:** Render the task 'Note' field using st.markdown() so users can include links or code snippets.
> 3. **Productivity Analytics:** Add an 'Insights' tab. Use st.bar_chart to show a count of completed tasks per day for the last 7 days.
> 4. **Data Portability:** Add a 'Backup' button in the sidebar that exports the entire database (Lists + Tasks) as a downloadable JSON file.
> 5. **Natural Language Dates:** Use python-dateutil to parse inputs like 'tomorrow' or 'next Monday' into the due_date field."

The revised Phase 1 Master Prompt was also tightened (adding a `note` column to Tasks, scoped session handling, `st.session_state` for the active list), and the Phase-4 deployment prompt explicitly required: `requirements.txt`, `Dockerfile` (`python:3.11-slim`), 3-4 pytest functions, GitHub Actions CI (flake8/black + pytest), and a `README.md` ensuring *"the app handles a missing DB file by creating it on startup."*

**Additional Vibe-Coding troubleshooters:**

- **"State Glitch":** *"Implement st.form for task creation with clear_on_submit=True to stabilize the UI state."*
- **"DB Locked" Error:** *"Ensure the SQLAlchemy engine uses check_same_thread=False and that sessions are properly closed using a context manager."*
- **"Visual Vibe" Check:** *"Format tags as st.caption or use small colored badges (custom HTML/CSS) to make them look like real UI elements."*

> **Note on what carried over to the build:** the prompts that were actually sent to Claude Opus 4.7 in the coding phase below mirror Gemini's revised plan very closely — Phase 1's prompt is reproduced verbatim, Phase 2's CRUD prompt is reproduced verbatim, Phase 3's prompt was forwarded with items **2, 3, and 4** (Markdown Notes / Analytics / JSON Backup) and items **1 and 5** (Multi-Tagging and Natural Language Dates) dropped, and Phase 4 was forwarded almost verbatim. The "sort by priority / due date" feature added later in the coding phase was an ad-hoc addition outside the original plan.

---

# Coding phase — Claude Opus 4.7 (60-minute sprint)

The thirteen turns that follow are the actual conversation with Claude Opus 4.7 that produced the codebase, driven by the planning artifacts generated above.

---

## Turn 1 — Initial scaffold

### Prompt

> Build a Python Streamlit app called 'VibeDo'. Use SQLAlchemy with SQLite for persistence. Create a schema for Lists (id, name) and Tasks (id, list_id, content, due_date, status, priority, created_at). Setup a db.py for session handling and app.py for the UI. The UI should have a sidebar to switch between Lists and a 'Create New List' button. Output the file structure and the initial connection code. Keep it MVP.

### Response

Created the project under `/Users/paco/vibedo/` with this layout:

```
vibedo/
├── app.py            # Streamlit UI (sidebar lists + create new list)
├── db.py             # Engine, SessionLocal, init_db, get_session()
├── models.py         # SQLAlchemy ORM: List, Task
├── requirements.txt  # streamlit, SQLAlchemy
└── vibedo.db         # created on first run
```

**`models.py`** — SQLAlchemy ORM:

```python
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class List(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    tasks = relationship(
        "Task",
        back_populates="list",
        cascade="all, delete-orphan",
        order_by="Task.created_at.desc()",
    )


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey("lists.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    due_date = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default="open")
    priority = Column(String(20), nullable=False, default="medium")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    list = relationship("List", back_populates="tasks")
```

**`db.py`** — engine on `sqlite:///vibedo.db`, `SessionLocal` factory, `get_session()` context manager that commits on success / rolls back on exception / always closes; `init_db()` calls `Base.metadata.create_all`.

**`app.py`** — Streamlit page config, sidebar with list radio + "+ Create New List" expander form, empty-state hint in the main pane.

To run:

```bash
cd vibedo
pip install -r requirements.txt
streamlit run app.py
```

---

## Turn 2 — Full task CRUD

### Prompt

> Inside app.py, implement full CRUD for tasks. Users should be able to: 1. Add tasks to the current list. 2. Mark tasks as complete (checkbox). 3. Delete tasks. 4. Edit task content inline. Use st.expander or st.columns for a clean layout. Ensure that checking a box immediately updates the SQLite DB. Add a 'Clear Completed' button. Show a progress bar for the current list (% of tasks done)

### Response

Rewrote `app.py` with the full CRUD layer.

**Key additions:**

- **Add** — form with content / due date / priority columns, calls `add_task()` and reruns.
- **Complete** — `st.checkbox` per row with `on_change=toggle_status`. Toggling commits to SQLite immediately (Streamlit fires the callback before the next render).
- **Delete** — 🗑 button per row.
- **Inline edit** — open tasks render as `st.text_input` bound to `on_change=commit_edit`; pressing Enter or blurring saves. Done tasks render as struck-through markdown.
- **Priority / due date** — also inline-editable selectbox + date input.

**Progress + Clear Completed:**

```python
st.progress(pct, text=f"{done}/{total} done ({pct * 100:.0f}%)")
if st.button("🧹 Clear Completed", disabled=done == 0):
    clear_completed(selected)
    st.rerun()
```

`clear_completed()` runs a single bulk DELETE filtered by `status == "done"`.

Layout: 4-column row per task `[checkbox | content | priority+due | delete]`.

**Note on rerun ordering:** checkbox / text-edit callbacks use `on_change`, which Streamlit runs *before* the next script execution — so the DB write happens, then the UI re-reads fresh state on rerun. No `st.rerun()` needed inside those callbacks.

---

## Turn 3 — Colored priority and overdue dates

### Prompt

> Add some improvements:
>
> * The priority color needs to change by the value of it. Example: if its high priority, then its RED. If its medium then is YELLOW (etc.)
> * If the date is overdue, then it needs to be RED

### Response

Streamlit's stock `selectbox` / `date_input` can't be styled per row, so I swapped them for popovers whose **labels** carry the color — a single visual element per field that doubles as the editor.

```python
PRIORITY_EMOJI = {"high": "🔴", "medium": "🟡", "low": "🟢"}
PRIORITY_COLOR = {"high": "red", "medium": "orange", "low": "green"}

def priority_label(p: str) -> str:
    return f"{PRIORITY_EMOJI[p]} :{PRIORITY_COLOR[p]}[**{p.title()}**]"

def due_label(d, status: str) -> str:
    if d is None:
        return "📅 Set date"
    if status != STATUS_DONE and d < date.today():
        return f":red[⚠ {d.isoformat()}]"
    return f"📅 {d.isoformat()}"
```

The 🟡 emoji gives true yellow (Streamlit's native colored-text palette has orange but no yellow, so emoji + orange text together read as yellow).

Done tasks aren't flagged red even when their date is past — once a task is complete, "overdue" no longer applies.

---

## Turn 4 — Power-user features (notes, insights, backup)

### Prompt

> Upgrade VibeDo with these 'Power User' features:
>
> 1. Markdown Notes: Render the task 'Note' field using st.markdown() so users can include links or code snippets.
> 2. Productivity Analytics: Add an 'Insights' tab. Use st.bar_chart to show a count of completed tasks per day for the last 7 days.
> 3. Data Portability: Add a 'Backup' button in the sidebar that exports the entire database (Lists + Tasks) as a downloadable JSON file.

### Response

**Schema upgrade.** Added two columns to `Task`:

```python
notes = Column(Text, nullable=True)
completed_at = Column(DateTime, nullable=True)
```

Plus an inline migration in `db.py` so existing `vibedo.db` files don't need to be wiped:

```python
def _ensure_columns() -> None:
    expected = {"notes": "TEXT", "completed_at": "DATETIME"}
    with engine.begin() as conn:
        existing = {
            row[1] for row in conn.exec_driver_sql("PRAGMA table_info(tasks)").fetchall()
        }
        for name, sql_type in expected.items():
            if name not in existing:
                conn.exec_driver_sql(f"ALTER TABLE tasks ADD COLUMN {name} {sql_type}")
```

**Markdown notes.** Each task got a `📝 Notes` expander with two nested tabs — **View** renders `st.markdown(t["notes"])`, **Edit** is a `st.text_area` bound to `commit_notes` via `on_change` for autosave. The expander label gets a "•" badge when notes exist.

**Insights tab.** Wrapped the main pane in `st.tabs(["📋 Tasks", "📊 Insights"])`. The Insights tab shows:

```python
def completion_counts(list_id, days=7):
    today = date.today()
    start = today - timedelta(days=days - 1)
    # query Task.completed_at >= start, status == done
    # bucket by date, zero-fill missing days
```

Then `st.bar_chart` of date × completed plus three KPI metrics (total / daily average / best day). `toggle_status` was updated to set `completed_at = datetime.utcnow()` on check and clear it on uncheck.

**JSON backup.**

```python
def export_all() -> dict:
    return {
        "exported_at": datetime.utcnow().isoformat() + "Z",
        "lists": [...],  # walks Lists -> Tasks, ISO timestamps
    }

st.download_button(
    "💾 Backup (JSON)",
    data=json.dumps(export_all(), indent=2),
    file_name=f"vibedo-backup-{date.today().isoformat()}.json",
    mime="application/json",
)
```

---

## Turn 5 — Deployment prep (Dockerfile, tests, CI, README)

### Prompt

> Prepare for deployment:
>
> * Dockerfile: Use python:3.11-slim.
> * test_app.py: Write 3-4 pytest functions for DB operations (create task, toggle status, export JSON).
> * .github/workflows/CI.yml: Standard Python lint (flake8/black) and pytest runner on Ubuntu.
> * README.md: Concise instructions on running via Docker or pip install. Ensure the app handles a missing DB file by creating it on startup.

### Response

To make DB code testable without booting Streamlit, I extracted pure DB ops into a new `services.py` module that takes a `Session` parameter. `app.py`'s helpers became thin one-liners that delegate (`with get_session() as s: services.foo(s, ...)`).

Also made the DB URL configurable via `VIBEDO_DB_URL` so Docker can mount a volume:

```python
DATABASE_URL = os.getenv("VIBEDO_DB_URL", "sqlite:///vibedo.db")
```

**`test_app.py`** — 4 pytest functions against an in-memory SQLite via a fixture:

1. `test_create_list_and_task` — list + task creation, defaults
2. `test_toggle_status_sets_and_clears_completed_at` — round-trip done/open with `completed_at` lifecycle
3. `test_clear_completed_only_removes_done` — bulk delete leaves open tasks alone
4. `test_export_all_round_trips_through_json` — every datetime is JSON-serializable

**`Dockerfile`:**

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8501 \
    VIBEDO_DB_URL=sqlite:////data/vibedo.db

VOLUME /data
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

**`.github/workflows/CI.yml`** — checkout → setup-python 3.11 (with pip cache) → install dev reqs → `black --check .` → `flake8 .` → `pytest -q`.

Plus `README.md`, `pyproject.toml` (black config, line-length 100), `.flake8` (matching), `requirements-dev.txt`, `.dockerignore`.

The "missing DB file is created on startup" requirement was already satisfied by SQLite + `Base.metadata.create_all`; the README calls it out explicitly.

---

## Turn 6 — Sortable tasks

### Prompt

> If its possible, create a option that can sort the tasks by priority, date of conclusion (etc.).

### Response

Added a sort dropdown in the Tasks-tab header with four options:

```python
SORT_LABELS = {
    "default": "Newest",
    "priority": "Priority",
    "due_date": "Due date",
    "content": "A → Z",
}
```

Ordering is built in `services._ordering(sort)`. **Open tasks always come before done** — the chosen key is the secondary order:

```python
def _ordering(sort: str):
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
        null_last = case((Task.due_date.is_(None), 1), else_=0)
        return (primary, null_last, Task.due_date.asc(), Task.created_at.desc())
    if sort == "content":
        return (primary, Task.content.asc())
    return (primary, Task.created_at.desc())
```

Priority sort uses a SQL `CASE` to rank high→medium→low (alphabetical would be wrong). Due-date sort uses a `CASE` to push NULL dates to the end — portable across SQLite versions.

The selectbox key is `f"sort_{list_id}"`, so each list remembers its own sort across reruns.

Two more tests added to `test_app.py` (priority sort + due-date NULLs-last), bringing the suite to **6 tests**.

---
