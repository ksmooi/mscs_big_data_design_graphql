# Create and activate a virtual environment
# ------------------------------------------------------------------
# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install responses
# python -m unittest utest_dgraph_client.py
# deactivate

import unittest
import responses

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

# Now you can import DgraphClient
from analysis_engine import DgraphClient

class TestDgraphClient(unittest.TestCase):
    def setUp(self):
        self.client = DgraphClient('http://localhost:8080/graphql')

    @responses.activate
    def test_query_success(self):
        # Mock the GraphQL response
        responses.add(
            responses.POST,
            'http://localhost:8080/graphql',
            json={'data': {'queryMember': [{'memberId': '1', 'name': 'John Doe', 'email': 'john.doe@example.com'}]}},
            status=200
        )

        # Define the GraphQL query
        query = """
        query {
            queryMember {
                memberId
                name
                email
            }
        }
        """

        # Execute the query
        response = self.client.query(query)

        # Assert the response
        self.assertEqual(response, {
            'data': {
                'queryMember': [{'memberId': '1', 'name': 'John Doe', 'email': 'john.doe@example.com'}]
            }
        })

    @responses.activate
    def test_query_failure(self):
        # Mock the GraphQL error response
        responses.add(
            responses.POST,
            'http://localhost:8080/graphql',
            json={'errors': [{'message': 'Some error occurred'}]},
            status=200
        )

        # Define the GraphQL query
        query = """
        query {
            queryMember {
                memberId
                name
                email
            }
        }
        """

        # Execute the query
        response = self.client.query(query)

        # Assert the response contains errors
        self.assertIn('errors', response)
        self.assertEqual(response['errors'][0]['message'], 'Some error occurred')

    @responses.activate
    def test_query_network_error(self):
        # Mock a network error
        responses.add(
            responses.POST,
            'http://localhost:8080/graphql',
            body=Exception('Network error')
        )

        # Define the GraphQL query
        query = """
        query {
            queryMember {
                memberId
                name
                email
            }
        }
        """

        # Execute the query and assert an exception is raised
        with self.assertRaises(Exception) as context:
            self.client.query(query)

        self.assertTrue('Network error' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
