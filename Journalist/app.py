from fastapi import FastAPI
import uvicorn

from Infrastructure.models import TransactionRecordg
from Journalist.command_processors import TransactionCommandProcessor

app = FastAPI(
    title="Journalist API",
    description="Veteran journalist publishing to the hottest topics.\n"
                "Makes latest transaction records available for consumption."
                "Available endpoints:\n"
                "1. POST /transactions",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "Welcome. Report new transactions here"}


@app.post("/transactions", status_code=200)
def post_transaction(transaction: TransactionRecord):
    message_id = TransactionCommandProcessor.post_transaction(transaction)
    return {"message": f"Transaction published successfully ,message ID: {message_id}"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
