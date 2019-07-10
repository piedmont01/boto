import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

try:
    response = ec2.describe_security_groups()
    values=response.values()
except ClientError as e:
    print(e)



print(response['SecurityGroups'])

i = 0

sec_group_id_list = set()
# while i < len(response['SecurityGroups']):
for i in range(len(response['SecurityGroups'])):
  sec_group_id_list.add(str(response['SecurityGroups'][i]['GroupId']))
  i=i+1

filter(None,sec_group_id_list)
print(len(sec_group_id_list))

instances = ec2.describe_instances()
print(instances['Reservations'][1])

count=0
ec2_sec_groups = set()
while count < len(instances['Reservations']):
  for thing in instances['Reservations'][count]['Instances']:
    for l in thing['SecurityGroups']:
      ec2_sec_groups.add((l['GroupId']))
  count=count+1


print("-----")
print(sec_group_id_list)
print("-----")
print(ec2_sec_groups)

get_rid_of = sec_group_id_list.difference(ec2_sec_groups)

ec2 = boto3.client('ec2')
print("-----")
print(get_rid_of)
for this in get_rid_of:
  try: 
    response = ec2.delete_security_group( GroupId=this, DryRun=False )
  except:
    print(f"Security group in use: {this}") 
