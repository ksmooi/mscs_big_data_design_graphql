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
    DgraphClient manages interactions with the Dgraph GraphQL API.
    It includes methods for querying, mutating, and subscribing to the GraphQL endpoint.
    """
    def __init__(self, graphql_endpoint='http://localhost:8080/graphql'):
        self.graphql_endpoint = graphql_endpoint
        self.stop_event = asyncio.Event()

    def query(self, query, variables=None):
        """
        Executes a GraphQL query.
        
        :param query: The GraphQL query string.
        :param variables: Optional variables for the query.
        :return: JSON response from the API.
        """
        response = requests.post(self.graphql_endpoint, json={'query': query, 'variables': variables})
        return response.json()

    def mutate(self, mutation, variables=None):
        """
        Executes a GraphQL mutation.
        
        :param mutation: The GraphQL mutation string.
        :param variables: Optional variables for the mutation.
        :return: JSON response from the API.
        """
        response = requests.post(self.graphql_endpoint, json={'query': mutation, 'variables': variables})
        return response.json()

    async def subscribe(self, subscription, variables=None):
        """
        Subscribes to a GraphQL subscription.
        
        :param subscription: The GraphQL subscription string.
        :param variables: Optional variables for the subscription.
        """
        async with websockets.connect(self.graphql_endpoint.replace("http", "ws"), subprotocols=["graphql-ws"]) as websocket:
            payload = json.dumps({
                'type': 'connection_init',
                'payload': {}
            })
            await websocket.send(payload)
            await websocket.recv()

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

    def add_order(self, order_id, member_id, product_ids, total, date):
        """
        Adds an order using the addOrder mutation.
        
        :param order_id: The order ID.
        :param member_id: The member ID.
        :param product_ids: List of product IDs.
        :param total: The total amount.
        :param date: The date of the order.
        :return: JSON response from the API.
        """
        mutation = """
        mutation AddOrder($input: [AddOrderInput!]!, $upsert: Boolean) {
          addOrder(input: $input, upsert: $upsert) {
            order {
              orderId
              member {
                memberId
                name
                email
              }
              products {
                productId
                name
                price
                category
              }
              total
              date
            }
            numUids
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
            }],
            "upsert": True
        }
        return self.mutate(mutation, variables)

    def update_order(self, order_id, total):
        """
        Updates an order using the updateOrder mutation.
        
        :param order_id: The order ID.
        :param total: The new total amount.
        :return: JSON response from the API.
        """
        mutation = """
        mutation UpdateOrder($filter: OrderFilter!, $set: OrderPatch!) {
          updateOrder(input: {filter: $filter, set: $set}) {
            order {
              orderId
              member {
                memberId
                name
                email
              }
              products {
                productId
                name
                price
                category
              }
              total
              date
            }
            numUids
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

    def delete_review(self, review_id):
        """
        Deletes a review using the deleteReview mutation.
        
        :param review_id: The review ID.
        :return: JSON response from the API.
        """
        mutation = """
        mutation DeleteReview($filter: ReviewFilter!) {
          deleteReview(filter: $filter) {
            review {
              reviewId
              rating
              comment
              member {
                memberId
                name
                email
              }
              product {
                productId
                name
                price
                category
              }
              date
            }
            msg
            numUids
          }
        }
        """
        variables = {
            "filter": {
                "reviewId": {
                    "eq": review_id
                }
            }
        }
        return self.mutate(mutation, variables)

    def stop(self):
        """
        Signals to stop the subscription.
        """
        self.stop_event.set()

# Usage example
if __name__ == '__main__':
    client = DgraphClient()

    def signal_handler(signal, frame):
        print("Caught Ctrl+C, stopping...")
        client.stop()

    signal.signal(signal.SIGINT, signal_handler)

    # Example usage
    async def main():
        # Add an order
        order_id = "order-" + datetime.now().strftime("%Y%m%d%H%M%S")
        response = client.add_order(order_id, '1', ['1', '2'], 200.0, datetime.now())
        print("Add Order Response:\n", response, "\n")

        # Update the order
        response = client.update_order(order_id, 250.0)
        print("Update Order Response:\n", response, "\n")

        # Delete a review
        response = client.delete_review("review-1")
        print("Delete Review Response:\n", response, "\n")

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
