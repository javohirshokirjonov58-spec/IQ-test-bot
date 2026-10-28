"""
SQLite ma'lumotlar bazasi boshqaruvi.
Foydalanuvchilar, test natijalari va umumiy reytingni saqlaydi.
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any

DB_PATH = "iq_bot.db"


def init_db(db_path: str = DB_PATH):
    """Baza jadvallarini yaratish."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Foydalanuvchilar jadvali
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Test natijalari jadvali
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                score INTEGER,
                total INTEGER,
                iq INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
            )
        """)
        
        conn.commit()


def register_user(telegram_id: int, username: Optional[str], full_name: str, db_path: str = DB_PATH):
    """Foydalanuvchini ro'yxatdan o'tkazish yoki yangilash."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (telegram_id, username, full_name)
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                username = excluded.username,
                full_name = excluded.full_name
        """, (telegram_id, username, full_name))
        conn.commit()


def save_result(telegram_id: int, score: int, total: int, iq: int, db_path: str = DB_PATH):
    """Test natijasini saqlash."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO results (telegram_id, score, total, iq)
            VALUES (?, ?, ?, ?)
        """, (telegram_id, score, total, iq))
        conn.commit()


def get_user_stats(telegram_id: int, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Foydalanuvchining shaxsiy eng yaxshi va oxirgi natijalarini olish."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as attempts,
                MAX(iq) as best_iq,
                MAX(score) as best_score,
                AVG(score) as avg_score
            FROM results
            WHERE telegram_id = ?
        """, (telegram_id,))
        stats = cursor.fetchone()
        
        if not stats or stats["attempts"] == 0:
            return None
            
        cursor.execute("""
            SELECT score, total, iq, created_at
            FROM results
            WHERE telegram_id = ?
            ORDER BY id DESC
            LIMIT 1
        """, (telegram_id,))
        last = cursor.fetchone()
        
        return {
            "attempts": stats["attempts"],
            "best_iq": stats["best_iq"],
            "best_score": stats["best_score"],
            "avg_score": round(stats["avg_score"], 1),
            "last_iq": last["iq"] if last else None,
            "last_score": last["score"] if last else None,
            "last_date": last["created_at"] if last else None,
        }


def get_top_leaderboard(limit: int = 10, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Eng yuqori IQ natijalariga ega foydalanuvchilar reytingi."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                u.telegram_id,
                u.full_name,
                u.username,
                MAX(r.iq) as max_iq,
                MAX(r.score) as max_score,
                r.total
            FROM results r
            JOIN users u ON u.telegram_id = r.telegram_id
            GROUP BY u.telegram_id
            ORDER BY max_iq DESC, max_score DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_total_users_count(db_path: str = DB_PATH) -> int:
    """Jami foydalanuvchilar soni."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        row = cursor.fetchone()
        return row[0] if row else 0
