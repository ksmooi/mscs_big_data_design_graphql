# Create and activate a virtual environment
# ------------------------------------------------------------------
# python3 -m venv myenv && source myenv/bin/activate

# Upgrade pip and install pydgraph
# ------------------------------------------------------------------
# pip install --upgrade pip && pip install requests pydgraph

import uuid
import json
import requests
from datetime import datetime

class DgraphDataInserter:
    """
    A class to insert data into Dgraph using GraphQL.
    
    Attributes:
    graphql_endpoint (str): The endpoint URL for the Dgraph GraphQL API.
    
    Methods:
    insert_member(member_id, name, email): Inserts a member into the database.
    insert_product(product_id, name, description, price, category): Inserts a product into the database.
    insert_order(order_id, member_id, product_ids, total, date): Inserts an order into the database.
    insert_review(review_id, rating, comment, member_id, product_id, date): Inserts a review into the database.
    """

    def __init__(self, graphql_endpoint='http://192.168.1.150:8080/graphql'):
        """
        Initializes the DgraphDataInserter with the GraphQL endpoint.
        
        Parameters:
        graphql_endpoint (str): The endpoint URL for the Dgraph GraphQL API.
        """
        self.graphql_endpoint = graphql_endpoint

    def insert_member(self, member_id, name, email):
        """
        Inserts a member into the database.
        
        Parameters:
        member_id (str): The unique identifier for the member.
        name (str): The name of the member.
        email (str): The email address of the member.
        
        Returns:
        dict: The JSON response from the Dgraph server.
        """
        mutation = """
        mutation AddMember($input: [AddMemberInput!]!) {
          addMember(input: $input) {
            member {
              memberId
              name
              email
            }
          }
        }
        """
        variables = {
            "input": [{
                "memberId": member_id,
                "name": name,
                "email": email
            }]
        }
        response = requests.post(self.graphql_endpoint, json={'query': mutation, 'variables': variables})
        return response.json()

    def insert_product(self, product_id, name, description, price, category):
        """
        Inserts a product into the database.
        
        Parameters:
        product_id (str): The unique identifier for the product.
        name (str): The name of the product.
        description (str): The description of the product.
        price (float): The price of the product.
        category (str): The category to which the product belongs.
        
        Returns:
        dict: The JSON response from the Dgraph server.
        """
        mutation = """
        mutation AddProduct($input: [AddProductInput!]!) {
          addProduct(input: $input) {
            product {
              productId
              name
              description
              price
              category
            }
          }
        }
        """
        variables = {
            "input": [{
                "productId": product_id,
                "name": name,
                "description": description,
                "price": price,
                "category": category
            }]
        }
        response = requests.post(self.graphql_endpoint, json={'query': mutation, 'variables': variables})
        return response.json()

    def insert_order(self, order_id, member_id, product_ids, total, date):
        """
        Inserts an order into the database.
        
        Parameters:
        order_id (str): The unique identifier for the order.
        member_id (str): The unique identifier of the member who placed the order.
        product_ids (list): A list of product IDs included in the order.
        total (float): The total amount of the order.
        date (datetime): The date when the order was placed.
        
        Returns:
        dict: The JSON response from the Dgraph server.
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
        response = requests.post(self.graphql_endpoint, json={'query': mutation, 'variables': variables})
        return response.json()

    def insert_review(self, review_id, rating, comment, member_id, product_id, date):
        """
        Inserts a review into the database.
        
        Parameters:
        review_id (str): The unique identifier for the review.
        rating (int): The rating given in the review.
        comment (str): The comment provided in the review.
        member_id (str): The unique identifier of the member who wrote the review.
        product_id (str): The unique identifier of the product being reviewed.
        date (datetime): The date when the review was written.
        
        Returns:
        dict: The JSON response from the Dgraph server.
        """
        mutation = """
        mutation AddReview($input: [AddReviewInput!]!) {
          addReview(input: $input) {
            review {
              reviewId
              rating
              comment
              date
              member {
                memberId
              }
              product {
                productId
              }
            }
          }
        }
        """
        variables = {
            "input": [{
                "reviewId": review_id,
                "rating": rating,
                "comment": comment,
                "member": {"memberId": member_id},
                "product": {"productId": product_id},
                "date": date.isoformat()
            }]
        }
        response = requests.post(self.graphql_endpoint, json={'query': mutation, 'variables': variables})
        return response.json()


def standard_example(dgraph_data_inserter):
    # Example of inserting a member
    print(dgraph_data_inserter.insert_member('1', 'Alice', 'alice@example.com'))

    # Example of inserting a product
    print(dgraph_data_inserter.insert_product('1', 'Lipstick', 'A red lipstick', 15.99, 'Beauty'))

    # Example of inserting an order
    print(dgraph_data_inserter.insert_order('1', '1', ['1'], 15.99, datetime.now()))

    # Example of inserting a review
    print(dgraph_data_inserter.insert_review('1', 5, 'Great product!', '1', '1', datetime.now()))

def create_10_members(dgraph_data_inserter):
    # Insert 10 members
    members = [
        ('1', 'Alice', 'alice@example.com'),
        ('2', 'Bob', 'bob@example.com'),
        ('3', 'Charlie', 'charlie@example.com'),
        ('4', 'David', 'david@example.com'),
        ('5', 'Eve', 'eve@example.com'),
        ('6', 'Frank', 'frank@example.com'),
        ('7', 'Grace', 'grace@example.com'),
        ('8', 'Hank', 'hank@example.com'),
        ('9', 'Ivy', 'ivy@example.com'),
        ('10', 'Jack', 'jack@example.com')
    ]

    for member_id, name, email in members:
        dgraph_data_inserter.insert_member(member_id, name, email)

def create_20_products(dgraph_data_inserter):
    # Insert 20 products
    products = [
        ('1', 'Lipstick', 'A red lipstick', 15.99, 'Beauty'),
        ('2', 'Shampoo', 'A nourishing shampoo', 8.99, 'Haircare'),
        ('3', 'Foundation', 'A liquid foundation', 25.99, 'Beauty'),
        ('4', 'Mascara', 'A waterproof mascara', 12.99, 'Beauty'),
        ('5', 'Conditioner', 'A smoothing conditioner', 9.99, 'Haircare'),
        ('6', 'Hair Spray', 'A strong hold hair spray', 7.99, 'Haircare'),
        ('7', 'Perfume', 'A floral perfume', 45.99, 'Fragrance'),
        ('8', 'Body Lotion', 'A hydrating body lotion', 11.99, 'Skincare'),
        ('9', 'Face Wash', 'A gentle face wash', 6.99, 'Skincare'),
        ('10', 'Sunscreen', 'A broad-spectrum sunscreen', 14.99, 'Skincare'),
        ('11', 'Nail Polish', 'A glossy nail polish', 5.99, 'Beauty'),
        ('12', 'Eye Liner', 'A long-lasting eye liner', 10.99, 'Beauty'),
        ('13', 'Blush', 'A powder blush', 9.99, 'Beauty'),
        ('14', 'Serum', 'A vitamin C serum', 29.99, 'Skincare'),
        ('15', 'Toner', 'A balancing toner', 12.99, 'Skincare'),
        ('16', 'Hair Oil', 'A nourishing hair oil', 19.99, 'Haircare'),
        ('17', 'Lip Balm', 'A moisturizing lip balm', 4.99, 'Beauty'),
        ('18', 'Face Mask', 'A hydrating face mask', 16.99, 'Skincare'),
        ('19', 'Body Wash', 'A refreshing body wash', 9.99, 'Skincare'),
        ('20', 'Hand Cream', 'A nourishing hand cream', 7.99, 'Skincare')
    ]

    for product_id, name, description, price, category in products:
        dgraph_data_inserter.insert_product(product_id, name, description, price, category)

def create_15_orders(dgraph_data_inserter):
    # Insert 15 orders
    orders = [
        ('1', '1', ['1', '2'], 24.98, datetime.now()),
        ('2', '2', ['3', '4'], 38.98, datetime.now()),
        ('3', '3', ['5', '6'], 17.98, datetime.now()),
        ('4', '4', ['7', '8'], 57.98, datetime.now()),
        ('5', '5', ['9', '10'], 21.98, datetime.now()),
        ('6', '6', ['11', '12'], 16.98, datetime.now()),
        ('7', '7', ['13', '14'], 22.98, datetime.now()),
        ('8', '8', ['15', '16'], 32.98, datetime.now()),
        ('9', '9', ['17', '18'], 21.98, datetime.now()),
        ('10', '10', ['19', '20'], 17.98, datetime.now()),
        ('11', '1', ['1', '3', '5'], 55.97, datetime.now()),
        ('12', '2', ['2', '4', '6'], 29.97, datetime.now()),
        ('13', '3', ['7', '9', '11'], 61.97, datetime.now()),
        ('14', '4', ['8', '10', '12'], 36.97, datetime.now()),
        ('15', '5', ['13', '15', '17'], 67.97, datetime.now())
    ]

    for order_id, member_id, product_ids, total, date in orders:
        dgraph_data_inserter.insert_order(order_id, member_id, product_ids, total, date)

def create_25_reviews(dgraph_data_inserter):
    # Insert 25 reviews
    reviews = [
        ('1', 5, 'Excellent product!', '1', '1', datetime.now()),
        ('2', 4, 'Very good, will buy again.', '2', '2', datetime.now()),
        ('3', 3, 'It is okay, not great.', '3', '3', datetime.now()),
        ('4', 5, 'Absolutely love this!', '4', '4', datetime.now()),
        ('5', 2, 'Not what I expected.', '5', '5', datetime.now()),
        ('6', 4, 'Good quality.', '6', '6', datetime.now()),
        ('7', 5, 'Best I have ever used!', '7', '7', datetime.now()),
        ('8', 3, 'Average product.', '8', '8', datetime.now()),
        ('9', 1, 'Terrible, do not buy!', '9', '9', datetime.now()),
        ('10', 4, 'Quite good for the price.', '10', '10', datetime.now()),
        ('11', 5, 'Perfect! Highly recommend.', '1', '11', datetime.now()),
        ('12', 4, 'Really like this.', '2', '12', datetime.now()),
        ('13', 2, 'Not satisfied.', '3', '13', datetime.now()),
        ('14', 5, 'Fantastic!', '4', '14', datetime.now()),
        ('15', 3, 'It is okay.', '5', '15', datetime.now()),
        ('16', 5, 'Great product!', '6', '16', datetime.now()),
        ('17', 4, 'Pretty good.', '7', '17', datetime.now()),
        ('18', 5, 'Amazing!', '8', '18', datetime.now()),
        ('19', 2, 'Disappointed.', '9', '19', datetime.now()),
        ('20', 3, 'It is alright.', '10', '20', datetime.now()),
        ('21', 5, 'Excellent!', '1', '1', datetime.now()),
        ('22', 4, 'Very good.', '2', '2', datetime.now()),
        ('23', 3, 'Average.', '3', '3', datetime.now()),
        ('24', 1, 'Terrible!', '4', '4', datetime.now()),
        ('25', 5, 'Love it!', '5', '5', datetime.now())
    ]

    for review_id, rating, comment, member_id, product_id, date in reviews:
        dgraph_data_inserter.insert_review(review_id, rating, comment, member_id, product_id, date)

# Usage
if __name__ == '__main__':
    dgraph_data_inserter = DgraphDataInserter()
    
    create_10_members(dgraph_data_inserter)
    create_20_products(dgraph_data_inserter)
    create_15_orders(dgraph_data_inserter)
    create_25_reviews(dgraph_data_inserter)

    #simple_example(dgraph_data_inserter)
