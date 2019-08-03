import boto3
from datetime import datetime
from dateutil import tz

client = boto3.client('logs')
response=client.describe_log_groups()

loglist=[]
for i in range(len(response['logGroups'])):
  thing = response['logGroups'][i]

  for p in thing.items():
    if p[0] == "logGroupName":
      val=str(p[1])
      print(val)
      loglist.append(val)
  print("-----")
  i=i+1


print(len(response['logGroups']))

client = boto3.client('logs')
for log in loglist:
  print(log)
  response=client.describe_log_streams(logGroupName=log, orderBy='LastEventTime',limit=10)
  for each in response.items():
    for this in each[1]:
      if this == 'logStreamName':
        print(each)
  print("---")
