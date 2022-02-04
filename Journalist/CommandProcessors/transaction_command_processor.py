from Infrastructure.exceptions import RecordNotFoundException, BadRequestException
from Infrastructure.Models import TransactionRecord
from Infrastructure.RepositoryKeeper import SKURepository
from Journalist.publisher import TransactionPublisher


class TransactionCommandProcessor:
    @classmethod
    def post_transaction(cls, transaction: TransactionRecord) -> str:
        """
        Publish message with new transaction record to PubSub topic and return message ID
        """
        # Verify sku_id exists in repository
        try:
            sku_record = SKURepository().get_sku_record(transaction.sku_id)
        except RecordNotFoundException:
            raise BadRequestException(error_description=f"Invalid SKU ID {transaction.sku_id}")

        # Convert sku_price from float to str
        transaction_values = [str(value) for value in transaction.dict(exclude={"transaction_date"}).values()]
        transaction_record = ",".join(transaction_values)
        return TransactionPublisher().publish_transaction(transaction_record)
