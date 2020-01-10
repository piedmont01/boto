import boto3

session = boto3.Session(profile_name='famc-prod')
client = session.client('ec2', region_name='us-east-1')


reservations = client.describe_instances(
    Filters=[
        {'Name': 'tag-key', 'Values': ['backup', 'Backup']},
    ]
    ).get(
        'Reservations', []
    )
instances = sum(
    [
        [i for i in r['Instances']]
        for r in reservations
    ], [])

print(instances)
