import boto3
import datetime

import os.path, time


# create a Boto3 session
session = boto3.Session(profile_name='353')
client = session.client('logs', region_name='us-east-1')

# determin timestamp of file
FILE='flowlog_profile.txt'
print("last modified: %s" % time.ctime(os.path.getmtime(FILE)))
print("created: %s" % time.ctime(os.path.getctime(FILE)))

# open a file for writing
f = open(FILE, "w")

# Get log groups
response = client.describe_log_groups().get('logGroups')

# we're traversing all the log groups
for row in response:
    count = 0
    
    # this is a dictionary and we're extracting the name
    logGroupName = row.get('logGroupName')

    # let's make sure these are the logs we're looking for
    if logGroupName.startswith('cfg'):
      if 'vpc' in logGroupName:

        print(logGroupName)
 
        # let's get all the log streams from the particular log group
        logStream = client.describe_log_streams(logGroupName=logGroupName)

        for row in logStream.get('logStreams'):
          logStreamName = row.get('logStreamName')
          response = client.get_log_events( logGroupName=logGroupName, logStreamName=logStreamName)
          count += 1
          for row in response.get('events'):
            f.write(row.get('message') + '\n')
      print(f"Log Group Name: {logGroupName} and Count: {count}")

server_list=session.resource('ec2', region_name='us-east-1')
 
interfacedict = {}
for server in server_list.instances.all():
      tags = server.tags

      if tags is not None:
        for tag in tags:
          if tag.get('Key') == 'Name':
            interfacelist = []
            print(tag.get('Value'))
            for interface in server.network_interfaces:
              interfacelist.append(interface.id)
            x = { tag.get('Value') : interfacelist }
            interfacedict.update(x)


print(interfacedict)

f = open(FILE,"r")

if f.mode == "r":
    unfound = []
    masterlist = []
    success = 0
    fail = 0
    contents = f.read()
    row = contents.split('\n')
    mycount = 0
    for entry in row:
      if len(entry.split()) == 14:
        ver, acct, interface, srcaddr, dstaddr, srcport, dstport, protocol, numpackets, numbytes, starttime, endtime, action, logstatus = entry.split()
        success += 1

        if starttime != '-':
          starttime = int(starttime)
          starttime = datetime.datetime.fromtimestamp(starttime).strftime('%Y-%m-%d %H:%M:%S')

        if endtime != '-':
          endtime = int(endtime)
          endtime = datetime.datetime.fromtimestamp(endtime).strftime('%Y-%m-%d %H:%M:%S')


        if protocol == '17':
          protocol = 'TCP'
        elif protocol == '6':
          protocol = 'UDP'

        if srcport == '22':
          srcport = 'SSH'

        if dstport == '22':
          dstport = 'SSH'

        if srcport == '53':
          srcport = 'DNS'

        if dstport == '53':
          dstport = 'DNS'

        if srcport == '123':
          srcport = 'NTP'

        if dstport == '123':
          dstport = 'NTP'

        if srcport == '135' or  srcport == '136' or  srcport == '137' or  srcport == '138' or  srcport == '139':
          srcport = 'NetBIOS'

        if dstport == '135' or  dstport == '136' or  dstport == '137' or  dstport == '138' or  dstport == '139':
          dstport = 'NetBIOS'

        if srcport == '80':
          srcport = 'HTTP'

        if dstport == '80':
          dstport = 'HTTP'

        if srcport == '389':
          srcport = 'RDP'

        if dstport == '389':
          dstport = 'RDP'

        if srcport == '443':
          srcport = 'HTTPS'

        if dstport == '443':
          dstport = 'HTTPS'

        host = ''
        mydict = {}
        mydict['ver'] = ver
        mydict['acct'] = acct
        mydict['interface'] = interface
        mydict['srcaddr'] = srcaddr
        mydict['dstaddr'] = dstaddr
        mydict['srcport'] = srcport
        mydict['dstport'] = dstport 
        mydict['protocol'] = protocol
        mydict['numpackets'] = numpackets
        mydict['numbytes'] = numbytes
        mydict['starttime'] = starttime
        mydict['endtime'] = endtime
        mydict['action'] = action
        mydict['logstatus'] = logstatus
        for key, val in interfacedict.items():
          for i in val:
            if i in interface:
              host = key
              break
        if host:
          mydict['hostname'] = host
          masterlist.append(mydict)
        else:
          unfound.append(interface)
      else:
        print(success)
        fail += 1

masterlist_sorted = sorted(masterlist, key = lambda i: (i['hostname'], i['starttime']))
f.close()
f = open("/tmp/ab", "w")
print(len(masterlist))
for i in masterlist:
    f.write(str(i.keys())+'\n')
f.close()

f = open("/tmp/cd", "w")
for i in masterlist:
    f.write(i.get('hostname') + '\n')
f.close()

for p in set(unfound):
  print(p)

f = open("/tmp/final", "w")
for row in masterlist_sorted:
  f.write(str(row) + '\n')
f.close()
