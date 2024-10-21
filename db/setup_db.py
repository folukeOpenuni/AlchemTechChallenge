import sqlite3

# Connect to SQLite database (this will create the file if it doesn't exist)
conn = sqlite3.connect('event_log.db')
cursor = conn.cursor()

# Create the event_log table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_log (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        event_status TEXT NOT NULL,
        event_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
        priority TEXT NOT NULL,
        category TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table 'event_log' created successfully.")
