"""
pytest configuration and shared fixtures
"""
import os
import sqlite3
import tempfile
from pathlib import Path

import pytest

# Import Flask app (adjust if needed)
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app, init_db


@pytest.fixture
def client():
    """Create Flask test client with temporary database"""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()

    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def auth_client(client):
    """Create authenticated test client"""
    os.environ['SECRET_KEY'] = 'test-secret-key'
    # Login first
    client.get('/', environ_base={'HTTP_COOKIE': 'key=test-secret-key'})
    return client


@pytest.fixture
def db():
    """Provide database connection for tests"""
    db_fd, db_path = tempfile.mkstemp()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('''
        CREATE TABLE IF NOT EXISTS homeworks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            hw_type TEXT,
            done BOOLEAN DEFAULT 0,
            priority TEXT DEFAULT '中',
            due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    yield conn

    conn.close()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def sample_homework(db):
    """Insert sample homework for testing"""
    cursor = db.execute('''
        INSERT INTO homeworks (title, subject, hw_type, due_date, priority)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Test Homework', 'ENG', '功課', '2025-03-25', '高'))
    db.commit()
    return cursor.lastrowid
