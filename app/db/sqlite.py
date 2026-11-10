import sqlite3
from pathlib import Path
from datetime import datetime, timezone

class DocumentRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY, user_id TEXT NOT NULL,
                filename TEXT NOT NULL, pages INTEGER NOT NULL,
                chunks INTEGER NOT NULL, uploaded_at TEXT NOT NULL)""")
            c.execute("CREATE INDEX IF NOT EXISTS idx_documents_user ON documents(user_id)")
    def connect(self):
        c = sqlite3.connect(self.db_path)
        c.row_factory = sqlite3.Row
        return c
    def create(self, document_id, user_id, filename, pages, chunks):
        stamp = datetime.now(timezone.utc).isoformat()
        with self.connect() as c:
            c.execute("INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?)",
                      (document_id,user_id,filename,pages,chunks,stamp))
        return stamp
    def list_for_user(self, user_id):
        with self.connect() as c:
            rows = c.execute("SELECT * FROM documents WHERE user_id=? ORDER BY uploaded_at DESC",(user_id,)).fetchall()
        return [dict(r) for r in rows]
    def get_for_user(self, document_id, user_id):
        with self.connect() as c:
            row = c.execute("SELECT * FROM documents WHERE document_id=? AND user_id=?",(document_id,user_id)).fetchone()
        return dict(row) if row else None
    def delete_for_user(self, document_id, user_id):
        with self.connect() as c:
            cur = c.execute("DELETE FROM documents WHERE document_id=? AND user_id=?",(document_id,user_id))
        return cur.rowcount > 0
