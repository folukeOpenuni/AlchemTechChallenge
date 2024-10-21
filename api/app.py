from flask import Flask, request, jsonify
from graphene import ObjectType, String, Int, Field, List, Schema, Mutation as BaseMutation
import sqlite3

import graphene

# Initialize Flask app
app = Flask(__name__)

# Define the SQLite database connection
def get_db_connection():
    conn = sqlite3.connect('event_log.db')
    conn.row_factory = sqlite3.Row  # This allows us to access rows as dictionaries
    return conn

# Define the EventType for GraphQL
class EventType(ObjectType):
    event_id = Int()
    event_type = String()
    event_status = String()
    event_datetime = String()
    priority = String()
    category = String()

# Define the Query class to get events
class Query(ObjectType):
    events = List(EventType)

    def resolve_events(self, info):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM event_log")
        rows = cursor.fetchall()
        conn.close()

        return [EventType(
            event_id=row['event_id'],
            event_type=row['event_type'],
            event_status=row['event_status'],
            event_datetime=row['event_datetime'],
            priority=row['priority'],
            category=row['category']
        ) for row in rows]

# Define Mutation class to add events
class AddEvent(graphene.Mutation):
    class Arguments:
        event_type = String(required=True)
        event_status = String(required=True)
        priority = String(required=True)
        category = String(required=True)

    ok = String()
    event = Field(lambda: EventType)

    def mutate(self, info, event_type, event_status, priority, category):
        print(f"Received Mutation: event_type={event_type}, event_status={event_status}, priority={priority}, category={category}")
        
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Insert event into the database
            cursor.execute('''
                INSERT INTO event_log (event_type, event_status, priority, category)
                VALUES (?, ?, ?, ?)
            ''', (event_type, event_status, priority, category))

            conn.commit()
            event_id = cursor.lastrowid
            print(f"Inserted Event with ID: {event_id}")

            event = EventType(
                event_id=event_id,
                event_type=event_type,
                event_status=event_status,
                event_datetime="Now",
                priority=priority,
                category=category
            )

            return AddEvent(ok="Event added successfully", event=event)

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return AddEvent(ok="Failed to add event", event=None)

        except Exception as e:
            print(f"Other error: {e}")
            return AddEvent(ok="Failed to add event", event=None)

        finally:
            conn.close()

# Define the Mutation class
class Mutation(graphene.ObjectType):
    add_event = AddEvent.Field()

# Create a schema for GraphQL
# schema = Schema(query=Query, mutation=Mutation)
schema = graphene.Schema(query=Query, mutation=Mutation)


# Set up Flask route to handle GraphQL requests
@app.route("/graphql", methods=["POST"])
def graphql():
    data = request.get_json()
    result = schema.execute(data.get("query"))
    return jsonify(result.data)

@app.route("/test_db")
def test_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Try inserting a test event into the database
        cursor.execute('''
            INSERT INTO event_log (event_type, event_status, priority, category)
            VALUES (?, ?, ?, ?)
        ''', ('TEST_TYPE', 'TEST_STATUS', 'HIGH', 'TEST_CATEGORY'))

        conn.commit()
        return "Event added successfully!"
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()


# Define a route for the root URL to avoid 404
@app.route('/')
def index():
    return "Welcome to the GraphQL API"

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
