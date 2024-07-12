# How Dgraph Generates APIs from Schema

## Introduction

### Overview of Dgraph
Dgraph is a high-performance, distributed graph database designed to handle highly connected data with ease. It provides a native GraphQL API, allowing users to define their data schema using GraphQL types and then automatically generating the necessary APIs to interact with the data. Dgraph's architecture ensures horizontal scalability, strong consistency, and efficient querying, making it ideal for modern applications that require complex data relationships and real-time insights.

### Importance of GraphQL APIs in Dgraph
GraphQL APIs are crucial in Dgraph as they provide a flexible and powerful way to interact with the data stored in the graph database. With GraphQL, clients can request exactly the data they need, reducing over-fetching and under-fetching issues commonly associated with traditional REST APIs. This flexibility allows for efficient data retrieval, making it easier to build responsive and performant applications. Furthermore, GraphQL's type system ensures that clients can only request valid fields, reducing the likelihood of errors and improving the overall robustness of the API.

### Brief Introduction to Schema-Driven API Generation
One of the standout features of Dgraph is its ability to generate APIs directly from a user-defined schema. When a schema is defined in GraphQL, Dgraph uses this schema to automatically create a set of Query, Mutation, and Subscription APIs. This schema-driven approach simplifies the development process, as developers can focus on defining their data models without worrying about the underlying API implementation. Dgraph's automatic API generation ensures that the APIs are always in sync with the schema, providing a seamless experience for both developers and clients.

By leveraging schema-driven API generation, Dgraph enables rapid development and iteration, allowing teams to quickly adapt to changing requirements and deliver features faster. This approach also ensures that the APIs are consistent and adhere to the defined schema, making it easier to maintain and scale the application over time.

### Table of API Generation

| API Category | Operation | Description | Use Case |
|--------------|------------|-------------|----------|
| **Query API** | `getMember(memberId: String!): Member` | Fetches a single `Member` by `memberId`. | Retrieve detailed information about a specific member. |
|              | `queryMember(filter: MemberFilter, order: MemberOrder, first: Int, offset: Int): [Member]` | Fetches a list of `Member` objects with optional filters, ordering, and pagination. | Get a list of members matching specific criteria. |
|              | `aggregateMember(filter: MemberFilter): MemberAggregateResult` | Aggregates `Member` objects based on a filter. | Get aggregate statistics about members, such as count or average. |
|              | `getProduct(productId: String!): Product` | Fetches a single `Product` by `productId`. | Retrieve detailed information about a specific product. |
|              | `queryProduct(filter: ProductFilter, order: ProductOrder, first: Int, offset: Int): [Product]` | Fetches a list of `Product` objects with optional filters, ordering, and pagination. | Get a list of products matching specific criteria. |
|              | `aggregateProduct(filter: ProductFilter): ProductAggregateResult` | Aggregates `Product` objects based on a filter. | Get aggregate statistics about products, such as count or average price. |
|              | `getOrder(orderId: String!): Order` | Fetches a single `Order` by `orderId`. | Retrieve detailed information about a specific order. |
|              | `queryOrder(filter: OrderFilter, order: OrderOrder, first: Int, offset: Int): [Order]` | Fetches a list of `Order` objects with optional filters, ordering, and pagination. | Get a list of orders matching specific criteria. |
|              | `aggregateOrder(filter: OrderFilter): OrderAggregateResult` | Aggregates `Order` objects based on a filter. | Get aggregate statistics about orders, such as count or average total. |
|              | `getReview(reviewId: String!): Review` | Fetches a single `Review` by `reviewId`. | Retrieve detailed information about a specific review. |
|              | `queryReview(filter: ReviewFilter, order: ReviewOrder, first: Int, offset: Int): [Review]` | Fetches a list of `Review` objects with optional filters, ordering, and pagination. | Get a list of reviews matching specific criteria. |
|              | `aggregateReview(filter: ReviewFilter): ReviewAggregateResult` | Aggregates `Review` objects based on a filter. | Get aggregate statistics about reviews, such as count or average rating. |
| **Mutation API** | `addMember(input: [AddMemberInput!]!, upsert: Boolean): AddMemberPayload` | Adds new `Member` objects. | Create new members in the system. |
|              | `updateMember(input: UpdateMemberInput!): UpdateMemberPayload` | Updates existing `Member` objects. | Modify details of existing members. |
|              | `deleteMember(filter: MemberFilter!): DeleteMemberPayload` | Deletes `Member` objects based on a filter. | Remove members that match specific criteria. |
|              | `addProduct(input: [AddProductInput!]!, upsert: Boolean): AddProductPayload` | Adds new `Product` objects. | Create new products in the system. |
|              | `updateProduct(input: UpdateProductInput!): UpdateProductPayload` | Updates existing `Product` objects. | Modify details of existing products. |
|              | `deleteProduct(filter: ProductFilter!): DeleteProductPayload` | Deletes `Product` objects based on a filter. | Remove products that match specific criteria. |
|              | `addOrder(input: [AddOrderInput!]!, upsert: Boolean): AddOrderPayload` | Adds new `Order` objects. | Create new orders in the system. |
|              | `updateOrder(input: UpdateOrderInput!): UpdateOrderPayload` | Updates existing `Order` objects. | Modify details of existing orders. |
|              | `deleteOrder(filter: OrderFilter!): DeleteOrderPayload` | Deletes `Order` objects based on a filter. | Remove orders that match specific criteria. |
|              | `addReview(input: [AddReviewInput!]!, upsert: Boolean): AddReviewPayload` | Adds new `Review` objects. | Create new reviews in the system. |
|              | `updateReview(input: UpdateReviewInput!): UpdateReviewPayload` | Updates existing `Review` objects. | Modify details of existing reviews. |
|              | `deleteReview(filter: ReviewFilter!): DeleteReviewPayload` | Deletes `Review` objects based on a filter. | Remove reviews that match specific criteria. |
| **Aggregation API** | `aggregateMember(filter: MemberFilter): MemberAggregateResult` | Aggregates `Member` objects based on filters. | Obtain aggregated statistics like count or averages of members. |
|              | `aggregateProduct(filter: ProductFilter): ProductAggregateResult` | Aggregates `Product` objects based on filters. | Obtain aggregated statistics like count or averages of products. |
|              | `aggregateOrder(filter: OrderFilter): OrderAggregateResult` | Aggregates `Order` objects based on filters. | Obtain aggregated statistics like count or averages of orders. |
|              | `aggregateReview(filter: ReviewFilter): ReviewAggregateResult` | Aggregates `Review` objects based on filters. | Obtain aggregated statistics like count or averages of reviews. |

