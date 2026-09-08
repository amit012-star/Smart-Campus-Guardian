import sqlite3
import hashlib


def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def create_database():

    connection = sqlite3.connect("emergency.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            emergency_type TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Add location_details if it does not exist
    cursor.execute("PRAGMA table_info(emergencies)")
    columns = [column[1] for column in cursor.fetchall()]

    if "location_details" not in columns:
        cursor.execute("""
            ALTER TABLE emergencies
            ADD COLUMN location_details TEXT
        """)

    # Add assigned_team if it does not exist
    cursor.execute("PRAGMA table_info(emergencies)")
    columns = [column[1] for column in cursor.fetchall()]

    if "assigned_team" not in columns:
        cursor.execute("""
            ALTER TABLE emergencies
            ADD COLUMN assigned_team TEXT DEFAULT 'Unassigned'
        """)

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Student account
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        ("student",)
    )

    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users
            (username, password, role)
            VALUES (?, ?, ?)
        """, (
            "student",
            hash_password("1234"),
            "student"
        ))

    # Admin account
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        ("admin",)
    )

    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users
            (username, password, role)
            VALUES (?, ?, ?)
        """, (
            "admin",
            hash_password("admin123"),
            "admin"
        ))

    connection.commit()
    connection.close()


def authenticate_user(username, password):

    connection = sqlite3.connect("emergency.db")
    cursor = connection.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
        SELECT role
        FROM users
        WHERE username = ?
        AND password = ?
    """, (
        username,
        hashed_password
    ))

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None


def add_emergency(
    student_name,
    emergency_type,
    location,
    location_details,
    description,
    priority,
    status,
    created_at
):

    connection = sqlite3.connect("emergency.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO emergencies
        (
            student_name,
            emergency_type,
            location,
            location_details,
            description,
            priority,
            status,
            created_at,
            assigned_team
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_name,
        emergency_type,
        location,
        location_details,
        description,
        priority,
        status,
        created_at,
        "Unassigned"
    ))

    connection.commit()
    connection.close()


def get_emergencies():

    connection = sqlite3.connect("emergency.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            student_name,
            emergency_type,
            location,
            location_details,
            description,
            priority,
            status,
            created_at,
            assigned_team
        FROM emergencies
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data


def update_status(report_id, new_status):

    connection = sqlite3.connect("emergency.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE emergencies
        SET status = ?
        WHERE id = ?
    """, (
        new_status,
        report_id
    ))

    connection.commit()
    connection.close()


def assign_team(report_id, team):

    connection = sqlite3.connect("emergency.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE emergencies
        SET assigned_team = ?
        WHERE id = ?
    """, (
        team,
        report_id
    ))

    connection.commit()
    connection.close()
