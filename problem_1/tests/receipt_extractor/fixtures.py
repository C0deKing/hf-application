import boto3
import pytest
from testcontainers.core.container import DockerContainer


@pytest.fixture(scope='session')
def dynamo_client():
    container = DockerContainer("amazon/dynamodb-local") \
        .with_command("-jar DynamoDBLocal.jar -sharedDb") \
        .with_exposed_ports(8000) \
        .start()

    dynamo_client = boto3.client('dynamodb',
                                 endpoint_url=f'http://localhost:{container.get_exposed_port(8000)}',
                                 region_name='local',
                                 aws_access_key_id='key',
                                 aws_secret_access_key='keyboard_cat')

    dynamo_client.create_table(
        TableName='receipt-extractor_receipts',
        KeySchema=[
            {"AttributeName": "request_id", "KeyType": "HASH"}  # Partition key
        ],
        AttributeDefinitions=[
            {"AttributeName": "request_id", "AttributeType": "S"}  # Partition key
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10,
        }
    )

    yield dynamo_client
