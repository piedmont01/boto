import boto3


profile_list = [ '133', '202', '230', '272', '353', '439',]  
for profile in profile_list:
  print(profile)
  session = boto3.Session(profile_name=profile)
  server_list=session.resource('ec2', region_name='us-east-1')
  for server in server_list.instances.all():
    tags = server.tags
    server_state =  server.state.get('Name')
    if server_state == 'running':
      if server.tags is not None:
        for tag in server.tags:
          if tag is not None:
            print(tag)
