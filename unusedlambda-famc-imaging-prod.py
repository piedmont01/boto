import boto3
import time
import sys

'''
This script will retrieve the list of functions from the region executed, create a
CloudTrail table in Athena, run a query to identify which functions have been invoked 
in the past 30 days, and print a list of those that are inactive. This allows you to 
understand if you have any Lambda functions not currently in use.

The script assumes the following:
1. You have CloudTrail Lambda data events enabled for all functions within your account
2. You have permissions to Athena and Lambda
3. You have Python and Boto3 installed
'''

# AWS region that you want to evaluate
# The script will only work in regions where Athena is supported
# Athena region availability can be found at https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/
REGION = "us-east-1"

# S3 bucket where Athena will store query history
# This bucket will be created in the region where the script is executed if it doesn't currently exist
#ATHENA_S3_BUCKET_NAME = "s3://athena-history-bucket-demo"
ATHENA_S3_BUCKET_NAME = "s3://athena-history-bucket-famc-imaging-prod"


# Athena table to create for CloudTrail logs
# This table will be created in the 'default' Athena database
TABLE_NAME = "cloudtrail_lambda_logs"

# Location of S3 bucket where CloudTrail logs are stored
# including CloudTrail Lambda data events
# CLOUDTRAIL_S3_BUCKET_NAME = "s3://{BucketName}/AWSLogs/{AccountID}/"
CLOUDTRAIL_S3_BUCKET_NAME = "s3://famc-imaging-prod-cloudtrail/AWSLogs/097856158272/"

CREATE_TABLE_QUERY_TEMPLATE = \
"""CREATE EXTERNAL TABLE {0} (
eventversion STRING,
userIdentity STRUCT<
  type:STRING,
  principalid:STRING,
  arn:STRING,
  accountid:STRING,
  invokedby:STRING,
  accesskeyid:STRING,
  userName:STRING,
  sessioncontext:STRUCT<
    attributes:STRUCT<
      mfaauthenticated:STRING,
      creationdate:STRING>,
    sessionIssuer:STRUCT<
      type:STRING,
      principalId:STRING,
      arn:STRING,
      accountId:STRING,
      userName:STRING>>>,
eventTime STRING,
eventSource STRING,
eventName STRING,
awsRegion STRING,
sourceIpAddress STRING,
userAgent STRING,
errorCode STRING,
errorMessage STRING,
requestParameters STRING,
responseElements STRING,
additionalEventData STRING,
requestId STRING,
eventId STRING,
resources ARRAY<STRUCT<
  ARN:STRING,accountId:
  STRING,type:STRING>>,
eventType STRING,
apiVersion STRING,
readOnly STRING,
recipientAccountId STRING,
serviceEventDetails STRING,
sharedEventID STRING,
vpcEndpointId STRING
)
PARTITIONED BY(year string)
ROW FORMAT SERDE 'com.amazon.emr.hive.serde.CloudTrailSerde'
STORED AS INPUTFORMAT 'com.amazon.emr.cloudtrail.CloudTrailInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION '{1}';"""

# Query to add a partition for 2018 to the CloudTrail table in Athena
CREATE_PARTITON_QUERY_TEMPLATE = """
ALTER TABLE {0} add partition (year="2018")
location '{1}/CloudTrail/{2}/2018/'"""

# Query used to search for Lambda data event Invoke activities for the past 30 days
LAST_RUN_QUERY_TEMPLATE = """
select json_extract_scalar(requestparameters, '$.functionName') as function_name, Max (eventtime) as "Last Run"
from {0}
where eventname='Invoke'
and year='2018'
and from_iso8601_timestamp(eventtime) > current_timestamp - interval '1' month
and json_extract_scalar(requestparameters, '$.functionName') in ({function_arns})
group by json_extract_scalar(requestparameters, '$.functionName')"""

lambda_client = boto3.client('lambda', region_name=REGION)
athena_client = boto3.client('athena', region_name=REGION)

# Retrieve a list of the function ARNs for the specified Region
def retrieve_function_arns(lambda_client):
    function_arns = []
    retrieve_function_arns.count=0
    functions = lambda_client.list_functions()
    for fn in functions['Functions']:
        retrieve_function_arns.count +=1
        function_arns.append(str(fn['FunctionArn']))

    print("You have {} functions in the ".format(retrieve_function_arns.count)+REGION+" region\n")
    if (retrieve_function_arns.count==0):
        print("The script will now exit")
        sys.exit()
    print("Now the script will run the following Athena queries:\n")
    print("1) Create the Athena table for CloudTrail")
    print("2) Add a partition for 'year' to the new table")
    print("3) Query Athena for the Lambda functions that have been invoked in the past 30 days\n")
    time.sleep(2)
    return function_arns


def run_query(athena_client, query):
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': 'default'
        },
        ResultConfiguration={
            'OutputLocation': ATHENA_S3_BUCKET_NAME+"-"+REGION,
        }
    )
    print('Query Execution ID: ' + response['QueryExecutionId'])
    execution_status = None
    while execution_status != 'SUCCEEDED':
        waiter = athena_client.get_query_execution(
            QueryExecutionId = response['QueryExecutionId'].lstrip('ID')
        )
        execution_status = waiter['QueryExecution']['Status']['State']

        if execution_status == 'FAILED':
            print("The query failed. Check the Athena history for details.")
            return

        print("Running")
        time.sleep(5)

    results = athena_client.get_query_results(
        QueryExecutionId = response['QueryExecutionId']
    )
    return results


def build_query_strings(function_arns):
    function_arns_csv = str(function_arns)[1:-1]
    create_table_query = CREATE_TABLE_QUERY_TEMPLATE.format(TABLE_NAME, CLOUDTRAIL_S3_BUCKET_NAME)
    create_partition_query = CREATE_PARTITON_QUERY_TEMPLATE.format(TABLE_NAME, CLOUDTRAIL_S3_BUCKET_NAME, REGION)
    last_run_query = LAST_RUN_QUERY_TEMPLATE.format(TABLE_NAME, function_arns = function_arns_csv)
    return create_table_query, create_partition_query, last_run_query


def get_set_of_function_arns_from_result_set(result_set):
    set_of_functions_used = set()
    get_set_of_function_arns_from_result_set.count=0
    for row in result_set[1:]:
        get_set_of_function_arns_from_result_set.count +=1
        function_arn = row['Data'][0]['VarCharValue']
        set_of_functions_used.add(function_arn)
    return set_of_functions_used


def main():
    function_arns = retrieve_function_arns(lambda_client)
    queries = build_query_strings(function_arns)
    query_results = []
    for q in queries:
	    query_results.append(run_query(athena_client, q))

    # We made sure that the last query run gets the data that we care about
    result_set = query_results[-1]['ResultSet']['Rows']

    set_of_functions_used = get_set_of_function_arns_from_result_set(result_set)

    # Compare the results from Athena to the list of existing functions and print the difference
    unusedcount=retrieve_function_arns.count-get_set_of_function_arns_from_result_set.count
    print("\nOut of the {}, there are {} functions that haven't been invoked in the past 30 days".format(retrieve_function_arns.count, unusedcount))
    difference_list = list(set(function_arns) - set_of_functions_used)
    difference_list.sort(key=str.lower)

    for stale_function_arn in difference_list:
        print(stale_function_arn)


if __name__ == '__main__':
    main()
