# operation-healthcare
**Publisher/Subscriber model with FastAPI framework to process streaming data and provide an up-to-date view of incoming data.**

## Overview
The project consists of four components, namely:
1. **Journalist**: Publisher service that publishes transaction records to the GCP Pub/Sub topic. 
Endpoint provided to post message to the topic: POST API /transactions
2. **BackstageSubscriber**: Subscriber service that fetches messages from the GCP PubSub topic and updates list of transactions.
3. **Reporter**: API service that caters to the queries regarding transaction information and summarizes transactions of a specified duration by SKU or category.
The service has three APIs that display information, namely:
   - GET /transaction/{transaction_id}: *Displays details of specified transaction*
   - GET /transaction-summary-bySKU/{last_n_days}: *Groups transactions performed over last n days by SKU and displays total amount for each SKU*
   - GET /transaction-summary-bycategory/{last_n_days}: *Groups transactions performed over last n days by category and displays total amount for each category*
4. **Infrastructure**: Collection of utilities to manage data store, private keys, and handler functions that can be accessed by the aforementioned services.

## Data Store
Transaction data is updated in transactions-db.csv where each record contains:
- transaction_id
- sku_id
- sku_price
- transaction_datetime

SKU data is stored in a static file sku-db.csv where each record contains:
- sku_id
- sku_name
- sku_category

## Salient features
- Makes use of pydantic BaseModels to validate and standardise request and response structures
- Leverages FastAPI-powered documentation to demonstrate expected request formats and sample responses at {BASE_URL}/docs
- Provides type-hints and comments where needed for increased readability and easier debugging.
