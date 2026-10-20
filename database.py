import sqlite3


class TriangleDatabase:
    """Класс работы с БД (SQLite)."""

    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                a REAL NOT NULL,
                b REAL NOT NULL,
                c REAL NOT NULL,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (a, b, c)
            )
        """)
        self.conn.commit()

    def add(self, a, b, c, triangle_type, error_message):
        try:
            self.conn.execute(
                "INSERT OR REPLACE INTO triangles VALUES (?, ?, ?, ?, ?)",
                (a, b, c, triangle_type, error_message),
            )
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def get(self, a, b, c):
        cur = self.conn.execute(
            "SELECT triangle_type, error_message FROM triangles "
            "WHERE a = ? AND b = ? AND c = ?",
            (a, b, c),
        )
        row = cur.fetchone()
        return row  # None, если записи нет; иначе кортеж (тип, ошибка)

    def delete(self, a, b, c):
        cur = self.conn.execute(
            "DELETE FROM triangles WHERE a = ? AND b = ? AND c = ?",
            (a, b, c),
        )
        self.conn.commit()
        return cur.rowcount > 0

    def close(self):
        self.conn.close()