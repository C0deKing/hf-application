import os
from typing import Optional

import boto3
import requests

from receipt_extractor.core.receipt import ReceiptProcessingService, \
    Receipt, ReceiptRepository, ReceiptStatus, ReceiptMessageService


class S3ReceiptProcessingService(ReceiptProcessingService):
    def __init__(self,
                 receipt_repository: ReceiptRepository,
                 receipt_message_service: ReceiptMessageService,
                 bucket_name: Optional[str] = None
                 ):
        if bucket_name is None:
            self.bucket_name = os.environ.get('S3_BUCKET_NAME', 'receipt-data')
        else:
            self.bucket_name = bucket_name
        self._s3_client = boto3.client('s3')
        self._receipt_repository = receipt_repository
        self._receipt_message_service = receipt_message_service

    def process_image(self, receipt: Receipt) -> Receipt:
        receipt = receipt.model_copy(
            update={
                'status': ReceiptStatus.PROCESSING
            }
        )
        self._receipt_repository.save(receipt)

        download_image_request = requests.get(receipt.image_url)
        if download_image_request.status_code != 200:
            pass

        image_content = download_image_request.content
        image_extension = receipt.image_url.path.split('.')[-1]
        image_path = f'images/request_id={receipt.request_id}/image.{image_extension}'
        self._s3_client.put_object(
            Body=image_content,
            Bucket=self.bucket_name,
            Key=image_path,
            ContentType='image'
        )
        receipt_request = receipt.model_copy(
            update={
                'status': ReceiptStatus.PROCESSED,
                'file_path': image_path
            }
        )
        self._receipt_repository.save(receipt_request)
        self._receipt_message_service.send(receipt_request)
        return receipt_request
