from fastapi import FastAPI, HTTPException
import uvicorn

from Reporter.query_processors import TransactionQueryProcessor
from Infrastructure.exceptions import RecordNotFoundException

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome. This is a project to summarize your transaction history."}


@app.get("/transaction/{transaction_id}", status_code=200)
def get_transaction(transaction_id: str):
    try:
        transaction = TransactionQueryProcessor.get_transaction(transaction_id)
    except RecordNotFoundException as tnfe:
        raise HTTPException(status_code=tnfe.error_code, detail=tnfe.error_description)
    return {"message": transaction}


@app.get("/transaction-summary-bySKU/{last_n_days}")
def get_transaction_summary_by_sku(last_n_days: int):
    transaction_summary = TransactionQueryProcessor.summarize_by_sku(last_n_days)
    return {"message": transaction_summary}


@app.get("/transaction-summary-bycategory/{last_n_days}")
def get_transaction_summary_by_category(last_n_days: int):
    transaction_summary = TransactionQueryProcessor.summarize_by_category(last_n_days)
    return {"message": transaction_summary}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
