import boto3
from botocore.config import Config


def create_timestream_write_client(aws_access_key_id,
                                   aws_secret_access_key,
                                   timeout=20,
                                   max_pool_connections=5000,
                                   retries=5):
  # Timestream is currently only available on eu-west-1
  region_name = 'eu-west-1'
  session = boto3.session.Session(aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)
  return session.client('timestream-write',
                        config=Config(read_timeout=timeout,
                                      max_pool_connections=max_pool_connections,
                                      retries={'max_attempts': retries}))


def create_timestream_query_client(aws_access_key_id, aws_secret_access_key):
  # Timestream is currently only available on eu-west-1
  region_name = 'eu-west-1'
  session = boto3.session.Session(aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)
  return session.client('timestream-query')


def prepare_metric_records(measure_name, measure_value, timestamp, dimensions):
  """
  Creates a metric record object to insert into Timestream
  """
  record = {
    'Time': str(timestamp),
    'Dimensions': dimensions,
    'MeasureName': measure_name,
    'MeasureValue': str(measure_value),
    'MeasureValueType': 'DOUBLE'
  }
  return record


def write_to_timestream(client, records, database_name, table_name):
  """
  Inserts a list of records into detech.ai's metrics
  """
  # The records limit per batch is 100 as stated on AWS Timestream documentation
  limit = 100
  for i in range(0, len(records), limit):
    client.write_records(DatabaseName=database_name,
                         TableName=table_name,
                         Records=records[i:i + limit],
                         CommonAttributes={})


def query_from_timestream(client, sql_query):
  return client.query(QueryString=sql_query)
