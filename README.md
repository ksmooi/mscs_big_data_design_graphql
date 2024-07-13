# BeautyInsights 360

Welcome to the BeautyInsights 360 project! This project is designed to provide a comprehensive solution for analyzing customer behavior, product performance, and sales trends for a beauty brand. It leverages Dgraph, a highly scalable and efficient graph database, to handle complex data relationships and provide real-time insights and recommendations.

## Project Overview

BeautyInsights 360 integrates various data sources to analyze customer information, shopping behavior, product reviews, and more. It utilizes advanced analytics and machine learning models to generate personalized product recommendations, optimize inventory, and improve marketing strategies. The project is structured to ensure modularity and ease of use, with clear separation of backend, frontend, and testing components.

## Documentation

### [System Design](docs/system_design.md)

This file provides a comprehensive overview of the system architecture and design of the BeautyInsights 360 project. It includes detailed diagrams and explanations of the different components and their interactions. This documentation helps users and developers understand the underlying structure of the system and how different modules work together to provide the desired functionality.

<a href="docs/system_design.md">
    <img src="docs/res/beauty360_system_arch_overall.jpg" width="600" alt="System Architecture">
</a>


### [GraphQL API Usage Guide](docs/api_usage_guide.md)

This file provides detailed instructions on how to interact with the API provided by the BeautyInsights 360 project. It covers various aspects of API usage, including available endpoints, query formats, and examples of how to perform common operations such as creating, reading, updating, and deleting data.

### [Dgraph API Generation](docs/dgraph_api_generation.md)

This file explains how to generate the API using Dgraph. It includes information on setting up the GraphQL schema, configuring Dgraph, and generating the necessary API endpoints. It also provides guidance on how to leverage Dgraph’s capabilities to efficiently manage and query graph data.

### [Installation Guide](docs/installation.md)

This file contains step-by-step instructions for installing and setting up the BeautyInsights 360 project. It covers all the prerequisites, environment setup, installation of necessary packages, and configuration of Dgraph using Docker and Docker Compose. This guide ensures that users can get the project up and running smoothly.

## Codebase Structure

### [src/backend folder](src/backend)

**Purpose**: This folder contains the core backend logic of the BeautyInsights 360 project. It includes scripts and modules that handle data analysis, processing, and other backend functionalities. The main script in this folder, `analysis_engine.py`, implements various analysis cases such as customer behavior analysis, product performance evaluation, and sales trend analysis.

### [src/examples folder](src/examples)

**Purpose**: This folder contains example scripts demonstrating how to interact with the Dgraph API using GraphQL. These scripts serve as practical guides for performing common operations such as queries, mutations, and subscriptions. They also include a script for creating mock data in the Dgraph database. The example scripts help users understand how to use the API and integrate it into their own applications.

- `api_query.py`: Example script for GraphQL queries.
- `api_mutation.py`: Example script for GraphQL mutations.
- `api_subscription.py`: Example script for GraphQL subscriptions.
- `create_mock_data.py`: Script for creating mock data in Dgraph.

### [src/tests folder](src/tests)

**Purpose**: This folder contains unit tests for the BeautyInsights 360 project. The tests ensure that the different components of the project are functioning correctly. The main test script, `utest_dgraph_client.py`, includes tests for the `DgraphClient` class, verifying its ability to handle queries, mutations, and subscriptions. Running these tests helps maintain code quality and reliability by catching bugs and issues early in the development process.

## Getting Started

To get started with the BeautyInsights 360 project, please refer to the [installation.md](docs/installation.md) file for detailed setup instructions.

For more information on using the API, generating the API with Dgraph, and understanding the system design, refer to the respective documentation files in the `docs` directory.

