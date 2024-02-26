from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, HttpUrl


class ReceiptErrorType(Enum):
    INVALID_IMAGE = "INVALID_IMAGE"
    ERROR_PROCESSING = "ERROR_PROCESSING"
    BAD_REQUEST = "BAD_REQUEST"


class ReceiptError(BaseModel):
    type_: ReceiptErrorType
    message: str


class ReceiptField(BaseModel):
    """
    ReceiptField: Represents an individual line item in the receipt
    """
    item: Optional[str]
    quantity: Optional[Union[int, str, float]]
    price: Optional[Union[int, str, float]]


class ReceiptTotal(BaseModel):
    """
    ReceiptTotal: Represents the total for the receipt
    """
    price: Union[int, str, float]


class ReceiptData(BaseModel):
    """
    ReceiptData: Represents the data to be extracted from a receipt
    """
    entries: Optional[List[ReceiptField]]
    total: Optional[ReceiptTotal]


class ReceiptRequest(BaseModel):
    """
    ReceiptRequest: Represents the required inputs to interact with the receipt extraction system
    """
    application_id: str
    image_url: HttpUrl
    request_id: Optional[UUID] = None


class ReceiptStatus(Enum):
    RECEIVED = "RECEIVED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    EXTRACTING = "EXTRACTING"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"


class ImageType(Enum):
    PNG = "png"
    JPG = "jpg"


class Receipt(BaseModel):
    """
    Receipt: Represents the receipt we want to process data for. This is the core entity of the ReceiptExtractor system
    """
    application_id: UUID
    request_id: UUID
    image_url: HttpUrl
    status: ReceiptStatus
    file_path: Optional[str]
    image_type: ImageType
    data: Optional[ReceiptData] = None


class ReceiptProcessingService(ABC):
    """
    ReceiptProcessingService: Interface for a service that preprocesses a ReceiptRequest to ensure
        1. Constraints are met (i.e. File's can be downloaded and are well formed)
        2. Receipt files are persisted in AWS S3
    """

    @abstractmethod
    def process_image(self, receipt: Receipt) -> Receipt:
        """
        process_image: This function will ensure the receipt request is well formed, and will persist any required data
        :param receipt_request:
        :return:
        """
        pass


class ReceiptExtractionService(ABC):
    """
    ReceiptExtractionService: Interface for a service that will extract data from a processed receipt object
    """

    @abstractmethod
    def extract_data(self, receipts: List[Receipt]) -> List[Receipt]:
        """
        extract_data: extacts "ReceiptData" from a processed "Receipt".
        :param receipt: The processed receipt to extract receipt data from
        :return: ReceiptData
        """
        pass


class ReceiptRepository(ABC):
    """
    ReceiptRepository: Interface for performing CRUD operations on a Receipt object to store the metadata and extracted data in the data store
    """

    @abstractmethod
    def find(self, receipt_id: UUID) -> Optional[Receipt]:
        """
        find_receipt: fetches a receipt object based on the receipt ID
        :param receipt_id: a UUID representing the receipt object to retrieve
        :return: Optional[Receipt]
        """
        pass

    @abstractmethod
    def save(self, receipt: Receipt) -> None:
        """
        save_receipt: saves a receipt object to the datastore
        :param receipt: The receipt object to be stored
        :return: None
        """
        pass


class ReceiptMessageService(ABC):
    @abstractmethod
    def send(self, receipt: Receipt) -> None:
        """
        save_receipt: saves a receipt object to the datastore
        :param receipt: The receipt object to be stored
        :return: None
        """
        pass
