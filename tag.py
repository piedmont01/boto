from __future__ import print_function
import json
import boto3
import logging
import time
import datetime
import os
import re
import ast

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def getEnvsTags(user):
    sys_envList = []
    sys_value = []
    tag_list = {}
    chk_user = user
    for envs in os.environ.keys():
        if re.search('SYSID_',envs):
            sys_envList.append(envs)
            sys_value.append(os.environ.get(envs))
            list = ast.literal_eval(os.environ.get(envs))
            email_list = list.pop('Email',None)
            if email_list is not None:
                for email in email_list:
                    if (chk_user.lower()) == (email.lower()):
                        print ('User match found')
                        tag_list = list
    print (sys_value)
    print (sys_envList)
    if (len(tag_list) == 0) :
        print ('tag_list is None')
        return None
    else:
        print (tag_list)
        return (tag_list)

def defineTags(user,common_tags):
    envTags = getEnvsTags(user)
    all_Tags = common_tags
    if envTags is not None:
        for envTag in envTags.keys():
            tag = {'Key': envTag, 'Value':envTags.get(envTag)}
            all_Tags.append(tag)
    return (all_Tags)

def lambda_handler(event, context):
    #logger.info('Event: ' + str(event))
    print('Received event: ' + json.dumps(event, indent=2))

    ids = []


    try:
        region = event['region']
        detail = event['detail']
        eventname = detail['eventName']
        arn = detail['userIdentity']['arn']
        principal = detail['userIdentity']['principalId']
        userType = detail['userIdentity']['type']
        creationDate = detail['eventTime']
        print ('Assinged region, detail, eventname, arn, principal, userType, creationDate')

        if userType == 'IAMUser':
            user = detail['userIdentity']['userName']

        else:
            user = principal.split(':')[1]

        print ('User '+user)
        logger.info('principalId: ' + str(principal))
        logger.info('region: ' + str(region))
        logger.info('eventName: ' + str(eventname))
        logger.info('detail: ' + str(detail))
        print ('Check Response Elements')

        if not (detail['responseElements'] or eventname == 'CreateBucket'):
            logger.warning('No responseElements found')
            if detail['errorCode']:
                logger.error('errorCode: ' + detail['errorCode'])
            if detail['errorMessage']:
                logger.error('errorMessage: ' + detail['errorMessage'])
            return False
        common_tags = [{'Key': 'Requestor', 'Value': user}, {'Key': 'PrincipalId', 'Value': principal}, {'Key': 'creationDate', 'Value': creationDate}]
        allTags = defineTags(user,common_tags)
        ec2 = boto3.resource('ec2')



        print ('Check Event Match')
        if eventname == 'CreateVolume':
            ids.append(detail['responseElements']['volumeId'])
            logger.info(ids)


        elif eventname == 'RunInstances':
            items = detail['responseElements']['instancesSet']['items']

            for item in items:
                ids.append(item['instanceId'])
            logger.info(ids)
            logger.info('number of instances: ' + str(len(ids)))

            base = ec2.instances.filter(InstanceIds=ids)

            #loop through the instances
            for instance in base:
                for vol in instance.volumes.all():
                    ids.append(vol.id)
                for eni in instance.network_interfaces:
                    ids.append(eni.id)


        elif eventname == 'CreateImage':
            ids.append(detail['responseElements']['imageId'])
            logger.info(ids)


        elif eventname == 'CreateSnapshot':
            ids.append(detail['responseElements']['snapshotId'])
            logger.info(ids)

        elif eventname == 'CreateBucket':
            s3 = boto3.resource('s3')
            s3_bucketName = detail['requestParameters']['bucketName']
            if s3_bucketName:
                bucket_tagging = s3.BucketTagging(s3_bucketName)
                #print (ids)
                #allTags = defineTags(user,common_tags)
                #print (type(allTags))
                s3_resp = bucket_tagging.put(Tagging={'TagSet':allTags})
                print (s3_resp)
                #print ('Tagged S3 bucket')

        elif eventname == 'CreateDBInstance':
            print ('CreateDBInstance')
            rds = boto3.client('rds')
            rds_arn = detail['responseElements']['dBInstanceArn']
            if rds_arn:
                print('Tagging resource ' + rds_arn)
                #allTags = defineTags(user,common_tags)
                rds_resp = rds.add_tags_to_resource(ResourceName=rds_arn,Tags=allTags)
                print (rds_resp)

        elif eventname == 'CreateDBSnapshot':
            print ('CreateDBSnapshot')
            rds_snp = boto3.client('rds')
            rds_snp_arn = detail['responseElements']['dBSnapshotArn']
            if rds_snp_arn:
                print('Tagging resource ' + rds_snp_arn)
                #allTags = defineTags(user,common_tags)
                rds_snp_resp = rds_snp.add_tags_to_resource(ResourceName=rds_snp_arn,Tags=allTags)
                print (rds_snp_resp)

        elif eventname == 'CreateFileSystem':
            print ('CreateFileSystem')
            efs = boto3.client('efs')
            efs_fsid = detail['responseElements']['fileSystemId']
            if efs_fsid:
                print('Tagging resource ' + efs_fsid)
                efs_resp = efs.create_tags(FileSystemId=efs_fsid,Tags=allTags)
                print (efs_resp)

        elif eventname == 'CreateTable':
            print ('CreateTable')
            dyn = boto3.client('dynamodb')
            dyn_arn = detail['responseElements']['tableDescription']['tableArn']
            if dyn_arn:
                print('Tagging resource ' + dyn_arn)
                #allTags = defineTags(user,common_tags)
                table_status = detail['responseElements']['tableDescription']['tableStatus']
                table_name = detail['responseElements']['tableDescription']['tableName']
                while (table_status == 'CREATING'):
                    print ('Table is being created')
                    table_check = dyn.describe_table(TableName=table_name)
                    print(table_check)
                    table_status = table_check['Table']['TableStatus']
                    print (table_status)
                if (table_status == 'ACTIVE'):
                    dyn_resp = dyn.tag_resource(ResourceArn=dyn_arn,Tags=allTags)
                    print (dyn_resp)

        else:
            logger.warning('Not supported action')

        if ids:
            for resourceid in ids:
                print('Tagging resource ' + resourceid)
            #allTags = defineTags(user,common_tags)
            ec2.create_tags(Resources=ids, Tags=allTags)

        logger.info(' Remaining time (ms): ' + str(context.get_remaining_time_in_millis()) + '\n')
        return True
    except Exception as e:
        logger.error('Something went wrong: ' + str(e))
        return False

