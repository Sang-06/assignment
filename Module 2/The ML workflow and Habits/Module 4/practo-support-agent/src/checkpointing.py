import sqlite3
import json
import os

class SQLiteCheckpointSaver:
    """Persists LangGraph agent state transitions into a SQLite database."""
    
    def __init__(self, db_path: str = "data/checkpoints.sqlite"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    thread_id TEXT PRIMARY KEY,
                    state_json TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_checkpoint(self, thread_id: str, state: dict):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO checkpoints (thread_id, state_json)
                VALUES (?, ?)
            """, (thread_id, json.dumps(state)))
            conn.commit()

    def load_checkpoint(self, thread_id: str) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT state_json FROM checkpoints WHERE thread_id = ?", (thread_id,))
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return {}