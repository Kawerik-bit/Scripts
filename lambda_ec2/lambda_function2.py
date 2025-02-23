import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# OpenSearch cluster details
REGION = "aws region"
HOST = "opensearch domain name"  # Replace with your OpenSearch endpoint
INDEX_NAME = "test-index"

# Get AWS credentials for signing requests
session = boto3.Session()
credentials = session.get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, REGION, 'es', session_token=credentials.token)

# Create OpenSearch client
client = OpenSearch(
    hosts=[{'host': HOST, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def lambda_handler(event, context):
    # Example document to index
    document = {
        "title": "Lambda OpenSearch Test",
        "content": "Testing AWS Lambda with OpenSearch.",
        "timestamp": "2025-02-19T12:00:00"
    }

    response = client.index(
        index=INDEX_NAME,
        body=document
    )

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
