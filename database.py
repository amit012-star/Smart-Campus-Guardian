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
