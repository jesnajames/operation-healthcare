from fastapi import FastAPI, HTTPException
import uvicorn

from Infrastructure.models import TransactionRecord
from Journalist.command_processors import TransactionCommandProcessor

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome. Report new transactions here"}


@app.post("/transactions", status_code=200)
def post_transaction(transaction: TransactionRecord):
    message_id = TransactionCommandProcessor.post_transaction(transaction)
    return {"message": f"Transaction published successfully ,message ID: {message_id}"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
