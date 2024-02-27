import json
import json

from receipt_extractor.dynamodb.receipt_repository import DynamoReceiptRepository

_receipt_repository = DynamoReceiptRepository()


def process_error(event, context):
    # TODO: Errors are not handled yet,
    #  but we need to retrieve the messages at the proper kinesis offset and update their status
    print(f'handle error {json.dumps(event)}')

    return {
        'message': 'Completed'
    }
