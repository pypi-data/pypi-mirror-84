import boto3
from botocore.config import Config


def create_timestream_session(aws_access_key_id, aws_secret_access_key, region_name='eu-west-1'):
  session = boto3.Session(aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=region_name)
  return session


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


def write_to_timestream(records, database_name, table_name, ts_session):
  """
  Inserts a list of records into detech.ai's metrics
  """
  write_client = ts_session.client('timestream-write',
                                   config=Config(read_timeout=20,
                                                 max_pool_connections=5000,
                                                 retries={'max_attempts': 5}))
  # The records limit per batch is 100 as stated on AWS Timestream documentation
  limit = 100
  for i in range(0, len(records), limit):
    write_client.write_records(DatabaseName=database_name,
                               TableName=table_name,
                               Records=records[i:i + limit],
                               CommonAttributes={})


def query_from_timestream(sql_query, database_name, table_name, ts_session):
  query_client = ts_session.client('timestream-query')
  return query_client.query(QueryString=sql_query)
