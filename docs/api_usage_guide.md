# Getting Started with GraphQL in Dgraph: Queries, Mutations, and Subscriptions

## Introduction

### Overview of GraphQL
GraphQL is a powerful query language for APIs and a runtime for executing those queries against your data. Unlike traditional REST APIs, where each endpoint returns a fixed structure of data, GraphQL allows clients to specify exactly what data they need. This results in more efficient data retrieval, reducing both over-fetching and under-fetching of data. Additionally, GraphQL allows multiple resources to be retrieved in a single request, which can significantly improve performance in applications with complex data needs.

Key features of GraphQL include:
- **Strongly Typed Schema**: Defines what queries clients can make and what types of data can be returned.
- **Single Endpoint**: All queries, mutations, and subscriptions are sent to a single endpoint.
- **Efficient Data Retrieval**: Clients can request only the data they need.
- **Real-time Data**: Supports subscriptions to enable real-time updates.

### The /graphql Endpoint in Dgraph
The `/graphql` endpoint in Dgraph serves the GraphQL API for interacting with your database. When you deploy a GraphQL schema, Dgraph automatically generates a spec-compliant GraphQL API at this endpoint. This allows you to perform queries, mutations, and subscriptions to manage and interact with your data.

**Key Points**:
- **Accessing the Endpoint**:
  - For Dgraph Cloud, the endpoint can be found in the Overview panel of the Dgraph Cloud dashboard.
  - For local installations, the default endpoint is `http://localhost:8080/graphql`.
- **Configuration**:
  - The endpoint URL can vary based on your configuration, including the port offset defined by the `--port_offset` option of the `dgraph alpha` command, the configuration of TLS for HTTPS, and the use of a load balancer.
- **Request Methods**:
  - GraphQL requests can be made via HTTP POST or HTTP GET methods, making it flexible and easy to integrate with various client applications.

### The /admin Endpoint in Dgraph
The `/admin` endpoint in Dgraph is designed for administrative tasks, allowing you to manage schemas, perform backups, and handle other maintenance operations. This endpoint is critical for maintaining the health and performance of your Dgraph database.

**Key Features**:
- **Schema Management**:
  - **Initial Setup**: When starting with a blank database, no schema is served at `/graphql`, and querying the `/admin` endpoint for `getGQLSchema` returns `null`.
  - **Validating Schemas**: You can validate a GraphQL schema before adding it to your database using the `/admin/schema/validate` endpoint.
  - **Modifying Schemas**: Schemas can be modified using the `/admin/schema` endpoint or the `updateGQLSchema` mutation.
    - Example of validating a schema:
      ```graphql
      type Person {
        name: String
      }
      ```
    - Example of updating a schema using `updateGQLSchema` mutation:
      ```graphql
      mutation {
        updateGQLSchema(input: { set: { schema: "type Person { name: String }"}}) {
          gqlSchema {
            schema
            generatedSchema
          }
        }
      }
      ```
- **Schema Updates and Effects**:
  - Adding a schema will refresh the `/graphql` endpoint to serve the new schema and update the underlying Dgraph instance's schema.
  - Schema updates allow for changes such as adding new fields and indexes. For example:
    ```graphql
    type Person {
      name: String @search(by: [regexp])
      dob: DateTime
    }
    ```

By understanding these endpoints and how to interact with them, you can effectively manage and utilize Dgraph's powerful features to build robust and scalable applications.



## GraphQL Client

### Introduction to Altair
Altair is a popular GraphQL client that provides a user-friendly interface for testing and interacting with GraphQL APIs. It offers features such as syntax highlighting, query history, and the ability to save and share queries, making it an essential tool for developers working with GraphQL. Altair supports both queries and mutations, and it also allows you to easily manage headers and variables.

Key features of Altair include:
- **Intuitive Interface**: A clean and easy-to-use interface for crafting and testing GraphQL queries and mutations.
- **Query History**: Keeps track of your queries so you can easily access previous ones.
- **Variable Management**: Simplifies the use of variables in your queries and mutations.
- **Header Management**: Allows you to set and manage HTTP headers for your requests.
- **Support for Subscriptions**: Enables testing of GraphQL subscriptions.
- **Multiple Tabs**: Allows you to work with multiple queries in different tabs simultaneously.

