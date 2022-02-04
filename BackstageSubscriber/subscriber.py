# TODO: Add docs and logs

import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

from Infrastructure.config import ROOT_DIR
from Infrastructure.repository_keeper import TransactionRepository


creds_path = os.path.join(ROOT_DIR, "operation-healthcare-private-key.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path

subscriber = pubsub_v1.SubscriberClient()
subscription_path = "projects/operation-healthcare/subscriptions/operation-healthcare-topic-sub"


def callback(message):
    TransactionRepository().add_transaction_record(message.data.decode("utf-8"))
    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)


if __name__ == "__main__":
    with subscriber:
        try:
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
