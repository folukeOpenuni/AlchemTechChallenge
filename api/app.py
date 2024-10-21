from flask import Flask
from graphene import ObjectType, String, Int, Field, List
from graphene import Schema
from flask_graphql import GraphQLView
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
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO event_log (event_type, event_status, priority, category)
            VALUES (?, ?, ?, ?)
        ''', (event_type, event_status, priority, category))

        conn.commit()
        event_id = cursor.lastrowid
        conn.close()

        event = EventType(
            event_id=event_id,
            event_type=event_type,
            event_status=event_status,
            event_datetime="Now",
            priority=priority,
            category=category
        )
        return AddEvent(ok="Event added successfully", event=event)

# Define Mutation class
class Mutation(ObjectType):
    add_event = AddEvent.Field()

# Create a schema for GraphQL
schema = Schema(query=Query, mutation=Mutation)

# Set up Flask app to use GraphQL
app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True  # Enable GraphiQL interface
))

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
