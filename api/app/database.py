import pyodbc
from contextlib import contextmanager
from app.config import settings

def get_connection() -> pyodbc.Connection:
    return pyodbc.connect(settings.connection_string)

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

def fetch_all(query: str, params: tuple = ()) -> list[dict]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def fetch_one(query: str, params: tuple = ()) -> dict | None:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        if row is None:
            return None
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))

def execute(query: str, params: tuple = ()) -> None:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

def check_health() -> bool:
    try:
        fetch_one("SELECT 1 AS ok")
        return True
    except Exception:
        return False
