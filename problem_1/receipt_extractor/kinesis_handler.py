import base64

from receipt_extractor.core.receipt import Receipt
from receipt_extractor.dynamodb.receipt_repository import DynamoReceiptRepository
from receipt_extractor.kinesis.receipt_message_service import KinesisReceiptMessageService
from receipt_extractor.s3 import S3ReceiptProcessingService
from receipt_extractor.transformers.receipt_extraction_service import TransformersReceiptExtractionService

_receipt_repository = DynamoReceiptRepository()

_receipt_processing_service = S3ReceiptProcessingService(
    receipt_repository=_receipt_repository,
    receipt_message_service=KinesisReceiptMessageService()
)


def process_receipt(event, context):
    if event['Records'] and len(event['Records']) > 0:
        base_64_encoded_data = [event['kinesis']['data'] for event in event['Records']]
        decoded_data = [base64.b64decode(raw_data) for raw_data in base_64_encoded_data]
        receipts = [Receipt.model_validate_json(data) for data in decoded_data]
        for receipt in receipts:
            _receipt_processing_service.process_image(receipt)
    return {
        'message': 'Completed'
    }


def extract_data(event, context):
    _receipt_extraction_service = TransformersReceiptExtractionService(
        receipt_repository=_receipt_repository
    )

    if event['Records'] and len(event['Records']) > 0:
        base_64_encoded_data = [event['kinesis']['data'] for event in event['Records']]
        decoded_data = [base64.b64decode(raw_data) for raw_data in base_64_encoded_data]
        receipts = [Receipt.model_validate_json(data) for data in decoded_data]
        _receipt_extraction_service.extract_data(receipts)
    return {
        'message': 'Completed'
    }
