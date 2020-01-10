import boto3
import os

#
# AWS accounts at FAMC
#
profile_list = ['famc-legacy', 'famc-qa', 'famc-ops', 'famc-prod' ]

for pro in profile_list:

  instance_volumes = []

  cmdstring = "gimme-aws-creds --profil %s" % (pro)
  os.system(cmdstring)

  session=boto3.Session(profile_name=pro)
  client=session.resource('ec2', region_name='us-east-1')
  running_instances = []
  stopped_instances = []

  #
  # traverse through all the servers in the account
  #
  for server in client.instances.all():
    
    print(server.id + ' ' + str(server.ami_launch_index))
  
    #
    # These instances are stopped
    #
    if server.state.get('Name') == 'stopped':
      stopped_instances.append(server.id)
    #
    # These instances are running
    #
    elif server.state.get('Name') == 'running':
      running_instances.append(server.id)
  
  
    #
    # print keyname
    #
    # print (server.key_name)
  
    #
    # print tags
    #
    # print (server.tags)
  
    #
    # print volumes - returns type list
    #
    volumes = server.volumes.all()
    volumes = server.volumes.filter(Filters=[{'Name': 'encrypted', 'Values': ['false']}, {'Name': 'status', 'Values': ['in-use']}]) # if you want to list out only attached volumes
  
    # print ([volume.id for volume in volumes])
  
    #
    # print volumes - returns type string
    #
    # for volume in volumes:
    #   print(volume.id)
  
    for volume in volumes:
      if server.state.get('Name') == 'running':
        instance_volumes.append(volume.id)
        
  
    #
    # list out server tags
    #
    # tags = server.tags
    # for thing in tags:
    #   if thing.get('Key')=='Name':
    #     print(thing.get('Value'))
