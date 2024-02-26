import pytest

from receipt_extractor.core.receipt import ReceiptRepository, Receipt, ReceiptStatus, ReceiptData, ReceiptTotal, \
    ReceiptField, ImageType
from receipt_extractor.dynamodb.receipt_repository import DynamoReceiptRepository
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
        file_path=None,
        data=None
    )


def test_can_save_and_fetch_receipt(receipt_repository: ReceiptRepository, receipt: Receipt):
    receipt_repository.save(receipt)
    actual = receipt_repository.find(receipt_id=receipt.request_id)
    assert actual == receipt


def test_can_save_and_fetch_with_file_path(receipt_repository: ReceiptRepository, receipt: Receipt):
    receipt = receipt.model_copy(
        update={
            'file_path': 's3:/foo-bar/baz',
            'status': ReceiptStatus.PROCESSED
        }
    )
    receipt_repository.save(receipt)
    actual = receipt_repository.find(receipt_id=receipt.request_id)
    assert actual == receipt


def test_can_save_and_fetch_with_receipt_data(receipt_repository: ReceiptRepository, receipt: Receipt):
    receipt = receipt.model_copy(
        update={
            'file_path': 's3:/foo-bar/baz',
            'status': ReceiptStatus.PROCESSED,
            'data': ReceiptData(
                total=ReceiptTotal(price=100.0),
                entries=[ReceiptField(
                    item='Salad',
                    quantity=100,
                    price=1.0
                )]
            )
        }
    )
    receipt_repository.save(receipt)
    actual = receipt_repository.find(receipt_id=receipt.request_id)
    assert actual == receipt
