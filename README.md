# operation-healthcare
**Publisher/subscribe model to process streaming data and provide an up-to-date view of incoming data.**

Transaction data is updated in transactions-db.csv where each record contains:
- transaction_id
- sku_id
- sku_price
- transaction_datetime

SKU data is stored in a static file sku-db.csv where each record contains:
- sku_id
- sku_name
- sku_category

The service has three APIs that display information, namely:
1. GET API /transaction/{transaction_id}: *Displays details of specified transaction*
2. GET API /transaction-summary-bySKU/{last_n_days}: *Groups transactions performed over last n days by SKU and displays total amount for each SKU*
3. GET API /transaction-summary-bycategory/{last_n_days}: *Groups transactions performed over last n days by category and displays total amount for each category*
