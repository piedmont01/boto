import json
import boto3
import socket
import time

retries = 10
retry_delay=10


def start_instance(region, instanceIDs):
    """
    #start_instance:This function will start the instance
    #param: region :- Name of region in which instance is deployed
    #param: instanceIDs:- List of instance ids
    #output:- None
    """
    print("Inside start_instance")
    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(InstanceIds = instanceIDs)
    print("Before start instance command")
    instances.start()
    print("After start instance command")
    for instance in instances:
        instance.wait_until_running()
        retry_count = 0
        #wait till instance came into running state and ip is assigned
        while retry_count <= retries:
            print("Public IP:"+str(instance.public_ip_address))
            instance.load()
            if instance.public_ip_address is not None:
                print("Public IP:"+str(instance.public_ip_address))
                time.sleep(retry_delay)
                break
            time.sleep(retry_delay)
            retry_count = retry_count + 1

        id = str(instance.id)
        print("Before creating ssm client command")
        ssm_client = boto3.client("ssm")
        s_command = "mkdir /home/test_EC2_start"
        ssm_command = ssm_client.send_command( InstanceIds=[id], DocumentName='AWS-RunShellScript',\
        Comment='Agent de-reg command', Parameters={ "commands":[ s_command ]  } )
        print("Inside Start command is executed")

def wait_for_command_execute(ssm_client, command_id, id):
    """
    #wait_for_command_execute:This function will wait until command get's executed
    #param: ssm_client :- ssm_client object
    #param: command_id:- Id of executed command
    #param: id:- Instance Id
    #output:- None
    """
    time.sleep(5)
    command_status = "Pending"
    #wait till command is executed
    while(command_status == "Pending" or command_status == "Delayed" or command_status == "In Progress"):
        output = ssm_client.list_commands(
            CommandId = command_id,
            InstanceId = id,
        )
        if any(cmd.get('StatusDetails', None) == 'Success' for cmd in output['Commands']):
            command_status =  "Success"
        elif any(cmd.get('StatusDetails', None) == 'Delivery Timed Out' for cmd in output['Commands']):
            command_status =  "Delivery Timed Out"
        elif any(cmd.get('StatusDetails', None) == 'Execution Timed Out' for cmd in output['Commands']):
            command_status =  "Execution Timed Out"
        elif any(cmd.get('StatusDetails', None) == 'Failed' for cmd in output['Commands']):
            command_status =  "Failed"
        elif any(cmd.get('StatusDetails', None) == 'Incomplete' for cmd in output['Commands']):
            command_status =  "Incomplete"
        elif any(cmd.get('StatusDetails', None) == 'Canceled' for cmd in output['Commands']):
            command_status =  "Canceled"
        elif any(cmd.get('StatusDetails', None) == 'Rate Exceeded' for cmd in output['Commands']):
            command_status =  "Rate Exceeded"

        print("Status:"+ command_status)
        print("output:"+str(output))
        print("=============================================================================")

    return command_status

def stop_instance(region, instanceIDs):
    """
    #stop_instance:This function will stop the instance
    #param: region :- Name of region in which instance is deployed
    #param: instanceIDs:- List of instance ids
    #output:- None
    """
    print("Inside stop_instance")
    for inst_id in instanceIDs:
        id = str(inst_id)
        ssm_client = boto3.client("ssm")
        s_command = "mkdir /home/test_EC2_stop"
        response = ssm_command = ssm_client.send_command( InstanceIds=[id], DocumentName='AWS-RunShellScript',\
            Comment='Agent de-reg command', Parameters={ "commands":[ s_command ]  } )

        command_id = response['Command']['CommandId']
        command_status = wait_for_command_execute(ssm_client, command_id, id)

    if command_status == "Success":
        print("Command is executed successfully...Stopping instance")
        time.sleep(retry_delay)
        ec2 = boto3.resource('ec2', region_name=region)
        ec2.instances.filter(InstanceIds = instanceIDs).stop() #for stopping an ec2 instance
    else:
        print("Cannot stop instance, command is not executed successfully...")


def terminate_instance(region, instanceIDs):
    """
    #terminate_instance:This function will terminate the instance
    #param: region :- Name of region in which instance is deployed
    #param: instanceIDs:- List of instance ids
    #output:- None
    """
    print("Inside terminate_instance")
    for inst_id in instanceIDs:
        id = str(inst_id)
        ssm_client = boto3.client("ssm")
        s_command = "cd /opt/Citizens/Core/bin/; ./EC2_Agent_MGMT.bash -c uninstall -d"
        response = ssm_command = ssm_client.send_command( InstanceIds=[id], DocumentName='AWS-RunShellScript',\
            Comment='Agent de-reg command', Parameters={ "commands":[ s_command ]  } )

        command_id = response['Command']['CommandId']
        command_status = wait_for_command_execute(ssm_client, command_id, id)

    if command_status == "Success":
        print("Command is executed successfully...Terminating instance")
        time.sleep(retry_delay)
        ec2 = boto3.resource('ec2', region_name=region)
        ec2.instances.filter(InstanceIds = instanceIDs).terminate() #for terminating an ec2 instance
    else:
        print("Cannot terminate instance, command is not executed successfully...")

def reboot_instance(region, instanceIDs):
    """
    #reboot_instance:This function will reboot the instance
    #param: region :- Name of region in which instance is deployed
    #param: instanceIDs:- List of instance ids
    #output:- None
    """
    print("Inside reboot_instance")
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.reboot_instances(InstanceIds=instanceIDs, DryRun=False)
    print("Instance reboot status:" + str(response))


def lambda_handler(event, context):
    """
    #lambda_handler:This is the begining of lambda
    #param: event :- event object
    #param: context:-
    #output:- None
    """
    #Get list of resources from events. It will be list of ARNs
    instance_arns = event['resources']
    instanceIDs = []
    for arn in instance_arns:
        instanceId = arn.split("/")[1]  #Get instance id only from ARN
        if instanceId != '':
            instanceIDs.append(instanceId)

    region = event['region']
    tag_name_dict = event['detail']['tags']
    changed_tage_dict = event['detail']['changed-tag-keys']
    changed_tage_dict = [x.lower() for x in changed_tage_dict]
    #convert all tags in lower case
    tag_name_dict =  {k.lower(): v.lower() for k, v in tag_name_dict.items()}

    if 'state' in tag_name_dict and 'state' in changed_tage_dict:
        if tag_name_dict['state'] == 'terminate':
            terminate_instance(region, instanceIDs)
        elif tag_name_dict['state'] == 'stop':
            stop_instance(region, instanceIDs)
        #elif tag_name_dict['state'] == 'start':
        #    start_instance(region, instanceIDs)
        #elif tag_name_dict['state'] == 'reboot':
        #    reboot_instance(region, instanceIDs)

    return {
        "statusCode": 200,
        "body": json.dumps('Instance operations are completed: ' + str(instanceIDs))
    }
