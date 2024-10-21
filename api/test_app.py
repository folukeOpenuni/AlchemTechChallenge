from flask_graphql import GraphQLView
import unittest
import json
from api.app import app, schema  # Ensure schema is imported

class TestGraphQLAPI(unittest.TestCase):

    def setUp(self):
        # Create a test client for Flask
        self.app = app.test_client()
        self.app.testing = True

        # Add GraphQL route to the app in testing
        app.add_url_rule(
            '/graphql',
            view_func=GraphQLView.as_view(
                'graphql',
                schema=schema, graphiql=True
            )
        )

    def test_add_multiple_events(self):
        # Mutation to add events
        mutation_query = '''
        mutation {
          add_event(event_type: "INFO", event_status: "SUCCESS", priority: "HIGH", category: "ERROR") {
            ok
          }
        }
        '''

        # Add first event
        response = self.app.post('/graphql', json={'query': mutation_query})
        
        # Debug: print the raw response for inspection
        print(f"Raw response for the first event: {response.data.decode('utf-8')}")  
        
        # Parse the response as JSON
        data = json.loads(response.data.decode('utf-8'))
        print(f"Parsed data for the first event: {data}")  # Debugging line

        # Ensure the response has a valid status code
        self.assertEqual(response.status_code, 200)

        # Ensure 'data' exists in the response
        self.assertIsNotNone(data, "Response data is None")
        self.assertIn('data', data, "No 'data' field in response")
        self.assertIn('add_event', data['data'], "No 'add_event' field in response")

        # Verify the value of the 'ok' field
        self.assertEqual(data['data']['add_event']['ok'], 'Event added successfully')


if __name__ == '__main__':
    unittest.main()
