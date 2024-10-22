from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import time
import threading
import random

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('event_log.db')
    conn.row_factory = sqlite3.Row  # return rows as dictionaries
    return conn

# Root route
@app.route('/')
def index():
    return "Welcome to the Event Log API!"

# Create an event
@app.route('/event', methods=['POST'])
def create_event():
    new_event = request.get_json()
    event_type = new_event['event_type']
    event_status = new_event['event_status']
    priority = new_event['priority']
    category = new_event['category']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO event_log (event_type, event_status, priority, category)
        VALUES (?, ?, ?, ?)
    ''', (event_type, event_status, priority, category))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Event created successfully'}), 201

# Get all events
@app.route('/events', methods=['GET'])
def get_events():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM event_log')
    events = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(event) for event in events])

# Get a single event by ID
@app.route('/event/<int:event_id>', methods=['GET'])
def get_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM event_log WHERE event_id = ?', (event_id,))
    event = cursor.fetchone()
    conn.close()
    
    if event:
        return jsonify(dict(event))
    else:
        return jsonify({'message': 'Event not found'}), 404

# Update an event by ID
@app.route('/event/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    updated_event = request.get_json()
    event_type = updated_event['event_type']
    event_status = updated_event['event_status']
    priority = updated_event['priority']
    category = updated_event['category']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE event_log
        SET event_type = ?, event_status = ?, priority = ?, category = ?
        WHERE event_id = ?
    ''', (event_type, event_status, priority, category, event_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Event updated successfully'})

# Delete an event by ID (Delete)
@app.route('/event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM event_log WHERE event_id = ?', (event_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Event deleted successfully'})

# Event simulator function
def generate_random_event():
    event_types = ['ERROR', 'WARNING', 'INFO', 'CRITICAL']
    event_statuses = ['PENDING', 'OPEN', 'CLOSED', 'FAILED']
    priorities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    categories = ['SYSTEM', 'SECURITY', 'APPLICATION', 'NETWORK']

    return {
        'event_type': random.choice(event_types),
        'event_status': random.choice(event_statuses),
        'priority': random.choice(priorities),
        'category': random.choice(categories),
    }

# Background thread to simulate events
def simulate_events():
    while True:
        event = generate_random_event()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO event_log (event_type, event_status, priority, category)
            VALUES (?, ?, ?, ?)
        ''', (event['event_type'], event['event_status'], event['priority'], event['category']))
        conn.commit()
        conn.close()

        print(f"Generated event: {event}")
        
        time.sleep(1200)  # Sleep for 2 min before generating another event

# Start the simulator thread when the Flask app starts
threading.Thread(target=simulate_events, daemon=True).start()
# Run the Flask app

if __name__ == '__main__':
    app.run(debug=True)
