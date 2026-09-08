import sqlite3


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

    # Check existing columns
    cursor.execute("PRAGMA table_info(emergencies)")
    columns = [column[1] for column in cursor.fetchall()]

    # Add location_details to old database
    if "location_details" not in columns:
        cursor.execute("""
            ALTER TABLE emergencies
            ADD COLUMN location_details TEXT
        """)

    connection.commit()
    connection.close()


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
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_name,
        emergency_type,
        location,
        location_details,
        description,
        priority,
        status,
        created_at
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
            created_at
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
    """, (new_status, report_id))

    connection.commit()
    connection.close()
