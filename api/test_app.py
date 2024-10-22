import unittest
import json
from api.app import app

class EventLogTestCase(unittest.TestCase):
    
    def setUp(self):
        # Set up the Flask testing client
        self.app = app.test_client()
        self.app.testing = True

    def test_create_event(self):
        # Simulate a POST request to create a new event
        new_event = {
            "event_type": "Error",
            "event_status": "Open",
            "priority": "High",
            "category": "System"
        }
        response = self.app.post('/event', data=json.dumps(new_event), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Event created successfully', response.data)

    def test_get_events(self):
        # Simulate a GET request to fetch all events
        response = self.app.get('/events')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'event_type', response.data)  # Ensure event_type exists in response

    def test_get_single_event(self):
        # Simulate a GET request to fetch a single event by ID
        response = self.app.get('/event/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'event_type', response.data)

    def test_update_event(self):
        # Simulate a PUT request to update an event
        updated_event = {
            "event_type": "Warning",
            "event_status": "Closed",
            "priority": "Medium",
            "category": "System"
        }
        response = self.app.put('/event/1', data=json.dumps(updated_event), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Event updated successfully', response.data)

    def test_delete_event(self):
        # Simulate a DELETE request to delete an event
        response = self.app.delete('/event/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Event deleted successfully', response.data)

if __name__ == '__main__':
    unittest.main()
