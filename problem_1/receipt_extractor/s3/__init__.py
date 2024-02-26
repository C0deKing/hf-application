from receipt_extractor.core.receipt import ReceiptProcessingService
from receipt_extractor.dynamodb.receipt_repository import DynamoReceiptRepository
from receipt_extractor.kinesis.receipt_message_service import KinesisReceiptMessageService
from receipt_extractor.s3.receipt_processing_service import S3ReceiptProcessingService


def receipt_processing_service_factory() -> ReceiptProcessingService:
    return S3ReceiptProcessingService(
        receipt_repository=DynamoReceiptRepository(),
        receipt_message_service=KinesisReceiptMessageService()
    )