### Installing Altair Chrome Extension
Altair is available as a Chrome extension, which makes it easy to install and use directly from your browser. Follow the steps below to install Altair:

#### GitHub Repository
You can find the source code and additional installation options for Altair on its GitHub repository:
- **GitHub Repository**: [Altair GraphQL Client](https://github.com/altair-graphql/altair)

#### Chrome Web Store
To install the Altair extension from the Chrome Web Store, follow these steps:
1. **Open the Chrome Web Store**: Go to the [Chrome Web Store](https://chromewebstore.google.com/search/Altair).
2. **Search for Altair**: Type "Altair GraphQL Client" in the search bar and press Enter.
3. **Select Altair**: Click on the Altair GraphQL Client from the search results.
4. **Add to Chrome**: Click the "Add to Chrome" button to install the extension.
5. **Confirm Installation**: A dialog box will appear. Click "Add Extension" to confirm and complete the installation.

Once installed, you can open Altair from your browser extensions or by navigating to `chrome://extensions/` and clicking on Altair.

With Altair installed, you can easily interact with your Dgraph GraphQL endpoints, test queries and mutations, and debug your GraphQL API. This makes it a valuable tool for both development and production environments.



## GraphQL Query Examples


### `getMember` API
**Introduction**: Fetches a single `Member` by `memberId`. Use case: Get detailed information about a specific member.

```graphql
query {
  getMember(memberId: "1") {
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
      date
    }
    recommendedProducts {
      productId
      name
    }
  }
}
```

### `queryMember` API
**Introduction**: Fetches a list of `Member` objects with optional filters, ordering, and pagination. Use case: Get a list of members with specific criteria.

```graphql
query {
  queryMember(filter: { name: { anyofterms: "Alice" } }, first: 5, offset: 0) {
    memberId
    name
    email
  }
}
```

### `aggregateMember` API
**Introduction**: Aggregates `Member` objects based on a filter. Use case: Get aggregate statistics about members, such as count or average.

```graphql
query {
  aggregateMember(filter: { name: { anyofterms: "Alice" } }) {
    count
  }
}
```

### `getProduct` API
**Introduction**: Fetches a single `Product` by `productId`. Use case: Get detailed information about a specific product.

```graphql
query {
  getProduct(productId: "1") {
    productId
    name
    description
    price
    category
    reviews {
      reviewId
      rating
      comment
    }
  }
}
```

### `queryProduct` API
**Introduction**: Fetches a list of `Product` objects with optional filters, ordering, and pagination. Use case: Get a list of products with specific criteria.

```graphql
query {
  queryProduct(filter: { category: { anyofterms: "Beauty" } }, first: 5, offset: 0) {
    productId
    name
    description
    price
    category
  }
}
```

### `aggregateProduct` API
**Introduction**: Aggregates `Product` objects based on a filter. Use case: Get aggregate statistics about products, such as count or average price.

```graphql
query {
  aggregateProduct(filter: { category: { anyofterms: "Beauty" } }) {
    count
    avg {
      price
    }
  }
}
```

### `getOrder` API
**Introduction**: Fetches a single `Order` by `orderId`. Use case: Get detailed information about a specific order.

```graphql
query {
  getOrder(orderId: "1") {
    orderId
    total
    date
    member {
      memberId
      name
    }
    products {
      productId
      name
      price
    }
  }
}
```

### `queryOrder` API
**Introduction**: Fetches a list of `Order` objects with optional filters, ordering, and pagination. Use case: Get a list of orders with specific criteria.

```graphql
query {
  queryOrder(filter: { total: { ge: 20.00 } }, first: 5, offset: 0) {
    orderId
    total
    date
  }
}
```

### `aggregateOrder` API
**Introduction**: Aggregates `Order` objects based on a filter. Use case: Get aggregate statistics about orders, such as count or average total.

```graphql
query {
  aggregateOrder(filter: { total: { ge: 20.00 } }) {
    count
    avg {
      total
    }
  }
}
```

### `getReview` API
**Introduction**: Fetches a single `Review` by `reviewId`. Use case: Get detailed information about a specific review.

```graphql
query {
  getReview(reviewId: "1") {
    reviewId
    rating
    comment
    date
    member {
      memberId
      name
    }
    product {
      productId
      name
      price
    }
  }
}
```

### `queryReview` API
**Introduction**: Fetches a list of `Review` objects with optional filters, ordering, and pagination. Use case: Get a list of reviews with specific criteria.

```graphql
query {
  queryReview(filter: { rating: { eq: 5 } }, first: 5, offset: 0) {
    reviewId
    rating
    comment
    date
  }
}
```

### `aggregateReview` API
**Introduction**: Aggregates `Review` objects based on a filter. Use case: Get aggregate statistics about reviews, such as count or average rating.

```graphql
query {
  aggregateReview(filter: { rating: { eq: 5 } }) {
    count
    avg {
      rating
    }
  }
}
```


## GraphQL Mutation Examples

### `addMember` API
**Introduction**: Adds one or more `Member` objects. Use case: Add new members to the system.

```graphql
mutation {
  addMember(input: [
    {
      memberId: "1",
      name: "Alice",
      email: "alice@example.com"
    },
    {
      memberId: "2",
      name: "Bob",
      email: "bob@example.com"
    }
  ]) {
    member {
      memberId
      name
      email
    }
  }
}
```

### `updateMember` API
**Introduction**: Updates an existing `Member` object. Use case: Update member information.

```graphql
mutation {
  updateMember(input: {
    filter: { memberId: { eq: "1" } },
    set: {
      name: "Alice Smith",
      email: "alice.smith@example.com"
    }
  }) {
    member {
      memberId
      name
      email
    }
  }
}
```

### `deleteMember` API
**Introduction**: Deletes one or more `Member` objects. Use case: Remove members from the system.

```graphql
mutation {
  deleteMember(filter: { memberId: { eq: "1" } }) {
    msg
    numUids
  }
}
```

### `addProduct` API
**Introduction**: Adds one or more `Product` objects. Use case: Add new products to the catalog.

```graphql
mutation {
  addProduct(input: [
    {
      productId: "1",
      name: "Lipstick",
      description: "A red lipstick",
      price: 15.99,
      category: "Beauty"
    },
    {
      productId: "2",
      name: "Shampoo",
      description: "A nourishing shampoo",
      price: 8.99,
      category: "Haircare"
    }
  ]) {
    product {
      productId
      name
      description
      price
      category
    }
  }
}
```

### `updateProduct` API
**Introduction**: Updates an existing `Product` object. Use case: Update product details.

```graphql
mutation {
  updateProduct(input: {
    filter: { productId: { eq: "1" } },
    set: {
      name: "Lipstick Deluxe",
      price: 18.99
    }
  }) {
    product {
      productId
      name
      price
    }
  }
}
```

### `deleteProduct` API
**Introduction**: Deletes one or more `Product` objects. Use case: Remove products from the catalog.

```graphql
mutation {
  deleteProduct(filter: { productId: { eq: "1" } }) {
    msg
    numUids
  }
}
```

### `addOrder` API
**Introduction**: Adds one or more `Order` objects. Use case: Create new orders.

```graphql
mutation {
  addOrder(input: [
    {
      orderId: "1",
      member: { memberId: "1" },
      products: [
        { productId: "1" },
        { productId: "2" }
      ],
      total: 24.98,
      date: "2023-07-15T10:00:00Z"
    }
  ]) {
    order {
      orderId
      total
      date
    }
  }
}
```

### `updateOrder` API
**Introduction**: Updates an existing `Order` object. Use case: Update order details.

```graphql
mutation {
  updateOrder(input: {
    filter: { orderId: { eq: "1" } },
    set: {
      total: 25.98
    }
  }) {
    order {
      orderId
      total
    }
  }
}
```

### `deleteOrder` API
**Introduction**: Deletes one or more `Order` objects. Use case: Remove orders from the system.

```graphql
mutation {
  deleteOrder(filter: { orderId: { eq: "1" } }) {
    msg
    numUids
  }
}
```

### `addReview` API
**Introduction**: Adds one or more `Review` objects. Use case: Add reviews for products.

```graphql
mutation {
  addReview(input: [
    {
      reviewId: "1",
      rating: 5,
      comment: "Excellent product!",
      member: { memberId: "1" },
      product: { productId: "1" },
      date: "2023-07-15T10:00:00Z"
    }
  ]) {
    review {
      reviewId
      rating
      comment
      date
    }
  }
}
```

### `updateReview` API
**Introduction**: Updates an existing `Review` object. Use case: Update review details.

```graphql
mutation {
  updateReview(input: {
    filter: { reviewId: { eq: "1" } },
    set: {
      comment: "Amazing product!"
    }
  }) {
    review {
      reviewId
      comment
    }
  }
}
```

### `deleteReview` API
**Introduction**: Deletes one or more `Review` objects. Use case: Remove reviews from the system.

```graphql
mutation {
  deleteReview(filter: { reviewId: { eq: "1" } }) {
    msg
    numUids
  }
}
```



## GraphQL Subscription Examples

### Subscribing to All Members (Create, Update, and Delete events)
```graphql
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
```
**Explanation:** This subscription listens for any changes (additions, updates, deletions) to `Member` records and retrieves their `memberId`, `name`, `email`, associated `orders`, and `reviews`.

### Subscribing to a Specific Member (Create, Update, and Delete events)
```graphql
subscription($memberId: String!) {
  getMember(memberId: $memberId) {
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
```
**Explanation:** This subscription listens for any changes to a specific `Member` identified by `memberId` and retrieves their `memberId`, `name`, `email`, associated `orders`, and `reviews`.

### Subscribing to All Products (Create, Update, and Delete events)
```graphql
subscription {
  queryProduct {
    productId
    name
    description
    price
    category
    reviews {
      reviewId
    }
  }
}
```
**Explanation:** This subscription listens for any changes (additions, updates, deletions) to `Product` records and retrieves their `productId`, `name`, `description`, `price`, `category`, and associated `reviews`.

### Subscribing to a Specific Product (Create, Update, and Delete events)
```graphql
subscription($productId: String!) {
  getProduct(productId: $productId) {
    productId
    name
    description
    price
    category
    reviews {
      reviewId
    }
  }
}
```
**Explanation:** This subscription listens for any changes to a specific `Product` identified by `productId` and retrieves their `productId`, `name`, `description`, `price`, `category`, and associated `reviews`.

### Subscribing to All Orders (Create, Update, and Delete events)
```graphql
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
```
**Explanation:** This subscription listens for any changes (additions, updates, deletions) to `Order` records and retrieves their `orderId`, `total`, `date`, associated `member`, and `products`.

### Subscribing to a Specific Order (Create, Update, and Delete events)
```graphql
subscription($orderId: String!) {
  getOrder(orderId: $orderId) {
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
```
**Explanation:** This subscription listens for any changes to a specific `Order` identified by `orderId` and retrieves their `orderId`, `total`, `date`, associated `member`, and `products`.

### Subscribing to All Reviews (Create, Update, and Delete events)
```graphql
subscription {
  queryReview {
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
```
**Explanation:** This subscription listens for any changes (additions, updates, deletions) to `Review` records and retrieves their `reviewId`, `rating`, `comment`, `date`, associated `member`, and `product`.

### Subscribing to a Specific Review (Create, Update, and Delete events)
```graphql
subscription($reviewId: String!) {
  getReview(reviewId: $reviewId) {
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
```
**Explanation:** This subscription listens for any changes to a specific `Review` identified by `reviewId` and retrieves their `reviewId`, `rating`, `comment`, `date`, associated `member`, and `product`.



## Conclusion

GraphQL and Dgraph together provide a robust and scalable solution for modern data management needs. By leveraging the capabilities of GraphQL, you can create efficient and responsive applications that meet the demands of today's dynamic data environments. Dgraph's seamless integration with GraphQL ensures that you have the tools necessary to build, manage, and optimize your data interactions with ease.

As you continue to explore and implement GraphQL with Dgraph, tools like Altair will be invaluable in simplifying your development process and enhancing your productivity. Whether you are building new applications or optimizing existing ones, the combination of GraphQL and Dgraph offers a powerful and flexible framework to achieve your goals.

We hope this article has provided you with a solid foundation to get started with GraphQL in Dgraph and inspired you to harness the full potential of these technologies in your projects.


