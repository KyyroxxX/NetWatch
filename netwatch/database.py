import sqlite3
from contextlib import closing
from pathlib import Path


DB_DIR = Path("data")
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "netwatch.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    with closing(get_connection()) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host TEXT NOT NULL,
                reachable INTEGER NOT NULL,
                latency_ms REAL,
                packet_loss INTEGER NOT NULL,
                timestamp REAL NOT NULL
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_measurements_host
            ON measurements(host)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_measurements_timestamp
            ON measurements(timestamp)
        """)

        connection.commit()


def save_measurement(result):
    with closing(get_connection()) as connection:
        connection.execute("""
            INSERT INTO measurements (
                host, reachable, latency_ms, packet_loss, timestamp
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            result.host,
            int(result.reachable),
            result.latency_ms,
            result.packet_loss,
            result.timestamp,
        ))

        connection.commit()


def get_host_summary(host):
    with closing(get_connection()) as connection:
        row = connection.execute("""
            SELECT
                COUNT(*) AS total_checks,
                COALESCE(
                    SUM(CASE WHEN reachable = 0 THEN 1 ELSE 0 END),
                    0
                ) AS failures,
                MIN(latency_ms) AS min_latency,
                MAX(latency_ms) AS max_latency,
                AVG(latency_ms) AS avg_latency
            FROM measurements
            WHERE host = ?
        """, (host,)).fetchone()

        return row


def get_recent_measurements(limit=20):
    if limit < 1:
        raise ValueError("Limit must be greater than zero")

    with closing(get_connection()) as connection:
        rows = connection.execute("""
            SELECT host, reachable, latency_ms, timestamp
            FROM measurements
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return rows
