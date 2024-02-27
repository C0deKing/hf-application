import os
from datetime import timezone, timedelta
from datetime import datetime

from typing import Optional, Any
from uuid import UUID
import boto3

from receipt_extractor.core.receipt import ReceiptRepository, Receipt, ReceiptStatus, ReceiptData, ImageType


class DynamoReceiptRepository(ReceiptRepository):
    def __init__(self, dynamo_client: Optional[Any] = None, retention_period_days: int = 1):
        if dynamo_client is None:
            region = os.environ.get('DYNAMODB_REGION', 'us-east-2')
            self._client = boto3.client('dynamodb', region_name=region)
        else:
            self._client = dynamo_client
        self._table_name = os.environ.get('DYNAMODB_TABLE_NAME', 'receipt-extractor_receipts')
        self._retention_period_days = retention_period_days

    def find(self, receipt_id: UUID) -> Optional[Receipt]:
        receipt_item = self._client.get_item(
            TableName=self._table_name,
            Key={
                'request_id': {'S': str(receipt_id)}
            }
        )['Item']
        receipt_data = None
        if 'data' in receipt_item is not None:
            receipt_data = ReceiptData.model_validate_json(receipt_item['data']['S'])
        return Receipt(
            application_id=UUID(receipt_item['application_id']['S']),
            request_id=UUID(receipt_item['request_id']['S']),
            image_url=receipt_item['image_url']['S'] if 'image_url' in receipt_item else None,
            status=ReceiptStatus(value=receipt_item['status']['S']),
            file_path=receipt_item['file_path']['S'] if 'file_path' in receipt_item else None,
            data=receipt_data,
            image_type=ImageType(receipt_item['image_type']['S'])
        )

    def save(self, receipt: Receipt) -> None:
        expiration_date = datetime.now(tz=timezone.utc) + timedelta(days=self._retention_period_days)
        receipt_item = {
            'application_id': {'S': str(receipt.application_id)},
            'request_id': {'S': str(receipt.request_id)},
            'status': {'S': receipt.status.value},
            'expire_at': {'N': str(expiration_date.timestamp())},
            'image_type': {'S': receipt.image_type.value}
        }
        if receipt.image_url is not None:
            receipt_item['image_url'] = {'S': str(receipt.image_url)}
        if receipt.file_path is not None:
            receipt_item['file_path'] = {'S': str(receipt.file_path)}
        if receipt.data is not None:
            receipt_item['data'] = {'S': receipt.data.model_dump_json()}

        self._client.put_item(
            TableName=self._table_name,
            Item=receipt_item
        )
