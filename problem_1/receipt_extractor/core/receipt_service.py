from typing import Union
from uuid import uuid1 as uuid

from receipt_extractor.core.receipt import ReceiptRepository, Receipt, ReceiptRequest, ReceiptError, ImageType, \
    ReceiptErrorType, ReceiptStatus, ReceiptMessageService


class ReceiptService:
    """
    ReceiptService: Interface for a service that preprocesses a ReceiptRequest to ensure
        1. Constraints are met (i.e. File's can be downloaded and are well formed)
        2. Receipt files are persisted in AWS S3
    """

    def __init__(self, receipt_repository: ReceiptRepository,
                 receipt_message_service: ReceiptMessageService):
        self.receipt_repository = receipt_repository
        self.receipt_message_service = receipt_message_service

    def receive_request(self, receipt_request: ReceiptRequest) -> Union[Receipt, ReceiptError]:
        """
        receive_request: This function will process the initial receipt request to make sure it is persisted into the receipt extraction system
        :param receipt_request:
        :return: Receipt
        """
        image_types = set(item.value for item in ImageType)
        extension = receipt_request.image_url.path.split('.')[-1]
        if extension not in image_types:
            return ReceiptError(
                type_=ReceiptErrorType.BAD_REQUEST,
                message='You must specify a JPG or PNG image'
            )

        if receipt_request.request_id is None:
            receipt_request = receipt_request.model_copy(
                update={'request_id': uuid()}
            )
        receipt = Receipt(
            application_id=receipt_request.application_id,
            request_id=receipt_request.request_id,
            image_url=receipt_request.image_url,
            status=ReceiptStatus.RECEIVED,
            file_path=None,
            image_type=ImageType(extension),
            data=None,
        )
        self.receipt_repository.save(receipt)
        self.receipt_message_service.send(receipt)
        return receipt
