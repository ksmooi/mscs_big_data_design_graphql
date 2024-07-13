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

class AnalysisAPI:
    """
    A class to interact with various analysis-related GraphQL API endpoints.
    """
    def __init__(self, client):
        """
        Initialize the AnalysisAPI with the provided DgraphClient.
        """
        self.client = client

    # Customer Behavior Analysis
    def customer_segmentation(self):
        """
        Group customers based on purchasing behavior, demographics, or interactions.
        """
        query = """
        query CustomerSegmentation {
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
        return self.client.query(query)

    def customer_lifetime_value(self):
        """
        Calculate the projected revenue a customer will generate over their relationship with the business.
        """
        query = """
        query CustomerLifetimeValue {
            queryMember {
                memberId
                orders {
                    total
                    date
                }
            }
        }
        """
        return self.client.query(query)

    def churn_analysis(self):
        """
        Identify customers at risk of leaving and understand factors contributing to churn.
        """
        query = """
        query ChurnAnalysis {
            queryMember {
                memberId
                orders {
                    orderId
                    date
                }
                reviews {
                    rating
                }
            }
        }
        """
        return self.client.query(query)

    def customer_journey_analysis(self):
        """
        Map out and analyze the customer's journey from discovery to purchase to improve the shopping experience.
        """
        query = """
        query CustomerJourneyAnalysis {
            queryMember {
                memberId
                orders {
                    orderId
                    date
                    products {
                        productId
                    }
                }
                reviews {
                    reviewId
                    date
                }
            }
        }
        """
        return self.client.query(query)

    def personalized_marketing(self):
        """
        Create targeted marketing campaigns based on customer preferences and behavior.
        """
        query = """
        query PersonalizedMarketing {
            queryMember {
                memberId
                recommendedProducts {
                    productId
                }
            }
        }
        """
        return self.client.query(query)

    # Product Performance and Feedback Analysis
    def product_performance_analysis(self):
        """
        Evaluate product sales performance, customer satisfaction, and identify top-performing products.
        """
        query = """
        query ProductPerformanceAnalysis {
            queryProduct {
                productId
                name
                price
                reviews {
                    reviewId
                }
                orders {
                    orderId
                }
            }
        }
        """
        return self.client.query(query)

    def review_sentiment_analysis(self):
        """
        Analyze customer feedback to understand product strengths and areas for improvement.
        """
        query = """
        query ReviewSentimentAnalysis {
            queryReview {
                reviewId
                rating
                comment
                product {
                    productId
                }
            }
        }
        """
        return self.client.query(query)

    # Sales and Promotion Analysis
    def sales_trend_analysis(self):
        """
        Identify sales patterns and seasonal trends to optimize inventory and marketing efforts.
        """
        query = """
        query SalesTrendAnalysis {
            queryOrder {
                orderId
                total
                date
                products {
                    productId
                }
            }
        """
        return self.client.query(query)

    def promotion_effectiveness_analysis(self):
        """
        Evaluate the impact of promotions and discounts on sales and customer acquisition.
        """
        query = """
        query PromotionEffectivenessAnalysis {
            queryOrder {
                orderId
                total
                date
                products {
                    productId
                }
            }
        """
        return self.client.query(query)

    def cross_sell_upsell_analysis(self):
        """
        Identify opportunities to recommend complementary or higher-value products.
        """
        query = """
        query CrossSellUpsellAnalysis {
            queryOrder {
                orderId
                products {
                    productId
                }
            }
            queryMember {
                memberId
                recommendedProducts {
                    productId
                }
            }
        }
        """
        return self.client.query(query)

    # Recommendation System Analysis
    def recommendation_effectiveness(self):
        """
        Assess the impact of recommendations on sales and customer engagement.
        """
        query = """
        query RecommendationEffectiveness {
            queryMember {
                memberId
                recommendedProducts {
                    productId
                }
            }
            queryOrder {
                orderId
                products {
                    productId
                }
            }
        }
        """
        return self.client.query(query)

    # Inventory and Demand Analysis
    def market_basket_analysis(self):
        """
        Identify products frequently bought together to optimize cross-selling and upselling strategies.
        """
        query = """
        query MarketBasketAnalysis {
            queryOrder {
                orderId
                products {
                    productId
                }
            }
        }
        """
        return self.client.query(query)

    def inventory_optimization(self):
        """
        Ensure optimal stock levels to meet demand without overstocking.
        """
        query = """
        query InventoryOptimization {
            queryOrder {
                products {
                    productId
                }
                date
            }
        }
        """
        return self.client.query(query)

    def demand_forecasting(self):
        """
        Predict future demand for products to inform supply chain and marketing decisions.
        """
        query = """
        query DemandForecasting {
            queryOrder {
                orderId
                total
                date
                products {
                    productId
                }
            }
        }
        """
        return self.client.query(query)

# Usage example
if __name__ == '__main__':
    client = DgraphClient()
    analysis_api = AnalysisAPI(client)

    def signal_handler(signal, frame):
        """
        Handle SIGINT signal to gracefully stop the client.
        """
        print("Caught Ctrl+C, stopping...")
        client.stop()

    signal.signal(signal.SIGINT, signal_handler)

    async def main():
        # Example usage
        response = analysis_api.customer_segmentation()
        print("Customer Segmentation Response:\n", response, "\n")

        response = analysis_api.customer_lifetime_value()
        print("Customer Lifetime Value (CLV) Analysis Response:\n", response, "\n")

        response = analysis_api.churn_analysis()
        print("Churn Analysis Response:\n", response, "\n")

        response = analysis_api.customer_journey_analysis()
        print("Customer Journey Analysis Response:\n", response, "\n")

        response = analysis_api.personalized_marketing()
        print("Personalized Marketing Response:\n", response, "\n")

        response = analysis_api.product_performance_analysis()
        print("Product Performance Analysis Response:\n", response, "\n")

        response = analysis_api.review_sentiment_analysis()
        print("Review Sentiment Analysis Response:\n", response, "\n")

        response = analysis_api.sales_trend_analysis()
        print("Sales Trend Analysis Response:\n", response, "\n")

        response = analysis_api.promotion_effectiveness_analysis()
        print("Promotion Effectiveness Analysis Response:\n", response, "\n")

        response = analysis_api.cross_sell_upsell_analysis()
        print("Cross-Sell and Upsell Analysis Response:\n", response, "\n")

        response = analysis_api.recommendation_effectiveness()
        print("Recommendation Effectiveness Response:\n", response, "\n")

        response = analysis_api.market_basket_analysis()
        print("Market Basket Analysis Response:\n", response, "\n")

        response = analysis_api.inventory_optimization()
        print("Inventory Optimization Response:\n", response, "\n")

        response = analysis_api.demand_forecasting()
        print("Demand Forecasting Response:\n", response, "\n")

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
        """
        Stop the event loop and cancel all tasks.
        """
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
