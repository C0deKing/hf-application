import os
from typing import Optional
from uuid import UUID

import boto3

from receipt_extractor.core.receipt import Receipt, ReceiptMessageService


class KinesisReceiptMessageService(ReceiptMessageService):

    def __init__(self, stream_name: Optional[str] = None):
        self._client = boto3.client('kinesis')
        if stream_name is None:
            self._stream_name = os.environ.get('KINESIS_STREAM')
        else:
            self._stream_name = stream_name

    def send(self, receipt: Receipt) -> None:
        self._client.put_record(
            StreamName=self._stream_name,
            Data=receipt.model_dump_json().encode(),
            PartitionKey=str(receipt.application_id)
        )
