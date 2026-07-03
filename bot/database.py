import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                name TEXT,
                project_type TEXT,
                description TEXT,
                contact TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def add_request(user_id, username, name, project_type, description, contact):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO requests (user_id, username, name, project_type, description, contact) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, username, name, project_type, description, contact)
        )
        await db.commit()
        return cursor.lastrowid


async def get_request(request_id):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM requests WHERE id = ?", (request_id,))
        return await cursor.fetchone()


async def get_recent_requests(limit=10):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM requests ORDER BY created_at DESC LIMIT ?", (limit,))
        return await cursor.fetchall()


async def get_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM requests")
        total = (await cursor.fetchone())[0]

        cursor = await db.execute("SELECT COUNT(*) FROM requests WHERE created_at >= date('now')")
        today = (await cursor.fetchone())[0]

        cursor = await db.execute("SELECT COUNT(*) FROM requests WHERE created_at >= date('now', '-7 days')")
        week = (await cursor.fetchone())[0]

        cursor = await db.execute("SELECT COUNT(*) FROM requests WHERE created_at >= date('now', '-30 days')")
        month = (await cursor.fetchone())[0]

        return {"total": total, "today": today, "week": week, "month": month}
