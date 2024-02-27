import os
import re
from typing import List, Optional

import boto3

from receipt_extractor.core.receipt import ReceiptExtractionService, Receipt, ReceiptRepository, ReceiptData, \
    ReceiptField, ReceiptTotal, ReceiptStatus
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image


def _field_and_type_in_dict(item: dict, field: str, types: List[any]) -> Optional[any]:
    if field in item.keys() and any(isinstance(item[field], type_) for type_ in types):
        return item[field]
    else:
        return None


def _parse_field(item: dict) -> ReceiptField:
    item_name = _field_and_type_in_dict(item, 'nm', [str])
    price = _field_and_type_in_dict(item, 'price', [int, float])
    quantity = _field_and_type_in_dict(item, 'cnt', [int, float])
    return ReceiptField(
        item=item_name,
        price=price,
        quantity=quantity
    )


def _parse_total(item: dict) -> Optional[ReceiptTotal]:
    if 'total' in item and 'total_price' in item['total']:
        return ReceiptTotal(price=item['total']['total_price'])
    else:
        return None


def _parse_menu(menu: List[dict]) -> List[ReceiptField]:
    return [_parse_field(item) for item in menu]


def _parse_output(output: dict) -> ReceiptData:
    return ReceiptData(
        entries=_parse_menu(output['menu']) if 'menu' in output else None,
        total=_parse_total(output)
    )


class TransformersReceiptExtractionService(ReceiptExtractionService):
    def __init__(self, receipt_repository: ReceiptRepository, bucket_name: Optional[str] = None):
        self._receipt_repository = receipt_repository
        self.processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
        self.model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
        if bucket_name is None:
            self.bucket_name = os.environ.get('S3_BUCKET_NAME', 'receipt-data')
        else:
            self.bucket_name = bucket_name
        self._s3_client = boto3.client('s3')

    def _receipt_file(self, receipt: Receipt) -> str:
        temp_file = f'/tmp/{receipt.request_id}.{receipt.image_type.value}'
        self._s3_client.download_file(self.bucket_name, receipt.file_path,
                                      temp_file)
        return temp_file

    def _process_output(self, sequence: str) -> dict:
        sequence = sequence.replace(self.processor.tokenizer.eos_token, "") \
            .replace(self.processor.tokenizer.pad_token, "")
        sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()
        return self.processor.token2json(sequence)

    def _update_status(self, receipt: Receipt, status: ReceiptStatus) -> Receipt:
        receipt = receipt.model_copy(
            update={
                'status': status
            }
        )
        self._receipt_repository.save(receipt)
        return receipt

    def extract_data(self, receipts: List[Receipt]) -> List[Receipt]:
        receipts = [self._update_status(receipt, ReceiptStatus.EXTRACTING) for receipt in receipts if
                    receipt.file_path is not None]
        files = [self._receipt_file(receipt) for receipt in receipts if receipt.file_path]
        images = [Image.open(file) for file in files]
        pixel_values = self.processor(images, return_tensors="pt").pixel_values
        task_prompt = "<s_cord-v2>"
        decoder_input_ids = self.processor.tokenizer([task_prompt for _ in range(len(receipts))],
                                                     add_special_tokens=False,
                                                     return_tensors="pt")["input_ids"]

        outputs = self.model.generate(pixel_values,
                                      decoder_input_ids=decoder_input_ids,
                                      max_length=self.model.decoder.config.max_position_embeddings,
                                      early_stopping=True,
                                      pad_token_id=self.processor.tokenizer.pad_token_id,
                                      eos_token_id=self.processor.tokenizer.eos_token_id,
                                      use_cache=True,
                                      num_beams=1,
                                      bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
                                      return_dict_in_generate=True,
                                      output_scores=True, )

        output = [self._process_output(sequence) for sequence in self.processor.batch_decode(outputs.sequences)]
        receipt_data = [
            _parse_output(data)
            for data in output
        ]

        updated_receipts = [
            receipt.model_copy(
                update={
                    'data': data,
                    'status': ReceiptStatus.COMPLETE
                }
            )
            for receipt, data in zip(receipts, receipt_data)
        ]
        for receipt in updated_receipts:
            self._receipt_repository.save(receipt)
        return updated_receipts