This table provides a concise overview of the API operations available for managing members, products, orders, and reviews in a Dgraph-powered application.


## Query API Generation

### Overview
Query APIs in Dgraph allow you to fetch data from the graph database. These APIs are automatically generated based on the schema you define, enabling you to retrieve individual records, lists of records with optional filtering, ordering, and pagination, as well as aggregate statistics.

### How it Works
For each type defined in your schema, Dgraph provides several query operations:
- **Single Record Queries**: Fetch a single record by its unique identifier using `get<Type>` queries.
- **List Queries**: Fetch a list of records with optional filters, ordering, and pagination using `query<Type>` queries.
- **Aggregation Queries**: Perform aggregate operations like count, average, sum, etc., using `aggregate<Type>` queries.

**Example Schema**:
```graphql
type Member {
  memberId: String! @id @search(by: [exact])
  name: String @search(by: [term, fulltext])
  email: String @search(by: [exact])
  orders: [Order] @hasInverse(field: member)
  reviews: [Review] @hasInverse(field: member)
}

type Product {
  productId: String! @id @search(by: [exact])
  name: String! @search(by: [term, fulltext])
  description: String @search(by: [fulltext])
  price: Float!
  category: String @search(by: [term])
  reviews: [Review] @hasInverse(field: product)
}
```

### More Examples

**Fetching a Single Member by ID**:
```graphql
query {
  getMember(memberId: "1") {
    memberId
    name
    email
  }
}
```

**Fetching a List of Members with Filters and Pagination**:
```graphql
query {
  queryMember(filter: { name: { anyofterms: "Alice" } }, order: { asc: name }, first: 5, offset: 0) {
    memberId
    name
    email
  }
}
```

**Aggregating Members**:
```graphql
query {
  aggregateMember(filter: { name: { anyofterms: "Alice" } }) {
    count
    avg {
      memberId
    }
  }
}
```

## Mutation API Generation

### Overview
Mutation APIs in Dgraph are used to modify data in the graph database. They are automatically generated based on the schema and allow you to add, update, and delete records.

### How it Works
For each type defined in your schema, Dgraph provides several mutation operations:
- **Add Mutations**: Add new records using `add<Type>` mutations.
- **Update Mutations**: Update existing records using `update<Type>` mutations.
- **Delete Mutations**: Delete records using `delete<Type>` mutations.

**Example Schema**:
```graphql
type Order {
  orderId: String! @id @search(by: [exact])
  member: Member! @hasInverse(field: orders)
  products: [Product!]!
  total: Float!
  date: DateTime! @search
}

type Review {
  reviewId: String! @id @search(by: [exact])
  rating: Int! @search
  comment: String @search(by: [fulltext])
  member: Member! @hasInverse(field: reviews)
  product: Product! @hasInverse(field: reviews)
}
```

### More Examples

**Adding a New Member**:
```graphql
mutation {
  addMember(input: [{ memberId: "1", name: "Alice", email: "alice@example.com" }], upsert: true) {
    member {
      memberId
      name
      email
    }
  }
}
```

**Updating an Existing Member**:
```graphql
mutation {
  updateMember(input: { filter: { memberId: { eq: "1" } }, set: { name: "Alice Johnson" } }) {
    member {
      memberId
      name
      email
    }
  }
}
```

**Deleting a Member**:
```graphql
mutation {
  deleteMember(filter: { memberId: { eq: "1" } }) {
    msg
  }
}
```

## Subscription API Generation

### Overview
Subscription APIs in Dgraph enable real-time updates by allowing clients to subscribe to changes in the database. For each type with the `@withSubscription` directive, Dgraph generates subscription operations for create, update, and delete events.

