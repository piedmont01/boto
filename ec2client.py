import boto3

client = boto3.client('ec2')

for row in client.describe_instances().get('Reservations'):
  for row in row.get('Instances'):
    print (row.get('InstanceId'))
