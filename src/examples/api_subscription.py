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
from datetime import datetime

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

    def mutate(self, mutation, variables=None):
        """
        Perform a GraphQL mutation.

        :param mutation: The GraphQL mutation string.
        :param variables: Optional variables for the mutation.
        :return: The response from the GraphQL API.
        """
        response = requests.post(self.graphql_endpoint, json={'query': mutation, 'variables': variables})
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

    def insert_order(self, order_id, member_id, product_ids, total, date):
        """
        Insert a new order.

        :param order_id: The unique ID of the order.
        :param member_id: The ID of the member placing the order.
        :param product_ids: A list of product IDs included in the order.
        :param total: The total amount of the order.
        :param date: The date of the order.
        :return: The response from the GraphQL API.
        """
        mutation = """
        mutation AddOrder($input: [AddOrderInput!]!) {
          addOrder(input: $input) {
            order {
              orderId
              total
              date
              member {
                memberId
              }
              products {
                productId
              }
            }
          }
        }
        """
        variables = {
            "input": [{
                "orderId": order_id,
                "member": {"memberId": member_id},
                "products": [{"productId": pid} for pid in product_ids],
                "total": total,
                "date": date.isoformat()
            }]
        }
        return self.mutate(mutation, variables)

    def update_order(self, order_id, total):
        """
        Update an existing order.

        :param order_id: The unique ID of the order.
        :param total: The new total amount of the order.
        :return: The response from the GraphQL API.
        """
        mutation = """
        mutation UpdateOrder($filter: OrderFilter!, $set: OrderPatch!) {
          updateOrder(input: {filter: $filter, set: $set}) {
            order {
              orderId
              total
              date
            }
          }
        }
        """
        variables = {
            "filter": {
                "orderId": {
                    "eq": order_id
                }
            },
            "set": {
                "total": total
            }
        }
        return self.mutate(mutation, variables)

    def stop(self):
        """
        Stop the subscription.
        """
        self.stop_event.set()

# Usage example
if __name__ == '__main__':
    client = DgraphClient()

    def signal_handler(signal, frame):
        """
        Signal handler to stop the client gracefully on Ctrl+C.
        """
        print("Caught Ctrl+C, stopping...")
        client.stop()

    signal.signal(signal.SIGINT, signal_handler)

    # Example subscription usage
    async def run_subscription():
        """
        Run a GraphQL subscription to listen for real-time updates.
        """
        # Example subscription for queryOrder
        subscription_query_order = """
        subscription {
          queryOrder {
            orderId
            total
            date
            member {
              memberId
            }
            products {
              productId
            }
          }
        }
        """

        # Example subscription for getOrder with filter by member
        subscription_query_order_filter_member = """
        subscription($memberId: String!) {
          queryOrder(filter: {member: {memberId: {eq: $memberId}}}) {
            orderId
            total
            date
            member {
              memberId
            }
            products {
              productId
            }
          }
        }
        """

        # Example subscription for getOrder with filter by product category
        subscription_query_order_filter_product_category = """
        subscription($category: String!) {
          queryOrder(filter: {products: {category: {eq: $category}}}) {
            orderId
            total
            date
            member {
              memberId
            }
            products {
              productId
              category
            }
          }
        }
        """

        # Example subscription for queryOrder with filter by date
        subscription_query_order_filter_date = """
        subscription($startDate: DateTime!, $endDate: DateTime!) {
          queryOrder(filter: {date: {between: {min: $startDate, max: $endDate}}}) {
            orderId
            total
            date
            member {
              memberId
            }
            products {
              productId
              category
            }
          }
        }
        """

        # Example subscription for queryOrder with filter and order by total
        subscription_query_order_filter_order_total = """
        subscription($minTotal: Float!) {
          queryOrder(filter: {total: {ge: $minTotal}}, order: {asc: total}) {
            orderId
            total
            date
            member {
              memberId
            }
            products {
              productId
              category
            }
          }
        }
        """

        # Example subscription for queryOrder with filter, order, first, and offset
        subscription_query_order_pagination = """
        subscription($minTotal: Float!) {
          queryOrder(filter: {total: {ge: $minTotal}}, order: {asc: total}, first: 10, offset: 5) {
            orderId
            total
            date
            member {
              memberId
            }
            products {
              productId
              category
            }
          }
        }
        """

        # Choose one of the above subscription queries to use
        subscription_query = subscription_query_order

        # Use appropriate variables if needed
        variables = None
        # variables = {"memberId": "1"}
        # variables = {"category": "Beauty"}
        # variables = {"startDate": "2024-01-01T00:00:00Z", "endDate": "2024-12-31T23:59:59Z"}
        # variables = {"minTotal": 100.0}

        await client.subscribe(subscription_query, variables)

    loop = asyncio.get_event_loop()

    def stop_loop():
        """
        Stop the event loop and cancel all tasks.
        """
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.stop()

    loop.add_signal_handler(signal.SIGINT, stop_loop)

    async def main():
        """
        Main function to run the example usage.
        """
        # Start subscription
        subscription_task = loop.create_task(run_subscription())

        # Add an order
        order_id = "order-" + datetime.now().strftime("%Y%m%d%H%M%S")
        response = client.insert_order(order_id, '1', ['1'], 100.0, datetime.now())
        print("Add Order Response:\n", response, "\n")

        await asyncio.sleep(5)  # Wait a bit to ensure the subscription catches the add event

        # Modify the order
        response = client.update_order(order_id, 150.0)
        print("Update Order Response:\n", response, "\n")

        await asyncio.sleep(5)  # Wait a bit to ensure the subscription catches the update event

        # Stop subscription
        client.stop()
        await subscription_task

    try:
        loop.run_until_complete(main())
    except asyncio.CancelledError:
        print("Task was cancelled")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("Event loop closed")
