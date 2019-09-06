import boto3
account_list = { '272': 'Imaging Prod', '202': 'Dev', '230': 'QA', '439': 'Prod', '133': 'Ops', '353': 'Original' }

profile_list = [ '133', '202', '230', '272', '353', '439',]

for profile in profile_list:
  session = boto3.Session(profile_name = profile)
  ec2 = session.client('ec2', region_name = 'us-east-1')
  sec_groups = ec2.describe_security_groups().get('SecurityGroups')

  #  ec2.describe_security_groups().get('SecurityGroups')[0].get('IpPermissions')[0].get('IpRanges')

  for p in range(len(sec_groups)):
    x = len(sec_groups[p].get('IpPermissions'))
    name = sec_groups[p].get('GroupName')
    for n in range(x):
      result = sec_groups[p].get('IpPermissions')[n].get('IpRanges')
      for ip in result:
        val = ip.get('CidrIp')
        addr, r = val.split('/')
        if addr == '0.0.0.0':
          print (f"Profile {account_list.get(profile)} Name {name}")
