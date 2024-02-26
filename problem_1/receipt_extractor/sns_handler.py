import json
import json

from receipt_extractor.dynamodb.receipt_repository import DynamoReceiptRepository

_receipt_repository = DynamoReceiptRepository()


def process_error(event, context):
    print(f'handle error {json.dumps(event)}')

    return {
        'message': 'Completed'
    }
