# Backend Lab

This folder is the standalone FastAPI practice project.

## Structure

```text
app/
  main.py                 Application entry point
  api/routes/             HTTP route modules
database.py               Existing SQLAlchemy experiment
dbconnection.py           Existing raw psycopg2 experiment
models.py                 Existing SQLAlchemy model experiment
```

The application entry point is `app.main:app`. The root-level Python files are
kept as learning experiments and are not imported by the application.

## Run

```powershell
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.