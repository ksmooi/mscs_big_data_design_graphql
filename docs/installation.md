# BeautyInsights 360 Installation Guide

## Prepare Python Environment

1. **Install Python (>= 3.8)**
2. **Install Required Packages**
   - Create a `requirements.txt` file with the following content:
     ```
     requests==2.26.0
     responses==0.13.3
     websockets==10.1
     pydgraph==21.3.0
     ```
   - Run the following command to install the packages:
     ```bash
     pip install -r requirements.txt
     ```

## Prepare Dgraph

1. **Install Dgraph with Docker**
   - Pull the latest Dgraph image:
     ```bash
     docker pull dgraph/dgraph:latest
     ```

2. **Setup Docker-Compose**
   - Create a `docker-compose.yml` file with the following content:
     ```yaml
     version: '3.6'
     services:
       # Dgraph database
       # Dgraph Zero is responsible for cluster management, including maintaining the membership information of Alpha nodes, 
       # distributing data shards, and managing the RAFT consensus algorithm for leader election among the Alpha nodes.
       zero:
         image: dgraph/dgraph:v23.1.1
         volumes:
           - /tmp/data:/dgraph
         ports:
           - 5080:5080
           - 6080:6080
         restart: on-failure
         command: dgraph zero --my=zero:5080
       
       # Dgraph Alpha nodes are responsible for storing and serving the graph data. They handle queries, mutations, and data retrieval.
       alpha:
         image: dgraph/dgraph:v23.1.1
         volumes:
           - /tmp/data:/dgraph
         ports:
           - 8080:8080
           - 9080:9080
         restart: on-failure
         command: dgraph alpha --my=alpha:7080 --zero=zero:5080 --security whitelist=127.0.0.1,192.168.1.0/24
       
       # Dgraph Ratel is the web-based UI for interacting with Dgraph. It allows users to visualize the schema, 
       # run queries and mutations, and manage the database through a graphical interface.
       ratel:
         image: dgraph/ratel:v21.12.0
         ports:
           - 8000:8000
     ```

3. **Control the Dgraph Service**
   - **Start Dgraph:**
     ```bash
     docker-compose up -d
     ```
   - **Stop Dgraph:**
     ```bash
     docker-compose down
     ```

## Load GraphQL Schema to Dgraph

1. **Drop All Schema**
   - Use the following command to drop all existing schema:
     ```bash
     curl -X POST 192.168.1.150:8080/alter -d '{"drop_all": true}'
     ```

2. **Load the GraphQL Schema File**
   - Save your schema file as `api_schema.graphql`.
   - Run the following command to upload the schema to Dgraph:
     ```bash
     curl -X POST localhost:8080/admin/schema --data-binary '@api_schema.graphql'
     ```

## Create Mock Data

1. **Create Mock Data in Dgraph Database**
   - Run the script to create mock data:
     ```bash
     python src/examples/create_mock_data.py
     ```

## Install Altair GraphQL Client (Chrome Extension)

1. **Install Altair GraphQL Client**
   - Visit the [Chrome Web Store](https://chromewebstore.google.com/detail/altair-graphql-client/flnheeellpciglgpaodhkhmapeljopja) and install the Altair GraphQL Client extension.

## Connect Dgraph Server with Altair GraphQL Client

1. **Connect to Dgraph Server**
   - Open the Altair GraphQL Client.
   - Set the Server URL to:
     ```
     http://192.168.1.150:8080/graphql
     ```

## Example GraphQL Queries, Mutations, and Subscriptions

1. **Example Scripts**
   - **GraphQL Query Example:**
     ```bash
     python src/examples/api_query.py
     ```
   - **GraphQL Mutation Example:**
     ```bash
     python src/examples/api_mutation.py
     ```
   - **GraphQL Subscription Example:**
     ```bash
     python src/examples/api_subscription.py
     ```

## Data Analysis Example

1. **Run Analysis Engine**
   - The main data analysis functionality is provided by the `analysis_engine.py` script:
     ```bash
     python src/backend/analysis_engine.py
     ```

## Unit Tests

1. **Run Unit Tests**
   - Execute the unit tests to ensure everything is set up correctly:
     ```bash
     python -m unittest discover -s src/tests -p "utest_dgraph_client.py"
     ```