### How it Works
For each type defined with the `@withSubscription` directive in your schema, Dgraph provides several subscription operations:
- **Created Records Subscriptions**: Listen for new records using `new<Type>` subscriptions.
- **Updated Records Subscriptions**: Listen for updates to existing records using `updated<Type>` subscriptions.
- **Deleted Records Subscriptions**: Listen for deletions of records using `deleted<Type>` subscriptions.

**Example Schema**:
```graphql
type Member @withSubscription {
  memberId: String! @id @search(by: [exact])
  name: String @search(by: [term, fulltext])
  email: String @search(by: [exact])
}

type Product @withSubscription {
  productId: String! @id @search(by: [exact])
  name: String! @search(by: [term, fulltext])
  description: String @search(by: [fulltext])
  price: Float!
  category: String @search(by: [term])
}
```

### More Examples

**Subscription for New Members**:
```graphql
subscription {
  newMember {
    memberId
    name
    email
  }
}
```

**Subscription for Updated Members**:
```graphql
subscription {
  updatedMember {
    memberId
    name
    email
  }
}
```

**Subscription for Deleted Members**:
```graphql
subscription {
  deletedMember {
    memberId
  }
}
```


## Practical Examples

### Practical Example for Query API
**Scenario**: You want to retrieve information about all members who have the term "Alice" in their name, ordered alphabetically by name, and limit the results to the first 5 members.

**GraphQL Query**:
```graphql
query {
  queryMember(filter: { name: { anyofterms: "Alice" } }, order: { asc: name }, first: 5, offset: 0) {
    memberId
    name
    email
  }
}
```

**Explanation**:
- **filter**: Filters members whose name contains the term "Alice".
- **order**: Orders the results alphabetically by the `name` field in ascending order.
- **first**: Limits the results to the first 5 members.
- **offset**: Starts the results from the 0th member (used for pagination).

### Practical Example for Mutation API
**Scenario**: You want to add a new product to the database.

**GraphQL Mutation**:
```graphql
mutation {
  addProduct(input: [{ 
    productId: "1", 
    name: "Lipstick", 
    description: "A long-lasting red lipstick.", 
    price: 19.99, 
    category: "Cosmetics" 
  }], upsert: true) {
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

**Explanation**:
- **input**: Specifies the product details to be added.
  - `productId`: Unique identifier for the product.
  - `name`: Name of the product.
  - `description`: Description of the product.
  - `price`: Price of the product.
  - `category`: Category of the product.
- **upsert**: Ensures the product is added only if it does not already exist.
- **product**: Returns the details of the added product.

### Practical Example for Subscription API
**Scenario**: You want to listen for real-time updates whenever a new member is added to the database.

**GraphQL Subscription**:
```graphql
subscription {
  newMember {
    memberId
    name
    email
  }
}
```

**Explanation**:
- **newMember**: Subscribes to events for newly added members.
- **memberId, name, email**: Specifies the fields to be returned for the newly added member.

**Usage**:
To use this subscription, you would need a GraphQL client that supports subscriptions, such as Altair, Apollo Client, or Relay. When a new member is added to the database, the subscription will automatically trigger and return the specified fields.



## Conclusion

### Summary of Dgraph's API Generation
Dgraph's ability to generate GraphQL APIs directly from a user-defined schema is a powerful feature that simplifies the development process. By defining the data schema using GraphQL types, Dgraph automatically creates a comprehensive set of Query, Mutation, and Subscription APIs. This schema-driven approach ensures that the APIs are always in sync with the data model, providing a consistent and reliable interface for interacting with the database.

### Benefits of Using Dgraph for GraphQL APIs
- **Automatic API Generation**: Dgraph generates APIs based on the schema, reducing the need for manual API development and maintenance.
- **Flexible Data Retrieval**: With GraphQL queries, clients can request exactly the data they need, improving efficiency and reducing bandwidth usage.
- **Real-Time Updates**: Subscriptions allow clients to receive real-time notifications about changes in the data, enabling the creation of dynamic and responsive applications.
- **Strong Consistency**: Dgraph ensures strong consistency across distributed nodes, providing reliable and accurate data access.
- **Scalability**: Designed to scale horizontally, Dgraph can handle large volumes of data and high query loads, making it suitable for enterprise-level applications.
- **Ease of Use**: With tools like Altair, developers can easily interact with the GraphQL APIs, test queries, and debug issues, streamlining the development workflow.

### Final Thoughts and Recommendations
Dgraph offers a robust and scalable solution for managing and interacting with graph data using GraphQL. Its automatic API generation from a schema simplifies development and ensures consistency between the data model and the API. By leveraging Dgraph's capabilities, developers can build efficient, responsive, and real-time applications with ease.

For those new to Dgraph, starting with the basics of schema definition and exploring the auto-generated APIs through tools like Altair is recommended. As you become more comfortable with the system, you can dive deeper into advanced features such as custom directives, nested queries, and performance optimization techniques.

Dgraph's seamless integration with GraphQL provides a powerful framework for modern data-driven applications, offering flexibility, scalability, and real-time capabilities that can significantly enhance the development and user experience.



