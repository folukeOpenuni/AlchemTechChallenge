from graphene import ObjectType, String, Field, List, Mutation, Int, DateTime
import graphene
import sqlite3

# Define the function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('event_log.db')
    conn.row_factory = sqlite3.Row  # Allow accessing columns by name
    return conn

# Define the EventType
class EventType(ObjectType):
    event_id = Int()
    event_type = String()
    event_status = String()
    event_datetime = DateTime()  # New field for event date and time
    priority = String()  # New field for priority
    category = String()  # New field for category
    timestamp = String()

# Update Query to return new fields
class Query(ObjectType):
    events = List(EventType, event_type=String(), event_status=String(), priority=String(), category=String())

    def resolve_events(self, info, event_type=None, event_status=None, priority=None, category=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM event_log"
        filters = []
        parameters = []

        if event_type:
            filters.append("event_type = ?")
            parameters.append(event_type)
        if event_status:
            filters.append("event_status = ?")
            parameters.append(event_status)
        if priority:
            filters.append("priority = ?")
            parameters.append(priority)
        if category:
            filters.append("category = ?")
            parameters.append(category)

        if filters:
            query += " WHERE " + " AND ".join(filters)

        cursor.execute(query, tuple(parameters))
        rows = cursor.fetchall()
        conn.close()

        return [EventType(event_id=row['event_id'], event_type=row['event_type'], event_status=row['event_status'],
                          event_datetime=row['event_datetime'], priority=row['priority'], category=row['category'],
                          timestamp=row['timestamp']) for row in rows]

# Define Mutation for inserting events with new fields
class CreateEvent(Mutation):
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

        event = EventType(event_id=event_id, event_type=event_type, event_status=event_status,
                          priority=priority, category=category, event_datetime="Now")
        return CreateEvent(ok="Event created successfully", event=event)

# Define Mutation class
class Mutation(ObjectType):
    create_event = CreateEvent.Field()

# Create a schema
schema = graphene.Schema(query=Query, mutation=Mutation)
