import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

try:
    response = ec2.describe_security_groups()
    values=response.values()
except ClientError as e:
    print(e)



#print(response['SecurityGroups'])

for item in values:
  if isinstance(item, list):
    for p in item:
      if isinstance(p.values(), list):
        for thing in p.values():
          print(thing)
#i = 0
#
#sec_group_id_list = set()
## while i < len(response['SecurityGroups']):
#for i in range(len(response['SecurityGroups'])):
#  sec_group_id_list.add(str(response['SecurityGroups'][i]['GroupId']))
#  i=i+1
#
#print(sec_group_id_list)
