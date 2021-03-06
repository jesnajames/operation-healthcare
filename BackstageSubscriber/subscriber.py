import os
from concurrent.futures import TimeoutError

from google.cloud import pubsub_v1
from loguru import logger

from Infrastructure.config import ROOT_DIR
from Infrastructure.RepositoryKeeper import TransactionRepository

creds_path = os.path.join(ROOT_DIR, "operation-healthcare-private-key.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path

subscriber = pubsub_v1.SubscriberClient()
subscription_path = "projects/operation-healthcare/subscriptions/operation-healthcare-topic-sub"


def callback(message):
    logger.debug(f"Message received: {message}")
    TransactionRepository().add_transaction_record(message.data.decode("utf-8"))
    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
logger.info(f"Listening for messages on {subscription_path}")

if __name__ == "__main__":
    with subscriber:
        try:
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
