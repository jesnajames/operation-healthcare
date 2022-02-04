import os
from google.cloud import pubsub_v1

from Infrastructure.config import ROOT_DIR


class TransactionPublisher:
    def __init__(self):
        creds_path = os.path.join(ROOT_DIR, "operation-healthcare-private-key.json")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path

        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = "projects/operation-healthcare/topics/operation-healthcare-topic"

    def publish_transaction(self, transaction_record: str) -> str:
        data = transaction_record.encode("utf-8")
        future = self.publisher.publish(self.topic_path, data)
        return future.result()


