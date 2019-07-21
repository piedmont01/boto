import boto3

x = []
profile_list = [ '272', '353', ] 
for profile_name in profile_list:
  print(f"Profile: {profile_name}")
  session = boto3.Session(profile_name=profile_name)
  client = session.client('route53', region_name='us-east-1')

  for key, val in client.list_hosted_zones().items():
    if key == 'HostedZones':
      for a in val:
        x.append(a['Id']) 
	
for i in x:
  resources = client.list_resource_record_sets(HostedZoneId=i)
  print(resources)
