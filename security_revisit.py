import boto3
from botocore.exceptions import ClientError


#try:
#    response = ec2.describe_security_groups()
#    values=response.values()
#except ClientError as e:
#    print(e)



#print(response['SecurityGroups'])

#for item in values:
#  if isinstance(item, list):
#    for p in item:
#      if isinstance(p.values(), list):
#        for thing in p.values():
#          print(thing)
#i = 0
#
#sec_group_id_list = set()
## while i < len(response['SecurityGroups']):
#for i in range(len(response['SecurityGroups'])):
#  sec_group_id_list.add(str(response['SecurityGroups'][i]['GroupId']))
#  i=i+1
#
#print(sec_group_id_list)

profile_list = [ '133', '202', '230', '272', '353', '439',] 

for profile in profile_list:
  session = boto3.Session(profile_name = profile)
  ec2 = session.client('ec2', region_name = 'us-east-1')
  security_group_list = []
  print(f"Profile name {profile}")
  for p in range(len(ec2.describe_security_groups().get('SecurityGroups'))):
    security_group_list.append(ec2.describe_security_groups().get('SecurityGroups')[p].get('GroupId'))

  for sec in security_group_list:
    ec2 = session.resource('ec2' , region_name='us-east-1')
    security_group = ec2.SecurityGroup(sec)

#  for sec in security_group_list:
#    ec2 = session.resource('ec2' , region_name='us-east-1')
#    security_group = ec2.SecurityGroup(sec)
#    print(security_group)
