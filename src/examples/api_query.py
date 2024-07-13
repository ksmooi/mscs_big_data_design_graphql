# Create and activate a virtual environment
# ------------------------------------------------------------------
# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install requests websockets
# deactivate

import json
import signal
import asyncio
import requests
import websockets

class DgraphClient:
    """
    A client class to interact with Dgraph's GraphQL API.
    It supports querying, mutating, and subscribing to real-time updates.
    """
    def __init__(self, graphql_endpoint='http://localhost:8080/graphql'):
        """
        Initialize the DgraphClient with the provided GraphQL endpoint.
        """
        self.graphql_endpoint = graphql_endpoint
        self.stop_event = asyncio.Event()

    def query(self, query, variables=None):
        """
        Perform a GraphQL query.

        :param query: The GraphQL query string.
        :param variables: Optional variables for the query.
        :return: The response from the GraphQL API.
        """
        response = requests.post(self.graphql_endpoint, json={'query': query, 'variables': variables})
        return response.json()

    async def subscribe(self, subscription, variables=None):
        """
        Perform a GraphQL subscription using WebSockets.

        :param subscription: The GraphQL subscription string.
        :param variables: Optional variables for the subscription.
        """
        async with websockets.connect(self.graphql_endpoint.replace("http", "ws"), subprotocols=["graphql-ws"]) as websocket:
            # Initialize the WebSocket connection
            payload = json.dumps({
                'type': 'connection_init',
                'payload': {}
            })
            await websocket.send(payload)
            await websocket.recv()

            # Start the subscription
            payload = json.dumps({
                'id': '1',
                'type': 'start',
                'payload': {
                    'query': subscription,
                    'variables': variables
                }
            })
            await websocket.send(payload)
            
            try:
                while not self.stop_event.is_set():
                    response = await websocket.recv()
                    print(response)
            except websockets.ConnectionClosed:
                pass

    def stop(self):
        """
        Stop the subscription.
        """
        self.stop_event.set()

    async def run_subscription(self, subscription_query, variables=None):
        """
        Run the subscription with the provided query and variables.

        :param subscription_query: The GraphQL subscription query string.
        :param variables: Optional variables for the subscription.
        """
        await self.subscribe(subscription_query, variables)

class MemberAPI:
    """
    A class to interact with Member-related GraphQL API endpoints.
    """
    def __init__(self, client):
        """
        Initialize the MemberAPI with the provided DgraphClient.
        """
        self.client = client

    def get_member(self, member_id):
        """
        Get a member by their ID.

        :param member_id: The ID of the member.
        :return: The response from the GraphQL API.
        """
        query = """
        {
          getMember(memberId: "%s") {
            memberId
            name
            email
            orders {
              orderId
              total
              date
            }
            reviews {
              reviewId
              rating
              comment
            }
          }
        }
        """ % member_id
        return self.client.query(query)

    def get_member_by_order_total(self, member_id, total):
        """
        Get a member by their order total.

        :param member_id: The ID of the member.
        :param total: The minimum order total to filter by.
        :return: The response from the GraphQL API.
        """
        query = """
        {
          getMember(memberId: "%s") {
            memberId
            name
            email
            orders(filter: {total: {gt: %d}}) {
              orderId
              total
              date
            }
          }
        }
        """ % (member_id, total)
        return self.client.query(query)

    def get_member_by_review_rating(self, member_id, rating):
        """
        Get a member by their review rating.

        :param member_id: The ID of the member.
        :param rating: The minimum review rating to filter by.
        :return: The response from the GraphQL API.
        """
        query = """
        {
          getMember(memberId: "%s") {
            memberId
            name
            email
            reviews(filter: {rating: {ge: %s}}) {
              reviewId
              rating
              comment
            }
          }
        }
        """ % (member_id, rating)
        return self.client.query(query)

    def query_members(self):
        """
        Query all members.

        :return: The response from the GraphQL API.
        """
        query = """
        {
          queryMember {
            memberId
            name
            email
          }
        }
        """
        return self.client.query(query)

    def query_members_by_order_date(self, start_date, end_date):
        """
        Query members by order date range.

        :param start_date: The start date of the range.
        :param end_date: The end date of the range.
        :return: The response from the GraphQL API.
        """
        query = """
        {
          queryMember {
            memberId
            name
            email
            orders(filter: {date: {between: {min: "%s", max: "%s"}}}) {
              orderId
              total
              date
            }
          }
        }
        """ % (start_date, end_date)
        return self.client.query(query)

    def query_members_with_order_avg(self):
        """
        Query members with the average order total.

        :return: The response from the GraphQL API.
        """
        query = """
        {
          queryMember {
            memberId
            name
            email
            ordersAggregate {
              totalAvg
            }
          }
        }
        """
        return self.client.query(query)

    def query_members_with_review_count(self):
        """
        Query members with the count of reviews.

        :return: The response from the GraphQL API.
        """
        query = """
        {
          queryMember {
            memberId
            name
            email
            reviewsAggregate {
              count
            }
          }
        }
        """
        return self.client.query(query)

    def query_members_with_pagination(self, filter_name, order_field, first, offset):
        """
        Query members with pagination.

        :param filter_name: The name to filter by.
        :param order_field: The field to order by.
        :param first: The number of results to return.
        :param offset: The offset for pagination.
        :return: The response from the GraphQL API.
        """
        query = """
        {
          queryMember(filter: {name: {anyofterms: "%s"}}, order: {asc: %s}, first: %d, offset: %d) {
            memberId
            name
            email
          }
        }
        """ % (filter_name, order_field, first, offset)
        return self.client.query(query)

# Usage example
if __name__ == '__main__':
    client = DgraphClient()
    member_api = MemberAPI(client)

    def signal_handler(signal, frame):
        print("Caught Ctrl+C, stopping...")
        client.stop()

    signal.signal(signal.SIGINT, signal_handler)

    async def main():
        # Example usage
        response = member_api.get_member("7")
        print("Get Member Response:\n", response, "\n")

        response = member_api.get_member_by_order_total("6", 10)
        print("Get Member by Order Total Response:\n", response, "\n")

        response = member_api.get_member_by_review_rating("2", 3)
        print("Get Member by Review Rating Response:\n", response, "\n")

        response = member_api.query_members()
        print("Query Members Response:\n", response, "\n")

        response = member_api.query_members_by_order_date("2023-01-01", "2023-12-31")
        print("Query Members by Order Date Response:\n", response, "\n")

        response = member_api.query_members_with_order_avg()
        print("Query Members with Order Avg Response:\n", response, "\n")

        response = member_api.query_members_with_review_count()
        print("Query Members with Review Count Response:\n", response, "\n")

        response = member_api.query_members_with_pagination("@example.com", "email", 10, 5)
        print("Query Members with Pagination Response:\n", response, "\n")

        # Start subscription example
        subscription_query = """
        subscription {
          queryMember {
            memberId
            name
            email
            orders {
              orderId
            }
            reviews {
              reviewId
            }
          }
        }
        """
        await client.run_subscription(subscription_query)

    loop = asyncio.get_event_loop()

    def stop_loop():
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.stop()

    loop.add_signal_handler(signal.SIGINT, stop_loop)

    try:
        loop.run_until_complete(main())
    except asyncio.CancelledError:
        print("Task was cancelled")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("Event loop closed")
