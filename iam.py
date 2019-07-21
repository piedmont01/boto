import boto3

client = boto3.client('iam')
response = client.list_users()

#for each in response.items():
#  for var in range(len(each)):
#    print(var,each[var])
#print("----")
#print(each[1])
user=[]


profile_list = [ '133', '202', '230', '272', '353', '439',] 

access_key = ['AKIAIC45ZM5KOUJXKXEA', 'AKIAIVT7X4IBUOBBNELQ', 'AKIAI3XODQP42YRZYVNQ', 'AKIAJHTSMM5MSDMEK72Q', 'AKIAIWCY2BZL57FIQ5ZA', 'AKIAJGZIB2533RIJSE7Q', 'AKIAIC45ZM5KOUJXKXEA', 'AKIAISOS6GMKGMBAF5OQ', 'AKIAJDOKZBTLIHE7ITHQ', 'AKIAITAA5VQEGMKS63WA', 'AKIAJIMAWPO5FHABTNJA', 'AKIAIM2XMEPEXFEGJVJA', 'AKIAJJQRET3ISBRE74NA', 'AKIAJMGBWTEOMTP5PUYQ', 'AKIAIY2PERDTHV2LPWDA', 'AKIAJA6TKHJ4LUW4WY5A', 'AKIAIBMR7YXPM6LDEZIQ', 'AKIAJS6PEHJTWUEZ4UXA' ]

mydict = {}

for profile_name in profile_list:
  no_access_key = []
  print(f"Profile Name: {profile_name}")
  session = boto3.Session(profile_name=profile_name)
  iam = session.client('iam', region_name='us-east-1') 
  response = iam.list_users()

  for each in response.items():
    if each[0] == "Users":
      for v in range(len(each[1])):
        mydict = each[1][v]
        user.append(mydict['UserName'])
  
  for person in user:
    try:
      paginator = client.get_paginator('list_access_keys')
      for response in paginator.paginate(UserName=person):
        for v in response.items():
          print(f"this is {v[1]}")
    except:
      no_access_key.append(person)

  mydict.update( {profile_name: no_access_key} )
  print(f"for profile {profile_name} these are users with no access keys {no_access_key}")

#for k, v in mydict.items():
#    print (f"key is {k} and value is {v}")
