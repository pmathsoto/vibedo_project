# VibeDo

A minimalist Streamlit todo app: lists, tasks with priority and due dates, markdown notes, completion analytics, JSON backup. Backed by SQLite + SQLAlchemy.

## Features

- Multiple lists with sidebar switcher
- Task CRUD with inline editing, completion checkbox, and per-row delete
- Priority badges colored red / yellow / green
- Due dates highlighted red when overdue
- Markdown-rendered notes per task
- **Insights** tab with a 7-day completion bar chart
- One-click JSON backup of the entire database

## Run with Docker

```bash
docker build -t vibedo .
docker run --rm -p 8501:8501 -v "$(pwd)/data:/data" vibedo
```

Open <http://localhost:8501>. The SQLite database lives at `./data/vibedo.db` on the host and is created automatically on first start.

## Run with pip

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

`vibedo.db` is created in the working directory on first launch — no migration step needed. Schema upgrades (e.g. new columns) are applied on startup via a small `ALTER TABLE` check in `db.py`.

## Configuration

| Env var | Default | Description |
|---|---|---|
| `VIBEDO_DB_URL` | `sqlite:///vibedo.db` | SQLAlchemy URL for the database |

The Docker image sets `VIBEDO_DB_URL=sqlite:////data/vibedo.db` so the DB persists in the mounted `/data` volume.

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

Tests run against an in-memory SQLite DB and exercise `services.py` directly — no Streamlit runtime needed.

## Lint / format

```bash
black .
flake8 .
```

Both run in CI on every push and pull request via `.github/workflows/CI.yml`.

## Project layout

```
.
├── app.py                       # Streamlit UI
├── services.py                  # Pure DB operations (testable)
├── db.py                        # Engine + session + auto-migration + env var
├── models.py                    # SQLAlchemy ORM
├── test_app.py                  # 6 pytest functions
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml               # black config (line-length 100)
├── .flake8                      # flake8 config (matching)
├── .dockerignore
├── README.md
├── TRANSCRIPT.md                # this file — full Gemini + Claude prompt log
├── vibedo.db                    # auto-created on first run
└── .github/workflows/CI.yml     # black --check + flake8 + pytest
```
