import uvicorn
from fastapi import FastAPI, HTTPException

from Infrastructure.exceptions import RecordNotFoundException
from Reporter.SampleResponses import category_summary_response, sku_summary_response, transaction_response
from Reporter.QueryProcessors import TransactionQueryProcessor

app = FastAPI(
    title="Reporter API",
    description="Your friendly neighbourhood reporter bringing you"
                " all the transaction information and summaries you need.\n"
                "Available endpoints:\n"
                "1. GET /transaction/{transaction_id}\n"
                "2. GET /transaction-summary-bySKU/{last_n_days}\n"
                "3. GET /transaction-summary-bycategory/{last_n_days}",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "Welcome. This is a project to summarize your transaction history."}


@app.get("/transaction/{transaction_id}", status_code=200, responses=transaction_response)
def get_transaction(transaction_id: str):
    try:
        transaction = TransactionQueryProcessor.get_transaction(transaction_id)
    except RecordNotFoundException as tnfe:
        raise HTTPException(status_code=tnfe.error_code, detail=tnfe.error_description)
    return {"message": transaction}


@app.get("/transaction-summary-bySKU/{last_n_days}", status_code=200, responses=sku_summary_response)
def get_transaction_summary_by_sku(last_n_days: int):
    transaction_summary = TransactionQueryProcessor.summarize_by_sku(last_n_days)
    return {"message": transaction_summary}


@app.get("/transaction-summary-bycategory/{last_n_days}", status_code=200, responses=category_summary_response)
def get_transaction_summary_by_category(last_n_days: int):
    transaction_summary = TransactionQueryProcessor.summarize_by_category(last_n_days)
    return {"message": transaction_summary}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
