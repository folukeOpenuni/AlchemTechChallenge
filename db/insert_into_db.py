import sqlite3

def insert_event(event_type, event_status, priority, category):
    # Connect to the database
    conn = sqlite3.connect('event_log.db')
    conn.row_factory = sqlite3.Row  # Allows us to access rows as dictionaries
    cursor = conn.cursor()

    # Insert the event into the event_log table
    try:
        cursor.execute('''
            INSERT INTO event_log (event_type, event_status, priority, category)
            VALUES (?, ?, ?, ?)
        ''', (event_type, event_status, priority, category))

        # Commit the transaction
        conn.commit()
        print(f"Inserted event with ID: {cursor.lastrowid}")

    except sqlite3.Error as e:
        print(f"Error inserting into database: {e}")

    finally:
        conn.close()

# Insert multiple events
insert_event('INFO', 'SUCCESS', 'HIGH', 'ERROR')
insert_event('WARNING', 'PENDING', 'MEDIUM', 'SYSTEM')
insert_event('CRITICAL', 'FAILED', 'LOW', 'SECURITY')
