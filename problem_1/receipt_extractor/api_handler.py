import json
from uuid import UUID

from receipt_extractor.core.receipt import ReceiptRequest, ReceiptError
from receipt_extractor.core.receipt_service import ReceiptService
from receipt_extractor.dynamodb.receipt_repository import DynamoReceiptRepository
from receipt_extractor.kinesis.receipt_message_service import KinesisReceiptMessageService

_receipt_repository = DynamoReceiptRepository()

_receipt_processing_service = ReceiptService(
    receipt_repository=_receipt_repository,
    receipt_message_service=KinesisReceiptMessageService()
)


def lambda_handler(event, context):
    method = event['httpMethod']
    if method == 'POST':
        body = json.loads(event['body'])
        request = ReceiptRequest.model_validate(body)
        receipt = _receipt_processing_service.receive_request(request)
        if isinstance(receipt, ReceiptError):
            return {
                'statusCode': 400,
                'body': receipt.model_dump_json()
            }
        else:
            return {
                'statusCode': 200,
                'body': receipt.model_dump_json()
            }
    elif method == 'GET':
        if 'queryStringParameters' in event and 'id' in event['queryStringParameters']:
            receipt_id = UUID(event['queryStringParameters']['id'])
            receipt = _receipt_repository.find(receipt_id)
            return {
                'statusCode': 200,
                'body': receipt.model_dump_json()
            }
        else:
            return {
                'statusCode': 400,
                'body': 'Please specify id as a query string parameter (e.g. GET /receipt/id=00000)'
            }
    else:
        return {
            'statusCode': 404,
            'body': 'Not Found'
        }
