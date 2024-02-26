import pytest

from receipt_extractor.core.receipt import ReceiptRepository, Receipt, ReceiptStatus, ReceiptExtractionService, \
    ImageType
from receipt_extractor.dynamodb.receipt_repository import DynamoReceiptRepository
from receipt_extractor.transformers.receipt_extraction_service import TransformersReceiptExtractionService
from tests.receipt_extractor.fixtures import dynamo_client
from uuid import uuid1 as random_uuid


@pytest.fixture
def receipt_repository(dynamo_client):
    return DynamoReceiptRepository(
        dynamo_client=dynamo_client
    )


@pytest.fixture(scope='function')
def receipt() -> Receipt:
    return Receipt(
        application_id=random_uuid(),
        request_id=random_uuid(),
        image_url='https://t3.ftcdn.net/jpg/01/82/01/18/360_F_182011806_mxcDzt9ckBYbGpxAne8o73DbyDHpXOe9.jpg',
        image_type=ImageType.JPG,
        status=ReceiptStatus.RECEIVED,
        file_path='images/request_id=0c0b626a-d1f9-11ee-a4d4-3753de4d104e/image.jpg',
        data=None
    )


@pytest.fixture(scope='function')
def receipt_extraction_service(receipt_repository: ReceiptRepository) -> ReceiptExtractionService:
    return TransformersReceiptExtractionService(
        receipt_repository=receipt_repository,
        bucket_name='hf-application-staging-receipt-data'
    )


def test_receipt_extraction_service(receipt: Receipt, receipt_extraction_service: ReceiptExtractionService):
    actual = receipt_extraction_service.extract_data([receipt, receipt])
    assert actual is not None
