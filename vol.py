import boto3

profile_list = [ '133', '202', '230', '272', '353', '439' ]
account_list = { '272': 'Imaging Prod', '202': 'Dev', '230': 'QA', '439': 'Prod', '133': 'Ops', '353': 'Original' }
count=0

for profile in profile_list:
  count += 1
  total_size = 0 
  session = boto3.Session(profile_name=profile)
  client = session.client('ec2', region_name='us-east-1')
  print(f"Profile: {account_list.get(profile)}")
  for row in client.describe_volumes().get('Volumes'):
    print(f"{count}. {row.get('VolumeId')} {row.get('Size')}")
    count += 1
    total_size += row.get('Size')
  print (f"Total size for {account_list.get(profile)} is {total_size}")
  count=0

for profile in profile_list:
  session = boto3.Session(profile_name=profile)
  client = session.resource('ec2', region_name='us-east-1')
  
  for vol in client.volumes.all():
    if vol.state == 'available':
      v=client.Volume(vol.id)
      print(v)
      v.delete()
