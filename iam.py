import boto3

client = boto3.client('iam')
response = client.list_users()

for each in response.items():
  for var in range(len(each)):
    print(var,each[var])
print("----")
print(each[1])
user=[]


profile_list = [ '133', '202', '230', '272', '353', '439',] 

for profile_name in profile_list:
  print(f"Profile Name: {profile_name}")
  session = boto3.Session(profile_name=profile_name)
  iam = session.client('iam', region_name='us-east-1') 
  response = iam.list_users()

  for each in response.items():
    if each[0] == "Users":
      print(type(each[1]))
      for v in range(len(each[1])):
        mydict = each[1][v]
        user.append(mydict['UserName'])
  
  for person in user:
    try:
      paginator = client.get_paginator('list_access_keys')
      for response in paginator.paginate(UserName=person):
        for v in response.items():
          print(v)
    except:
      print(f"User {person} has no access key")
