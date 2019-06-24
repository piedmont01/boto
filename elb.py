import boto3
import boto3.session

session = boto3.Session(profile_name='ekendall')
client = session.client('elb', region_name='us-east-1')
response = client.modify_load_balancer_attributes(
 LoadBalancerName='test',
    LoadBalancerAttributes={
   'AccessLog':{ 
            'Enabled': True
        }
    }
)
