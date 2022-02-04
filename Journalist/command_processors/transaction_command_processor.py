from Infrastructure.models import TransactionRecord
from Journalist.publisher import TransactionPublisher


class TransactionCommandProcessor:
    @classmethod
    def post_transaction(cls, transaction: TransactionRecord) -> str:
        """
        Publish message with new transaction record to PubSub topic and return message ID
        """
        # TODO Validate sku_id exists
        transaction_values = [str(value) for value in transaction.dict(exclude={"transaction_date"}).values()]
        transaction_record = ",".join(transaction_values)
        return TransactionPublisher().publish_transaction(transaction_record)
