import boto3


def find_log_stream(profile_name, interface, hostname):


    session = boto3.Session(profile_name=profile_name)
    client = session.client('logs', region_name='us-east-1')

    response = client.describe_log_groups().get('logGroups')

    interfacelogs = interface + '-all'

    # we're traversing all the log groups
    for row in response:
        count = 0

        # this is a dictionary and we're extracting the name
        logGroupName = row.get('logGroupName')

        # let's make sure these are the logs we're looking for
        if logGroupName.startswith('cfg'):
            if 'vpc' in logGroupName:
                # print(f"Log group name: {logGroupName}")
                # let's get all the log streams from the particular log group
                logStream = client.describe_log_streams(
                    logGroupName=logGroupName)

                for row in logStream.get('logStreams'):
                    logStreamName = row.get('logStreamName')
                    if interface in logStreamName:
                        response = client.get_log_events(
                            logGroupName=logGroupName,
                            logStreamName=logStreamName
                        )
                        count += 1
                        # for row in response.get('events'):
                        #     print(row.get('message') + ' ' +  hostname + '\n')
                        return response


account_list = {
    '272': 'Imaging Prod',
    '202': 'Dev',
    '230': 'QA',
    '439': 'Prod',
    '133': 'Ops',
    '353': 'Original'}
profile_list = ['133', '202', '230', '272', '353', '439', ]

for profile_name in profile_list:
    session = boto3.Session(profile_name=profile_name)

    server_list = session.resource('ec2', region_name='us-east-1')

    interfacedict = {}
    for server in server_list.instances.all():
        tags = server.tags

        if tags is not None:
            for tag in tags:
                if tag.get('Key') == 'Name':
                    interfacelist = []
                    for interface in server.network_interfaces:
                        interfacelist.append(interface.id)
                    x = {tag.get('Value'): interfacelist}
                    interfacedict.update(x)
    all_logs = []
    undef = []
    response = None
    if interfacedict:
        print(f"Account: {account_list.get(profile_name)}")
        for key, val in interfacedict.items():
            print(f"Key: {key} and Value: {val}")
            for i in val:
                resp = find_log_stream(profile_name, i, key)
                if response is None:
                  print(f"{key}")
