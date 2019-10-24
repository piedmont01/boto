import boto3

account_list = { '272': 'Imaging Prod', '202': 'Dev', '230': 'QA', '439': 'Prod', '133': 'Ops', '353': 'Original' }

x = []
profile_list = [ '272', '202', '230', '439', '353' ]
for profile_name in profile_list:
  session = boto3.Session(profile_name=profile_name)
  client = session.client('route53', region_name='us-east-1')

  response = client.list_hosted_zones()
  if response != '':
    print(f"Profile: {profile_name} {account_list.get(profile_name)}")
    for key, val in response.items():
      if key == 'HostedZones':
        for i in val:
          print(f"\t{i['Name']}")
          l = client.list_resource_record_sets(HostedZoneId=i['Id'])
          for a,b in l.items():
            if a == 'ResourceRecordSets':
              for each in b:
                for ky, vl in each.items():
                  if ky == 'Type':
                    typ = vl
                  if ky == 'ResourceRecords':
                    for everything in vl:
                      #print(f"\t\t{everything}")
                      print(f"\t\tType {typ} is {everything['Value']}")
